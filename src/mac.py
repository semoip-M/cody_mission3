def mac(pattern, filt):
    """검증된 동일 크기의 정사각 행렬 두 개의 MAC 점수를 구한다."""
    total = 0
    n = len(pattern)
    for row in range(n):
        for col in range(n):
            total += pattern[row][col] * filt[row][col]
    return total
