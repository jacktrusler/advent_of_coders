<!-- Entries between SOLUTIONS and RESULTS tags are auto-generated -->

[![AoC](https://badgen.net/badge/AoC/2022/blue)](https://adventofcode.com/2022)
![Language](https://badgen.net/badge/Language/Python/blue)

# 🎄 Advent of Code 2022 🎄

## Solutions

<!--SOLUTIONS-->

[![Day](https://badgen.net/badge/01/%E2%98%85%E2%98%85/green)](#d01)
[![Day](https://badgen.net/badge/02/%E2%98%85%E2%98%85/green)](#d02)
[![Day](https://badgen.net/badge/03/%E2%98%86%E2%98%86/green)](#d03)
[![Day](https://badgen.net/badge/04/%E2%98%86%E2%98%86/green)](#d04)
[![Day](https://badgen.net/badge/05/%E2%98%86%E2%98%86/gray)](#d05)
[![Day](https://badgen.net/badge/06/%E2%98%86%E2%98%86/gray)](#d06)
[![Day](https://badgen.net/badge/07/%E2%98%86%E2%98%86/gray)](#d07)
[![Day](https://badgen.net/badge/08/%E2%98%86%E2%98%86/gray)](#d08)
[![Day](https://badgen.net/badge/09/%E2%98%86%E2%98%86/gray)](#d09)
[![Day](https://badgen.net/badge/10/%E2%98%86%E2%98%86/gray)](#d10)
[![Day](https://badgen.net/badge/11/%E2%98%86%E2%98%86/gray)](#d11)
[![Day](https://badgen.net/badge/12/%E2%98%86%E2%98%86/gray)](#d12)
[![Day](https://badgen.net/badge/13/%E2%98%86%E2%98%86/gray)](#d13)
[![Day](https://badgen.net/badge/14/%E2%98%86%E2%98%86/gray)](#d14)
[![Day](https://badgen.net/badge/15/%E2%98%86%E2%98%86/gray)](#d15)
[![Day](https://badgen.net/badge/16/%E2%98%86%E2%98%86/gray)](#d16)
[![Day](https://badgen.net/badge/17/%E2%98%86%E2%98%86/gray)](#d17)
[![Day](https://badgen.net/badge/18/%E2%98%86%E2%98%86/gray)](#d18)
[![Day](https://badgen.net/badge/19/%E2%98%86%E2%98%86/gray)](#d19)
[![Day](https://badgen.net/badge/20/%E2%98%86%E2%98%86/gray)](#d20)
[![Day](https://badgen.net/badge/21/%E2%98%86%E2%98%86/gray)](#d21)
[![Day](https://badgen.net/badge/22/%E2%98%86%E2%98%86/gray)](#d22)
[![Day](https://badgen.net/badge/23/%E2%98%86%E2%98%86/gray)](#d23)
[![Day](https://badgen.net/badge/24/%E2%98%86%E2%98%86/gray)](#d24)
[![Day](https://badgen.net/badge/25/%E2%98%86%E2%98%86/gray)](#d25)

<!--/SOLUTIONS-->

_Click a badge to go to the specific day._


## <a name="d01"></a> Day 01: Calorie Counting

[Task description](https://adventofcode.com/2022/day/1) - [Complete solution](day01/calorie_counting.py) - [Back to top](#top)  
  
Runtime: 0.627 ms  

### Part One

This day is relatively simple overall, so we'll just take it slow and walk through every step.  

The main skill being tested here is honestly just our ability to read and organize the input. For this day, our input is split into "chunks", where each chunk is a list of calorie values held by each elf. These chunks are separated by a blank line, meaning we can find them by splitting the input on two newlines.  

    chunks = []
    with open('path/to/data.txt') as f:
        for chunk in f.read().split('\n\n'):
            chunks.append(chunk)

Now, to get the total number of calories held by each elf, we can loop over each chunk and sum the value in each line of the chunk. This means that we'll have to convert each value in the chunk to an int instead of a string. The simplest way to do this is by using the `map()` function to apply a function to every element of a given iterable. The built-in `sum()` function will then be super handy for adding them together, as it will add up all the values in a given iterable.  

    per_elf = []
    for chunk in chunks:
        values = map(int, chunk.splitlines())
        per_elf.append(sum(values))

However, this is a **lot** of looping. And if there's one thing python hates, it's looping. Using list comprehension, all of the above lines can be neatly combined:

    with open('path/to/data.txt') as f:
        per_elf = sum(map(int, x.splitlines())) for x in f.read().split('\n\n'))

Finally, the highest value that any elf has can be found using the built-in `max()` function.  

    most_calories = max(per_elf)

### Part Two

Part two asks us to find the total calories held by the three elves with the most calories. We can simply sort our list of calories per elf by using the `sorted()` method. Then, sum the last three elements in the list.

    top_three = sum(sorted(per_elf)[-3:])

Easy peasy!


## <a name="d02"></a> Day 02: Rock Paper Scissors

[Task description](https://adventofcode.com/2022/day/2) - [Complete solution](day02/rock_paper_scissors.py) - [Back to top](#top)  
  
Runtime: 0.867 ms  

### Part One

For part two, we have to take a series of character inputs and use them to play Rock, Paper, Scissors. Each line gives two values: one is the opponent's choice ('A' for rock, 'B' for paper, 'C' for scissors), the other is our choice ('X' for rock, 'Y' for paper, 'Z' for scissors). We can represent this input as a list of tuples.

    # Note: aoc.read_lines() is simply a fancy utility function that will split the input data by line
    rounds = [tuple(x.split(' ')) for x in aoc.read_lines()]

Each line represents one round of the game. The score for any given round is determined by two factors: the option we have chosen `{rock: 1 point, paper: 2 points, scissors: 3 points}` and the result of the round from our perspective `{win: 6 points, draw: 3 points, loss: 0 points}`. We can represent these values using enums.

    class Option(IntEnum):
        ROCK = 1
        PAPER = 2
        SCISSORS = 3

    class Outcome(IntEnum):
        WIN = 6
        DRAW = 3
        LOSS = 0

Finally, let's make a function that determines how many points we get for one round. Our choice is simply dependent on the letter given by the input, while the result is dependent on both our choice and the opponent's choice. A combination of switch statement and if statements can get us there pretty easily.

    def translator(opponent: str, me: str) -> int:
        match me:
            case 'X':
                choice = Option.ROCK
                result = Outcome.DRAW if opponent == 'A' else (Outcome.WIN if opponent == 'C' else Outcome.LOSS)
            case 'Y':
                choice = Option.PAPER
                result = Outcome.DRAW if opponent == 'B' else (Outcome.WIN if opponent == 'A' else Outcome.LOSS)
            case 'Z':
                choice = Option.SCISSORS
                result = Outcome.DRAW if opponent == 'C' else (Outcome.WIN if opponent == 'B' else Outcome.LOSS)
        return choice + result

Theoretically, we could just loop through our list of rounds, get the points of each round and sum it like so.

    part_one = sum([translator(x) for x in rounds])

But we're better than that! Because of the way the game works, there is a finite number of independent inputs to this function: `('A', 'X'), ('A', 'Y'), ('A', 'Z'), ('B', 'X'), etc, etc`. The output of this function will be the same for any given input. Likewise, our input of rounds is actually just a collection of each of these inputs n times. Instead of calling our function once for each round, why don't we call it once for each input? We can easily count the number of each input using the `Counter` object, which counts a given iterable into a dict of \[key,int\] values.

    rounds = Counter([tuple(x.split(' ')) for x in aoc.read_lines()])
    part_one = sum(v * translator(*k) for k, v in rounds.items())

### Part Two

This time, the `XYZ` inputs no longer represent the option we have chosen, but instead represent the outcome of the round. This is no big deal, all we have to do is slightly adjust our original function.

    def translator2(opponent: str, me: str) -> int:
        match me:
            case 'X':
                result = Outcome.LOSS
                choice = Option.ROCK if opponent == 'B' else (Option.PAPER if opponent == 'C' else Option.SCISSORS)
            case 'Y':
                result = Outcome.DRAW
                choice = Option.ROCK if opponent == 'A' else (Option.PAPER if opponent == 'B' else Option.SCISSORS)
            case 'Z':
                result = Outcome.WIN
                choice = Option.ROCK if opponent == 'C' else (Option.PAPER if opponent == 'A' else Option.SCISSORS)
        return choice + result

    part_two = sum(v * translator2(*k) for k, v in rounds.items())

Tada! Nice and simple, and with minimal looping!

## <a name="d03"></a> Day 03: Rucksack Reorganization

[Task description](https://adventofcode.com/2022/day/3) - [Complete solution](day03/rucksack_reorganization.py) - [Back to top](#top)  

Runtime: 1.367 ms  

### Part One

Here we arrive at one of those advent of code days that is just totally broken by using sets. For those not in the know, a `set` is an unmutable collection of unique, unordered values. For instance, if you were to make a `set` out of this list: `[3, 5, 3, 1, 3]`, the `set` would contain the following values: `{1, 3, 5}`. The best way to think a `set` visually is as a single circle in a larger venn diagram.

First thing's first though, let's read our input. Each line is a list of characters that are contained in one rucksack. We can make a list of lists where each inner list contains every item within the rucksack.

    rucksacks = [list(x) for x in aoc.read_lines()]

Then, we have to determine what the "priority" of each item is. `{'a'-'z': 1-26, 'A'-'Z': 27-52}`. We can iterate through the lowercase and uppercase letters using the `ascii_lowercase` and `ascii_uppercase` functions from the `string` library. The `enumerate` function will then let us loop through these while extracting both the current index, and the current value.

    priorities = {char: i+1 for i, char in enumerate(list(ascii_lowercase) + list(ascii_uppercase))}

Finally, we need a function that can find the item contained in both rucksack compartments. If we split the string in half, and change each half into a set, we can find the `intersection` of those sets to determine which item(s) is contained in both. The `intersection` of two sets can be found using the bitwise `&` operator

    def check_compartment(items: str) -> int:
        common_item = set(items[len(items)//2:]) & set(items[:len(items)//2])
        return list(common_item)[0]

    part_one = sum(priorities[check_compartment(x)] for x in rucksacks)

### Part Two

This time, we need to get every group of three rucksacks and find the common item between all of them. First, we'll need to have a function that can get that common item. Once again, we can use `intersection`. However, this time we'll call it in a different way.

    def check_group(sacks: list[str]) -> int:
        common_item = set.intersection(*map(set, sacks))
        return list(common_item)[0]

`map(set, sacks)` will convert all of our sacks (represented by lists of strings) into sets of strings instead. Then, we can use the `*` operator to unpack that list into the arguments of `set.intersection`. The result is our one common item.

Using the `range` function, we can easily step over our list of rucksacks, taking care to split them into groups of three. The first argument of range is the starting value of the iteration, the second is the ending value, and the third argument is the step -- the size of each jump in iteration. So `range(0, len(rucksacks), 3)` will iterate over the values `(0, 3, 6, 9, 12, ...)` all the way until the end of our rucksack list.

    sum(priorities[check_group(rucksacks[i:i+3])] for i in range(0, len(rucksacks), 3))

## <a name="d04"></a> Day 04: Camp Cleanup

[Task description](https://adventofcode.com/2022/day/4) - [Complete solution](day04/camp_cleanup.py) - [Back to top](#top)  

Runtime: 6.560 ms  

### Part One

Another day of advent of code, another day of sets. For this day, our input is a list of section IDs that each pair of elves is assigned to clean in the format `x1-x2,y1-y2`. We can use regex to pretty cleanly grab these values out of the line.

    m = tuple(map(int, re.match(r'(\d+)-(\d+),(\d+)-(\d+)', line).groups()))

Our goal is then to find out if the range of x (`x1-x2`) contains the entire range of y (`y1-y2`) or vice versa. This is another way of asking whether or not the set of x values is a subset of y values. This can be found using the `<=` or `>=` operators between two sets.

    def parse_line(line: str) -> tuple[set,set]:
        m = tuple(map(int, re.match(r'(\d+)-(\d+),(\d+)-(\d+)', line).groups()))
        return set(range(m[0], m[1]+1)), set(range(m[2], m[3]+1))

    assignments = [parse_line(x) for x in aoc.read_lines()]
    part_one = len([x for x in assignments if x[0] <= x[1] or x[1] <= x[0]])

### Part Two

For part two, we just need to see if there's any overlap between the two elves. This can be very easily found using the `intersection` of the two sets.

    part_two = len([x for x in assignments if x[0] & x[1]])

Tada! Not much else to say here, really.
