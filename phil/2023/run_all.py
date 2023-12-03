import importlib


def main():
    for problem in range(1, 26):
        try:
            mod = importlib.import_module(f"day{problem:02}")
        except ModuleNotFoundError:
            continue
        a, b, elapsed_ms = mod.solve()
        print(f"[Day {problem:02}] A:{a} / B:{b} / Time(ms):{elapsed_ms}")


if __name__ == "__main__":
    main()
