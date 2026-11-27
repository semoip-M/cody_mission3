from math import isfinite


def make_matrix(n, fill=0):
    return [[fill for _ in range(n)] for _ in range(n)]


def is_square(matrix, n):
    return (
        isinstance(matrix, list)
        and len(matrix) == n
        and all(isinstance(row, list) and len(row) == n for row in matrix)
    )


def is_finite_number(value):
    return type(value) is int or (type(value) is float and isfinite(value))


def validate_matrix(matrix, n, name):
    if not is_square(matrix, n):
        raise ValueError(f"{name} 크기 불일치 (필요한 크기 {n}×{n})")
    if any(not is_finite_number(value) for row in matrix for value in row):
        raise ValueError(f"{name}에는 유한한 숫자만 넣을 수 있습니다.")


def make_cross(n):
    matrix = make_matrix(n)
    middle = n // 2
    for index in range(n):
        matrix[middle][index] = 1
        matrix[index][middle] = 1
    return matrix
