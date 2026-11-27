import json
import re
from pathlib import Path

from .judge import EPSILON, UNDECIDED, judge, normalize_label
from .mac import mac
from .matrix import make_cross, validate_matrix
from .perf import print_performance

DATA_PATH = Path(__file__).resolve().parent.parent / "data.json"
FILTER_KEY = re.compile(r"size_([1-9][0-9]*)")
PATTERN_KEY = re.compile(r"size_([1-9][0-9]*)_[0-9]+")


def validate_filter_pair(group, n):
    if not isinstance(group, dict):
        raise ValueError("필터 그룹은 객체여야 합니다.")
    pair = {}
    for key, matrix in group.items():
        label = normalize_label(key)
        if label is None or label in pair:
            raise ValueError(f"알 수 없거나 중복된 필터 라벨 {key!r}")
        validate_matrix(matrix, n, f"{label} 필터")
        pair[label] = matrix
    if pair.keys() != {"Cross", "X"}:
        raise ValueError("Cross와 X 필터가 모두 필요합니다.")
    return pair


def load_filters(groups):
    filters, errors = {}, {}
    print("\n[필터 로드]")
    if not isinstance(groups, dict):
        print("스키마 오류: filters는 객체여야 합니다.")
        return filters, errors

    for key, group in groups.items():
        match = FILTER_KEY.fullmatch(key)
        if match is None:
            print(f"{key}: 필터 키는 size_N 형식이어야 합니다.")
            continue
        try:
            n = int(match[1])
            filters[n] = validate_filter_pair(group, n)
        except ValueError as error:
            errors[key] = str(error)
            print(f"{key}: {error}")
        else:
            print(f"{key}: Cross, X 필터 로드 완료")
    return filters, errors


def evaluate_case(case_id, case, filters, filter_errors):
    match = PATTERN_KEY.fullmatch(case_id)
    try:
        if match is None:
            raise ValueError("패턴 키는 size_N_idx 형식이어야 합니다.")
        n = int(match[1])
        if not isinstance(case, dict):
            raise ValueError("패턴 항목은 객체여야 합니다.")
        pattern = case.get("input")
        validate_matrix(pattern, n, "입력 패턴")
        expected = normalize_label(case.get("expected"))
        if expected is None:
            raise ValueError(f"알 수 없는 expected 라벨 {case.get('expected')!r}")
        if n not in filters:
            key = f"size_{n}"
            reason = filter_errors.get(key, "필터가 없거나 filters 구조가 잘못되었습니다.")
            raise ValueError(f"{key}: {reason}")
    except ValueError as error:
        return f"[데이터/스키마] {error}"

    pair = filters[n]
    try:
        cross_score = mac(pattern, pair["Cross"])
        x_score = mac(pattern, pair["X"])
        verdict = judge(cross_score, x_score)
    except (OverflowError, ValueError):
        return "[수치 비교] MAC 점수가 유한한 숫자 범위를 벗어났습니다."

    print(f"Cross 점수: {cross_score}")
    print(f"X 점수: {x_score}")
    print(f"판정: {verdict} | expected: {expected}")
    if verdict == expected:
        return None
    if verdict == UNDECIDED:
        return f"[수치 비교] 동점 (|Cross-X| < {EPSILON:g}, expected {expected})"
    return f"[로직] 점수가 높은 라벨 {verdict}와 expected {expected}가 다릅니다."


def run_json_mode(path=DATA_PATH):
    try:
        with open(path, encoding="utf-8-sig") as source:
            data = json.load(source)
    except FileNotFoundError:
        print(f"파일을 찾을 수 없습니다: {path}")
        return
    except (OSError, ValueError) as error:
        print(f"JSON을 읽을 수 없습니다: {error}")
        return

    if not isinstance(data, dict) or not isinstance(data.get("patterns"), dict):
        print("스키마 오류: 최상위 JSON과 patterns는 객체여야 합니다.")
        return

    filters, filter_errors = load_filters(data.get("filters"))
    patterns = data["patterns"]
    failures = {}

    print("\n[패턴 분석]")
    for case_id, case in patterns.items():
        print(f"\n{case_id}")
        reason = evaluate_case(case_id, case, filters, filter_errors)
        if reason is None:
            print("PASS")
        else:
            failures[case_id] = reason
            print(f"FAIL {reason}")

    # 모든 크기에 같은 형태의 입력을 사용해 데이터 검증과 성능 측정을 독립시킨다.
    samples = {}
    for n in (3, 5, 13, 25):
        cross = make_cross(n)
        samples[n] = (cross, cross)
    print_performance(samples)
    print(f"\n[결과 요약] 전체 {len(patterns)} / 통과 {len(patterns) - len(failures)} / 실패 {len(failures)}")
    for case_id, reason in failures.items():
        print(f"- {case_id} {reason}")
