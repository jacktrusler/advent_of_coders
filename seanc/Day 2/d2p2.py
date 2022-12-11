def score(opp_play, desired_outcome):
    score = round_score(desired_outcome) + choice_score(opp_play, desired_outcome)
    return score

def round_score(desired_outcome):
    if ((desired_outcome == "Z")):
        return 6 # WIN
    if ((desired_outcome == "X")):
        return 0 # LOSE
    if ((desired_outcome == "Y")):
        return 3 # DRAW


def choice_score(opp_play, desired_outcome):
    if (desired_outcome == "X"):
        if (opp_play == "A"):
            return 3
        if (opp_play == "B"):
            return 1
        if (opp_play == "C"):
            return 2       
    if (desired_outcome == "Y"):
        if (opp_play == "A"):
            return 1
        if (opp_play == "B"):
            return 2
        if (opp_play == "C"):
            return 3           
    if (desired_outcome == "Z"):
        if (opp_play == "A"):
            return 2
        if (opp_play == "B"):
            return 3
        if (opp_play == "C"):
            return 1       

if __name__ == "__main__":
    input = "Day 2/input.txt"
    total_score = 0 
    with open(input) as f:
        lines = f.readlines()
    for line in lines:
        opp_play = line[0].strip()
        desired_outcome= line[2].strip()
        total_score = total_score + score(opp_play, desired_outcome)
    print(total_score)
