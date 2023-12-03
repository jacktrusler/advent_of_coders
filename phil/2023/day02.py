from pathlib import Path
import utils

@utils.solver(Path(__file__).parent / "input" / "02.txt")
def solve(raw_input: str):
    a = 0
    b = 0
    cube_max = {"red": 12, "green": 13, "blue": 14}
    for line in raw_input.splitlines():
        cube_min = {"red": 0, "green": 0, "blue": 0}
        possible = True
        game_id_text, game_text = line.split(":")
        for trial_text in game_text.split(";"):
            for cube_info in trial_text.split(","):
                n_text, color = cube_info.split()
                n = int(n_text)
                if n > cube_max[color]:
                    possible = False
                if n > cube_min[color]:
                    cube_min[color] = n
        if possible:
            a += int(game_id_text.split()[1])
        b += cube_min["red"] * cube_min["blue"] * cube_min["green"]
    return a, b

if __name__ == '__main__':
    utils.report(*solve())
