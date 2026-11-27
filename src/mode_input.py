from .judge import EPSILON, UNDECIDED, judge
from .mac import mac
from .matrix import is_finite_number, make_matrix
from .perf import print_performance


def parse_number(token):
    try:
        return int(token)
    except ValueError:
        value = float(token)
        if not is_finite_number(value):
            raise ValueError("유한한 숫자를 입력하세요.")
        return value


def read_matrix(name, n=3):
    print(f"{name} ({n}줄, 공백으로 구분)")
    matrix = make_matrix(n)
    for row in range(n):
        while True:
            parts = input(f"{row + 1}/{n}행: ").split()
            if len(parts) != n:
                print(f"입력 형식 오류: 한 줄에 숫자 {n}개를 입력하세요.")
                continue
            try:
                matrix[row] = [parse_number(token) for token in parts]
            except ValueError:
                print("입력 형식 오류: 유한한 숫자를 입력하세요.")
                continue
            break
    return matrix


def run_input_mode():
    filter_a = read_matrix("필터 A")
    filter_b = read_matrix("필터 B")
    print("필터 A와 B를 저장했습니다.")
    pattern = read_matrix("패턴")

    try:
        score_a = mac(pattern, filter_a)
        score_b = mac(pattern, filter_b)
        verdict = judge(score_a, score_b, "A", "B")
    except (OverflowError, ValueError):
        print("연산 오류: MAC 점수가 유한한 숫자 범위를 벗어났습니다.")
        return

    print(f"\nA 점수: {score_a}")
    print(f"B 점수: {score_b}")
    if verdict == UNDECIDED:
        verdict = f"판정 불가 (|A-B| < {EPSILON:g})"
    print(f"판정: {verdict}")
    print_performance({3: (pattern, filter_a)})
