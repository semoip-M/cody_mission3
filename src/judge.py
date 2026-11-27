from .matrix import is_finite_number

EPSILON = 1e-9
UNDECIDED = "UNDECIDED"
LABELS = {"+": "Cross", "cross": "Cross", "plus": "Cross", "x": "X", "ex": "X"}


def normalize_label(raw):
    if isinstance(raw, str):
        return LABELS.get(raw.strip().lower())
    return None


def judge(a, b, label_a="Cross", label_b="X"):
    if not is_finite_number(a) or not is_finite_number(b):
        raise ValueError("MAC 점수가 유한한 숫자 범위를 벗어났습니다.")
    if abs(a - b) < EPSILON:
        return UNDECIDED
    return label_a if a > b else label_b
