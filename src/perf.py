from time import perf_counter

from .mac import mac

REPEAT = 10


def measure_mac_ms(pattern, filt):
    elapsed = 0.0
    for _ in range(REPEAT):
        start = perf_counter()
        mac(pattern, filt)
        elapsed += perf_counter() - start
    return elapsed * 1000 / REPEAT


def print_performance(samples):
    print(f"\n[성능 분석] MAC 1회 평균 ({REPEAT}회 반복)")
    print("크기(N×N)   평균 시간(ms)   연산 횟수(N²)")
    for n, (pattern, filt) in sorted(samples.items()):
        average = measure_mac_ms(pattern, filt)
        print(f"{n}×{n:<10} {average:>12.6f} {n * n:>14}")
