"""I Was Told There Would Be No Math"""


def main():
    """Exercise 1"""
    with open(file="inputs.txt", mode="r", encoding="utf-8") as f_present_list:
        required_wrapping_sqft = 0
        for present_str in f_present_list:
            present_str = present_str.strip()
            [l, w, h] = [int(dim) for dim in present_str.split("x")]
            lw_face = l*w
            wh_face = h*w
            hl_face = h*l
            required_wrapping_sqft += 2*(lw_face+wh_face+hl_face) \
                + min(lw_face, wh_face, hl_face)
        print(required_wrapping_sqft, " sqft.")


if __name__ == "__main__":
    main()
