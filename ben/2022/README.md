<!-- Entries between SOLUTIONS and RESULTS tags are auto-generated -->

[![AoC](https://badgen.net/badge/AoC/2022/blue)](https://adventofcode.com/2022)
![Language](https://badgen.net/badge/Language/Python/blue)

# 🎄 Advent of Code 2022 🎄

## Solutions

<!--SOLUTIONS-->

[![Day](https://badgen.net/badge/01/%E2%98%85%E2%98%85/green)](#d01)
[![Day](https://badgen.net/badge/02/%E2%98%85%E2%98%85/green)](#d02)
[![Day](https://badgen.net/badge/03/%E2%98%85%E2%98%85/green)](#d03)
[![Day](https://badgen.net/badge/04/%E2%98%85%E2%98%85/green)](#d04)
[![Day](https://badgen.net/badge/05/%E2%98%85%E2%98%85/green)](#d05)
[![Day](https://badgen.net/badge/06/%E2%98%85%E2%98%85/green)](#d06)
[![Day](https://badgen.net/badge/07/%E2%98%85%E2%98%85/green)](#d07)
[![Day](https://badgen.net/badge/08/%E2%98%85%E2%98%85/green)](#d08)
[![Day](https://badgen.net/badge/09/%E2%98%85%E2%98%85/green)](#d09)
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

For day two, we have to take a series of character inputs and use them to play Rock, Paper, Scissors. Each line gives two values: one is the opponent's choice ('A' for rock, 'B' for paper, 'C' for scissors), the other is our choice ('X' for rock, 'Y' for paper, 'Z' for scissors). We can represent this input as a list of tuples.

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

Runtime: 1.232 ms  

### Part One

Here we arrive at one of those advent of code days that is just totally broken by using sets. For those not in the know, a `set` is an unmutable collection of unique, unordered values. For instance, if you were to make a `set` out of this list: `[3, 5, 3, 1, 3]`, the `set` would contain the following values: `{1, 3, 5}`. The best way to think of a `set` visually is as a single circle in a larger venn diagram.

First thing's first though, let's read our input. Each line is a list of characters that are contained in one rucksack. We can make a list of lists where each inner list contains every item within the rucksack.

    rucksacks = [list(x) for x in aoc.read_lines()]

Then, we have to determine what the "priority" of each item is. `{'a'-'z': 1-26, 'A'-'Z': 27-52}`. We can iterate through the lowercase and uppercase letters using the `ascii_lowercase` and `ascii_uppercase` functions from the `string` library. The `enumerate` function will then let us loop through these while extracting both the current index and the current value.

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

Runtime: 1.313 ms  

### Part One

Today's problem asks us to essentially find the overlap between two ranges. On paper, this should be a slam dunk use of sets. However, on further thought, sets might not be ideal. While still a perfectly valid solution, creating a set out of each of these inputs involves creating the full ranges, which hurts us both in time and memory. Instead, we have all the information we need when parsing the lines. If we assume elf `a` and elf `b`, our input provides a list of `amin`, `amax`, `bmin`, and `bmax`

    def parse_line(line: str) -> tuple[int,int,int,int]:
        a, b = line.split(',')
        amin, amax = map(int, a.split('-'))
        bmin, bmax = map(int, b.split('-'))
        return amin, amax, bmin, bmax
    assignments = [parse_line(x) for x in aoc.read_lines()]

Our goal is then to find out if the range of `a` (`amin-amax`) contains the entire range of `b` (`bmin-bmax`) or vice versa:

    amin            amax        amin       amax
    |---------------|           |----------|
       |--------|               |---------------|
       bmin     bmax            bmin            bmax

As seen above, this occurs when both `amin <= bmin and amax >= bmax` or when `bmin <= amin and bmax >= amax`. We can simply compare the various min/max values to each other to determine this for each line.

    def contains(min_a: int, max_a: int, min_b: int, max_b: int) -> bool:
        return min_a <= min_b and max_a >= max_b or min_b <= min_a and max_b >= max_a

    part_one = len([x for x in assignments if contains(*x)])

### Part Two

For part two, we just need to see if there's any overlap between the two assignments. Instead of checking for when this is true, it's much easier to find when it is false.

    amin         amax
    |------------|
                    |------|
                    bmin   bmax

If `a` ends before `b` starts (or vice versa), then there is no overlap. The inverse of that will tell us when overlap occurs for a given line.

    def overlap(min_a: int, max_a: int, min_b: int, max_b: int) -> bool:
        return not (max_a < min_b or max_b < min_a)

    part_two = len([x for x in assignments if overlap(*x)])

Tada! Believe it or not, I found this solution to be about 4 times faster than the `set`-based solution, though both were more than sufficiently fast.

## <a name="d05"></a> Day 05: Supply Stacks

[Task description](https://adventofcode.com/2022/day/5) - [Complete solution](day05/supply_stacks.py) - [Back to top](#top)  

Runtime: 1.559 ms  

### Part One

Today's issue has us dealing with moving crates between a series of stacks. The first question we have to ask is "how do we want to represent the data?". Each movement will involve moving `n` crates from some stack `a` to some stack `b`. While my gut instinct was to use a series of `deque` objects, since this is just a series of LIFO stacks, the fact that we have to move multiple crates at once actually makes me rather use a series of lists. This is because there's no way to pop multiple values from a `deque` at the same time, whereas with lists, I can slice multiple values off at once. So we can represent our stacks of crates using this structure.

    Stacks = dict[int, list[str]]

With our data structure in place, let's read the input, which is split into two chunks: our initial state of stacks and the movements we need to perform. Let's start with the initial state.

        [D]        # <-- This is the final element of a stack
    [N] [C]    
    [Z] [M] [P]    # <-- This is the 0th element of a stack
     1   2   3     # <-- Last row is the ID of a given stack

Here we see how the input is structured. We want to look at it from the bottom-up to make our initial state of `Stacks`. Let's create a function that does that.

    def parse_state(state: str) -> Stacks:
        lines = state.splitlines()
        crates, stacks = lines[:-1], lines[-1]
        return {int(stack_no): [row[i] for row in reversed(crates) if row[i] != ' '] 
                for i, stack_no in enumerate(stacks) if stack_no != ' '}

    initial_state, movements = aoc.read_chunks()
    stacks = parse_state(initial_state)

The bottom line (`stacks`) contains our stack_ids and a bunch of spaces we don't care about. Meanwhile, every other line (`crates`) contains the letters of our crates and a bunch of other characters we don't care about. Notice that the letter of a crate is always in the same index as the stack id itself. If we enumerate over `stacks` (taking care to skip spaces), we are left with every index that contains the letters in that stack. Then we can loop backwards over `crates` and grab that index in each row (once again skipping blank lines).

With that out of the way, all that's left is to move the crates around. We can use regex to parse our movement lines, like so:

    m = re.match(r'move (\d+) from (\d+) to (\d+)', movement).groups()
    amount, start, end = int(m[0]), int(m[1]), int(m[2])

Once we have that, it's as simple as pulling `amount` number of crates from `start` stack and placing them into `end` stack. Be sure you remember to remove the crates from the `start` stack along the way.

    def move(stacks: Stacks, movement: str) -> Stacks:
        m = re.match(r'move (\d+) from (\d+) to (\d+)', movement).groups()
        amount, start, end = int(m[0]), int(m[1]), int(m[2])
        to_move = stacks[start][-amount:]        # Grab the crates that need moved
        stacks[start] = stacks[start][:-amount]  # Remove those crates from the start stack
        stacks[end].extend(reversed(to_move))    # Place them into the end stack
        return stacks

Finally, let's call this function once for each movement. The `reduce` function in the `functools` library helps a lot here. Given a function, an iterable, and an initial state, you can apply the function from left to right on the iterable and obtain the final value. For instance `reduce(lambda x,y: x*y, numbers, 1)` will multiply every value of `numbers` together, starting with the value 1.

    stacks = reduce(lambda x,y: move(x, y), movements.splitlines(), stacks)
    part_one = ''.join([q[-1] for q in stacks.values()])

### Part Two

Part two doesn't change things a whole lot for us. Instead of reversing the crates that are moved, we want to keep them in the same order. To do that, we can just edit our move function a little bit:

    def move(stacks: Stacks, movement: str, reverse: bool = True) -> Stacks:
        m = re.match(r'move (\d+) from (\d+) to (\d+)', movement).groups()
        amount, start, end = int(m[0]), int(m[1]), int(m[2])
        to_move = stacks[start][-amount:]
        stacks[start] = stacks[start][:-amount]
        stacks[end].extend(reversed(to_move) if reverse else to_move)
        return stacks

A new optional argument `reverse` was added. If `reverse` is `True`, we will reverse the moved crates (like in part 1). However, now we can pass `False` in, and it will give us our answer for part two.

    stacks = reduce(lambda x,y: move(x, y, reverse=False), movements.splitlines(), stacks)
    part_two = ''.join([q[-1] for q in stacks.values()])

If you're trying to do both parts in one script, it should be noted that our move function **mutates** our `Stacks` state. Because of this, you can't keep using the same state object for both parts, because the initial state will have changed after part one. We can use the `deepcopy` function from the `copy` module to copy the state of our `Stacks` object before we modify it.

    from copy import deepcopy

    stacks1 = deepcopy(stacks)
    stacks1 = reduce(lambda x,y: move(x, y), movements, stacks1)
    part_one = ''.join([q[-1] for q in stacks1.values()])

    stacks2 = deepcopy(stacks)
    stacks2 = reduce(lambda x,y: move(x, y, reverse=False), movements, stacks2)
    part_two = ''.join([q[-1] for q in stacks2.values()])

## <a name="d06"></a> Day 06: Tuning Trouble

[Task description](https://adventofcode.com/2022/day/6) - [Complete solution](day06/tuning_trouble.py) - [Back to top](#top)  

Runtime: 2.001 ms  

### Notes

...  

## <a name="d07"></a> Day 07: No Space Left On Device

[Task description](https://adventofcode.com/2022/day/7) - [Complete solution](day07/no_space_left_on_device.py) - [Back to top](#top)  

Runtime: 1.938 ms  

### Notes

...  

## <a name="d08"></a> Day 08: Treetop Tree House

[Task description](https://adventofcode.com/2022/day/8) - [Complete solution](day08/treetop_tree_house.py) - [Back to top](#top)  

Runtime: ...  

### Notes

...  

## <a name="d09"></a> Day 09: Rope Bridge

[Task description](https://adventofcode.com/2022/day/9) - [Complete solution](day09/rope_bridge.py) - [Back to top](#top)  

Runtime: ...  

### Notes

...  

