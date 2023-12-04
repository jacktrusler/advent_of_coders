<!-- Entries between SOLUTIONS and RESULTS tags are auto-generated -->

[![AoC](https://badgen.net/badge/AoC/2023/blue)](https://adventofcode.com/2023)
![Language](https://badgen.net/badge/Language/Python/blue)

# 🎄 Advent of Code 2023 🎄

## Solutions

<!--SOLUTIONS-->

[![Day](https://badgen.net/badge/01/%E2%98%85%E2%98%85/green)](#d01)
[![Day](https://badgen.net/badge/02/%E2%98%85%E2%98%85/green)](#d02)
[![Day](https://badgen.net/badge/03/%E2%98%85%E2%98%85/green)](#d03)
[![Day](https://badgen.net/badge/04/%E2%98%85%E2%98%85/green)](#d04)
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

_Click a badge to go to the specific day._

ic day._

## <a name="d01"></a> Day 01: Trebuchet

[Task description](https://adventofcode.com/2023/day/1) - [Complete solution](day01/trebuchet.py) - [Back to top](#top)  

Runtime: 4.486 ms  

### Part One

A new December begins, and so does a new advent of code! Yippee! Looks like we get the pleasure of starting this year off with some super-duper string manipulation. Always fun.

We start with a list of strings that contain digits within them, like `pqr3stu8vwx`. We must obtain the first and last digit of each string and combine them into one two-digit number--in this case, `38`. The most sensible way to do this is to use our good friend, the regular expression. We could look over each line, finding all digits `(?=(\d))`. Then, simply grab the first and last (which could be the same with only one match) and convert them to a two-digit int. Let's make a function that can do just that.

```python
def pull_digits(line: str) -> int:
    pattern = fr'(?=(\d))'
    matches = re.findall(pattern, line)
    first, last = matches[0], matches[-1]
    return int(f'{first}{last}')

calibrations = aoc.read_data()
part_one = sum(pull_digits(x) for x in calibrations.splitlines())
```

Tada! Not the fastest solution, but it's simple enough. However, I'm not incredibly satisfied with it. Running an individual regular expression over every line doesn't feel very great (and is definitely slow). It'd be much more preferable to run the regex over the entirety of the data and pick it apart after. Let's try that instead.

```python
def pull_digits(calibrations: str) -> Generator[int]:
    matches = re.findall(fr'(?=(\n|\d))', calibrations)
    for key, group in itertools.groupby(matches, lambda x: x == '\n'):
        if key:
            continue
        group = list(group)
        yield int(f'{group[0]}{group[-1]}')

calibrations = aoc.read_data()
part_one = sum(pull_digits(calibrations))
```

This feels much more smooth. We've changed the function to accept the entirety of the data instead of one line. Then we edit our regular expression to match digits and newlines. We can then group our resulting matches by the newlines to get the results for each individual line. Only one loop required, and only one regular expression to parse.

### Part Two

For part two, we are told that the strings also contain the literal words for digits (i.e. "one", "two", or "three"). These strings can also count as digits. Well let's start by defining a map from word to digit:

```python
DIGIT_STRINGS = {
    'zero': '0',
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9'
}
```

Next, we have to update our regular expression pattern to also check for these words. This would require a final product of `(?=(\n|\d|one|two|three|etc))`. Finally, we'll have to adjust our existing function to both accept a pattern as a parameter, and to replace any "digit word" matches with their appropriate value.

```python
def pull_digits(calibrations: str, pattern: str) -> Generator[int]:
    matches = re.findall(pattern, calibrations)
    for key, group in itertools.groupby(matches, lambda x: x == '\n'):
        if key:
            continue
        group = list(group)
        first = DIGIT_STRINGS.get(group[0], group[0])
        last = DIGIT_STRINGS.get(group[-1], group[-1])
        yield int(f'{first}{last}')

pattern2 = fr'(?=(\n|\d|{"|".join(list(DIGIT_STRINGS.keys()))}))'
yield sum(pull_digits(calibrations, pattern2))
```

## <a name="d02"></a> Day 02: Cube Conundrum

[Task description](https://adventofcode.com/2023/day/2) - [Complete solution](day02/cube_conundrum.py) - [Back to top](#top)  

Runtime: 0.924 ms  

### Part One

For part two, we are tasked with playing a very boring sounding game with our elf friend--he will repeatedly grab from a bag a handful of random cubes, put them back in the bag, and then repeat a few times. Then for some reason, he will change the number of cubes in the bag in between games, and we'll play again. In doing so, we can gather data from the random pulls regarding how many total cubes of each color are in the bag for each game.

Long story short, this is yet another string manipulation puzzle. We're given a string of the following format and tasked with finding out whether or not that particular game could be played with only `12 red cubes, 13 green cubes and 14 blue cubes`:

    Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red

There's a lot of numbers and words in this string, but you'd be surprised at how little of it we actually need when it comes down to it. First, we need the game number (`4` in this case). However, because the game numbers move up in chronological order, we really don't need to pull it from the string--we can just assume it.

Next, we need the largest number of each cube color that appeared in this game. In this case, it would be `14 red cubes, 3 green cubes, and 15 blue cubes`. The rest of the numbers do not make any impact on this. Because of this, we can actually make our string manipulation a little easier: let's just ignore everything after the `:`, and then ignore every `,` and `;`. This will leave us with a string like so:

    1 green 3 red 6 blue 3 green 6 red 3 green 15 blue 14 red

We could then split this string by spaces and loop through pretty smoothly.

```python
for i, game_log in enumerate(aoc.read_lines(), start=1):
    game_log = game_log.split(': ')[1].replace(',', '').replace(';', '').split(' ')
```

Next, it would really help if we could iterate over two elements at once, so that we could get `(1, green), (3, red), (6, blue), ...`. Let's make a quick function to help with that.

```python
def pairwise(iterable):
    a = iter(iterable)
    return zip(a, a)
```

We can throw that into a loop in our main block of code. While we're at it, we'll need somewhere to sort and store the cube counts. Let's grab a default dictionary with `set` type:

```python
for i, game_log in enumerate(aoc.read_lines(), start=1):
    cube_counts = defaultdict(set)
    game_log = game_log.split(': ')[1].replace(',', '').replace(';', '').split(' ')
    
    for amount, color in pairwise(game_log):
        cube_counts[color].add(int(amount))
```

Lastly, all we really need from the information we've gathered it the max count of each cube color. We can then compare that to the test values mentioned above. Let's put it all together:

```python
TEST_CUBES = {
    'red': 12,
    'green': 13,
    'blue': 14
}

part_one = 0
for i, game_log in enumerate(aoc.read_lines(), start=1):
    cube_counts = defaultdict(set)
    game_log = game_log.split(': ')[1].replace(',', '').replace(';', '').split(' ')
    
    for amount, color in pairwise(game_log):
        cube_counts[color].add(int(amount))
    max_cubes = {k: max(v) for k, v in cube_counts.items()}

    if all(v <= TEST_CUBES[k] for k, v in max_cubes.items()):
        part_one += i
```

## Part Two

Part two doesn't really change a whole lot. Instead of comparing against a test game, we need to calculate the "power" of a set of cubes by getting the product of the max number of each cube color. Luckily, we already have all the information needed for this. We just have to throw a quick extra line in.

```python
part_one, part_two = 0, 0
for i, game_log in enumerate(aoc.read_lines(), start=1):
    cube_counts = defaultdict(set)
    game_log = game_log.split(': ')[1].replace(',', '').replace(';', '').split(' ')
    
    for amount, color in pairwise(game_log):
        cube_counts[color].add(int(amount))
    max_cubes = {k: max(v) for k, v in cube_counts.items()}

    if all(v <= TEST_CUBES[k] for k, v in max_cubes.items()):
        valid_game_total += i
    power += reduce(lambda x,y: x*y, max_cubes.values())
```

...  

## <a name="d03"></a> Day 03: Gear Ratios

[Task description](https://adventofcode.com/2023/day/3) - [Complete solution](day03/gear_ratios.py) - [Back to top](#top)  

Runtime: 4.809 ms (in office)  

### Part One

Today's test has us searching over a grid of characters in an attempt to find `part numbers`. These can be identified as any number that is adjacent to a non-period, non-digit symbol. Adjacencies can include diagonal. In the example below, the part numbers have been highlighted.

<img src="day03/img/part-numbers.png" width="15%"/>

Right away, we can run into a few traps here. It might make sense to approach this as a grid. This would even allow us to get into some sneaky numpy shenanigans that could ease the adjacency detection. However, if we were to take this approach, we would have a hard time getting the entirety of a part number. For example, the part number `617` is adjacent to a `*` symbol. We could pretty easily identify that the `7` is adjacent to the `*`, but to then get the entire number of `617` would be a lot of extra work.

However, if we approach this only as a block of text, it's going to be very hard to discern what it means to be adjacent. We still need some sense of location, which means that the concept of a grid is still useful. Maybe we can use both ideas! Let's start with the whole numbers and try to identify which ones are part numbers. We can do this using (once again) regular expressions.

```python
schematic = aoc.read_data()
for _match in re.finditer(r'(\d+)', schematic):
    val = _match.group()
```

Using re.finditer, we can iterate over each whole digit within the entire block of text. The `_match` object stores both the start of the match and its value. Using the start of the match, we can determine the `(x, y)` location of the number in the corresponding grid.

```python
schematic = aoc.read_data()
schematic_grid = schematic.splitlines()
line_length = len(schematic_grid[0]) + 1

for _match in re.finditer(r'(\d+)', schematic):
    y, x = divmod(_match.start(), line_length)
    val = _match.group()
```

Next, we need to check every point adjacent to the number. Because the number could be of any digit length, we have to use the length of the match to determine how wide of an area to search. In the example below, for part number `633`, we have to check all of the highlighted points. This part number starts at `(6, 2)`, and so we'll need to check every point within `y-range (1, 3)` and `x-range (5, 9)`.

<img src="day03/img/adjacent.png" width="15%"/>

With that in mind, we can use a combination of `itertools.product` and `range` along with the information we've already gathered to easily iterate over all of these points.

```python
schematic = aoc.read_data()
schematic_grid = schematic.splitlines()
line_length = len(schematic_grid[0]) + 1

for _match in re.finditer(r'(\d+)', schematic):
    y, x = divmod(_match.start(), line_length)
    val = _match.group()
    for adj_y, adj_x in itertools.product(range(y-1, y+2), range(x-1, x+len(val)+1)):
        try:
            adj_val = schematic_grid[adj_y][adj_x]
        except IndexError:
            continue
```

Finally, we just need to check if any of those adjacent points contain a symbol of interest. Because we don't explicitly know which symbols we're looking for, it will be easier to check which symbols *don't* interest us.

```python
schematic = aoc.read_data()
schematic_grid = schematic.splitlines()
line_length = len(schematic_grid[0]) + 1

non_symbols = {str(n) for n in range(10)} | {"."}

part_total = 0
for _match in re.finditer(r'(\d+)', schematic):
    y, x = divmod(_match.start(), line_length)
    val = _match.group()
    for adj_y, adj_x in itertools.product(range(y-1, y+2), range(x-1, x+len(val)+1)):
        try:
            adj_val = schematic_grid[adj_y][adj_x]
        except IndexError:
            continue

        if adj_val not in non_symbols:
            part_total += int(val)
```

### Part Two

Part two has us instead checking for `gears`. A gear is defined as any `*` symbol that is adjacent to **exactly** two part numbers. Immediately, you may try to find these by searching the string for that symbol and searching its adjacent points for digits. However, you quickly run into an issue doing this.

In the example below, there are three `*` symbols that could be potential gears. Looking at the middle one, it's pretty easy to identify that it is **not** a gear, due to the fact that there is only one digit adjacent to it. However, the other two (both of which **are** in fact gears), have three digits adjacent to them. It's very difficult in the program to discern which of these digits come from the same part numbers.

<img src="day03/img/gears.png" width="15%"/>

Instead of approaching it that way, let's modify our existing code to store a map of `*` symbols to lists of adjacent part numbers. Whenever we find a `*` in the adjacent points of a part number, we will store the part number in this dictionary, like so:

```python
schematic = aoc.read_data()
schematic_grid = schematic.splitlines()
line_length = len(schematic_grid[0]) + 1

non_symbols = {str(n) for n in range(10)} | {"."}
gear_values = defaultdict(list)

for _match in re.finditer(r'(\d+)', schematic):
    y, x = divmod(_match.start(), line_length)
    val = _match.group()
    for adj_y, adj_x in itertools.product(range(y-1, y+2), range(x-1, x+len(val)+1)):
        try:
            adj_val = schematic_grid[adj_y][adj_x]
        except IndexError:
            continue

        if adj_val not in non_symbols:
            # When a gear is found, add to the gear_values dictonary
            if adj_val == '*':
                gear_values[(adj_y, adj_x)].append(int(val))
```

Once the loop has completed, we can check which gears are valid by checking the length of the list held by the dictionary.

```python
gear_ratios = sum(v[0] * v[1] for v in gear_values.values() if len(v) == 2)
```

...  

## <a name="d04"></a> Day 04: Scratchcards

[Task description](https://adventofcode.com/2023/day/4) - [Complete solution](day04/scratchcards.py) - [Back to top](#top)  

Runtime: 2.306 ms (in office)  

### Part One

Day 4 is a little sigh of relief after a slightly more difficult day 3. Given a set of lottery cards, we have to determine which ones are winners. Each card has two sets of numbers: the first are the winning numbers, and the second are numbers we have, as shown below.

    Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53

Thanks to the wonders of `sets`, this is a fairly easy thing to accomplish in python. If we can get the two groups of numbers into their own sets, the `union` of these sets would include only the numbers that appear in **both** sets. The union of two sets can be found using the `&` operator.

<img src="day04/img/union.png" width="70%"/>

With this in mind, let's make a function that can parse the input and create a union of the two sets of numbers.

```python
def matches(card_str: str) -> set[int]:
    winning, mine = card_str.split(': ')[1].split(' | ')
    winning = {int(x) for x in winning.strip().split()}
    mine = {int(x) for x in mine.strip().split()}
    return winning & mine
```

With this, we can now iterate through each card and calculate its score. The score doubles for each match, starting with 1 point for 1 match. Thus, it has the following trend:

| Matches | Score |
| ------- | ----- |
|       0 |     0 |
|       1 |     1 |
|       2 |     2 |
|       3 |     4 |
|       4 |     8 |

With this in mind, we can create a score function of $score = 2 ^ {matches - 1}$, taking note that the score is `0` when the number of matches is zero. We can use an if check to ensure that there actually are matches before adding to the score in any way.

```python
cards = aoc.read_lines()

score = 0
for i, card in enumerate(cards, start=1):
    if num_matches := len(matches(card)):
        score += 2 ** (num_matches - 1)
```

### Part Two

With part two, the rules change slightly. When we win a card, we instead gain copies of the next `x` cards, where `x` is the number of matches. So, if `Card 3` has 3 matches, we would gain a copy of `Cards 4, 5, and 6`. Where things get a little tricky is that if we have multiple copies of a card, each of the copies will produce their own copies. So if we had 4 copies of `Card 4`, and it has 2 matches, we would get 4 copies each of `Cards 5 and 6`.

This shouldn't complicate things too much. Because `Card x` will only add cards for values higher than `x`, we can still iterate through our cards in numeric order. We'll need a dictionary of how many copies of each card we have, starting with 1 of each. Then, on our winning cards (where there are any matches at all), we'll simply add values to this dictionary equal to the number of copies of the current card. The last thing we need to make sure we check for is that we don't add any copies of cards past the max number of cards.

```python
cards = aoc.read_lines()

copies = {x: 1 for x in range(1, len(cards) + 1)}
for i, card in enumerate(cards, start=1):
    if num_matches := len(matches(card)):
        top_card = min(len(cards), i + num_matches)
        for new_copy in range(i + 1, top_card + 1):
            copies[new_copy] += copies[i]
total_copies = sum(copies.values())
```

...  

