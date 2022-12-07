def main():
  msg = open('./input.txt').read()
  elves = msg.split('\n\n')
  maxCals = 0
  for elf in elves:
    currentCals = sum(list(map(int,elf.split('\n'))))
    maxCals = max(currentCals,maxCals)
  print(f"The elf with the most calories has {maxCals} calories!")

main()