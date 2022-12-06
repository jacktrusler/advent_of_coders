"""Figure Santas Floor"""


def main():
    """Stairmaster"""
    with open(file="input.txt", mode="r", encoding="utf-8") as f_steps:
        steps = f_steps.readline()
        f_steps.close()
        floor = 0
        for step in steps:
            if step == "(":
                floor += 1
            elif step == ")":
                floor -= 1
        print("ends up on ", floor)


if __name__ == "__main__":
    main()
