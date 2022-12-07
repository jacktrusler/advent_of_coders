def main():
  text = open('../p1/rpsInput.txt').read()
  games = text.split('\n')
  total = 0
  for game in games:
    round = game.split(' ')
    score = choiceScoring(round)
    total += score
  print(f"The total score for all the round is {total}!")

def choiceScoring(round):
  choice = round[0]
  outcome = round[1]
  choices = {
  'A' : 1,#rock
  'B' : 2,#paper
  'C' : 3 #scissors
  }
  obj = {}
  if (outcome == 'X'):#lose
    obj = {
    'A' : 'C',#rock
    'B' : 'A',#paper
    'C' : 'B' #scissors
    }
  elif (outcome == 'Y'):#draw
    obj = {
    'A' : 'A',#rock
    'B' : 'B',#paper
    'C' : 'C' #scissors
    }
  elif (outcome == 'Z'):#win
    obj = {
    'A' : 'B',#rock
    'B' : 'C',#paper
    'C' : 'A' #scissors
    }
  return choices[obj[choice]] + outcomeScoring[outcome]


outcomeScoring = {
  'X' : 0, #lose
  'Y' : 3, #draw
  'Z' : 6  #win
  }
  

main()