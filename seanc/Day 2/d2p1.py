def score(opp_play, my_play):
    score = round_score(opp_play, my_play) + choice_score(my_play)
    return score

def round_score(opp_play, my_play):
    if ((opp_play == "A"  and my_play == "Y") or (opp_play == "B"  and my_play == "Z") or (opp_play == "C"  and my_play == "X")):
        return 6 # WIN
    if ((opp_play == "A"  and my_play == "Z") or (opp_play == "B"  and my_play == "X") or (opp_play == "C"  and my_play == "Y")):
        return 0 # LOSE
    if ((opp_play == "A"  and my_play == "X") or (opp_play == "B"  and my_play == "Y") or (opp_play == "C"  and my_play == "Z")):
        return 3 # DRAW


def choice_score(my_play):
    if (my_play == "X"):
        return 1
    if (my_play == "Y"):
        return 2
    if (my_play == "Z"):
        return 3


if __name__ == "__main__":
    input = "Day 2/input.txt"
    total_score = 0 
    with open(input) as f:
        lines = f.readlines()
    for line in lines:
        opp_play = line[0].strip()
        my_play = line[2].strip()
        total_score = total_score + score(opp_play, my_play)
    print(total_score)
