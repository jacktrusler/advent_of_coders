def main():
  text = open('./rpsInput.txt').read()
  games = text.split('\n')
  total = 0
  for game in games:
    round = ''.join(game.split(' '))
    score = scoring[round]
    total += score
  print(f"The total score for all the round is {total}!")

scoring = {
  # A & X are Rock
  # B & Y are Paper
  # C & Z are Scissors
  'AY' : 8,
  'AX' : 4,
  'AZ' : 3,
  'BY' : 5,
  'BX' : 1,
  'BZ' : 9,
  'CY' : 2,
  'CX' : 7,
  'CZ' : 6
}
  

main()