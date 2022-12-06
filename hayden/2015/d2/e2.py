"""I Was Told There Would Be No Math"""


def main():
    """Exercise 2"""
    with open(file="inputs.txt", mode="r", encoding="utf-8") as f_present_list:
        required_ribbon = 0
        for present_str in f_present_list:
            present_str = present_str.strip()
            [l, w, h] = [int(dim) for dim in present_str.split("x")]
            lw_face = (2*l)+(2*w)
            wh_face = (2*h)+(2*w)
            hl_face = (2*h)+(2*l)
            required_ribbon += (l * w * h) \
                + min(lw_face, wh_face, hl_face)
        print(required_ribbon, " linear ft.")


if __name__ == "__main__":
    main()
