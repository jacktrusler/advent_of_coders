<!-- Entries between SOLUTIONS and RESULTS tags are auto-generated -->

[![AoC](https://badgen.net/badge/AoC/2023/blue)](https://adventofcode.com/2023)
![Language](https://badgen.net/badge/Language/Python/blue)

# 🎄 Advent of Code 2023 🎄

## Solutions

<!--SOLUTIONS-->

[![Day](https://badgen.net/badge/01/%E2%98%85%E2%98%85/green)](#d01)
[![Day](https://badgen.net/badge/02/%E2%98%85%E2%98%85/green)](#d02)
[![Day](https://badgen.net/badge/03/%E2%98%86%E2%98%86/gray)](#d03)
[![Day](https://badgen.net/badge/04/%E2%98%86%E2%98%86/gray)](#d04)
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

