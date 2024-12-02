//! [Day 4](https://adventofcode.com/2021/day/4): Bingo.

pub fn parse_input(input: &str) -> (Vec<u32>, Vec<Vec<Vec<u32>>>) {
    let mut split = input.split("\n\n");
    let nums = split
        .next()
        .unwrap()
        .split(',')
        .filter_map(|n| n.parse::<u32>().ok());
    let boards = split.map(|board| {
        board
            .lines()
            .map(|line| {
                line.split_whitespace()
                    .filter_map(|n| n.parse::<u32>().ok())
                    .collect()
            })
            .collect()
    });
    (nums.collect(), boards.collect())
}

// [input | boards] =
//   File.read!("src/day_4/input.txt")
//   |> String.split("\n\n", trim: true)
//   |> Enum.map(&String.split(&1, ~r{[\n|,]}, trim: true))

// input = Stream.map(1..length(input), &Enum.take(input, &1)) |> Stream.take(-length(input) + 4)

// boards =
//   Stream.map(boards, fn board -> Enum.map(board, &String.split/1) end)
//   |> Enum.map(fn board -> {board, Enum.zip_with(board, & &1)} end)

// pub fn bingo_1() {}

// pub fn bingo_2() {}
