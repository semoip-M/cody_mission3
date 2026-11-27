from src.mode_input import run_input_mode
from src.mode_json import run_json_mode


def main():
    print("=== Mini NPU Simulator ===")
    print("1. 사용자 입력 (3×3)")
    print("2. data.json 분석")
    try:
        while True:
            choice = input("선택: ").strip()
            if choice == "1":
                run_input_mode()
                return
            if choice == "2":
                run_json_mode()
                return
            print("1 또는 2를 입력하세요.")
    except (EOFError, KeyboardInterrupt):
        print("\n입력이 종료되었습니다.")


if __name__ == "__main__":
    main()
