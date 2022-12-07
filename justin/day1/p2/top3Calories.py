def main():
  msg = open('../p1/input.txt').read()
  elves = msg.split('\n\n')
  maxCals = []
  for elf in elves:
    currentCals = sum(list(map(int,elf.split('\n'))))
    if len(maxCals) < 3:
      maxCals.append(currentCals)
    elif currentCals > min(maxCals):
      maxCals[maxCals.index(min(maxCals))] = currentCals
  maxCals.sort(reverse=True)
  totalCals = sum(maxCals)
  print(f"The elves with the most calories have {maxCals[0]}, {maxCals[1]}, and {maxCals[2]} for a total of {totalCals} calories!")

main()