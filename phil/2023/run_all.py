import importlib
import pathlib
import utils


def main():
    for day in range(1, 26):
        try:
            puzzle = importlib.import_module(f"day{day:02}")
        except ModuleNotFoundError:
            continue
        puzzle_input = pathlib.Path(__file__).parent / "input" / f"{day:02}.txt"
        a, b, elapsed_ms = utils.run_solution(puzzle.solve, puzzle_input)
        print(f"[Day {day:02}] Time(ms):{elapsed_ms} A:{a} B:{b}")


if __name__ == "__main__":
    main()
