"""Figure Santas Floor"""


def main():
    """Stairmaster"""
    with open(file="input.txt", mode="r", encoding="utf-8") as f_steps:
        steps = f_steps.readline()
        f_steps.close()
        floor = 0
        it_step = 0
        for step in steps:
            it_step += 1
            if step == "(":
                floor += 1
            elif step == ")":
                floor -= 1
            if floor == -1:
                print("Went under at ", it_step)
                break


if __name__ == "__main__":
    main()
