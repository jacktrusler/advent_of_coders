//! [Day 1](https://adventofcode.com/2021/day/1): Sonar sweep thingy.

pub fn parse_input(input: &str) -> Vec<usize> {
    input
        .split_whitespace()
        .filter_map(|s| s.parse::<usize>().ok())
        .collect()
}

pub fn sonar_sweep_1(depths: &[usize]) -> usize {
    depths.windows(2).filter(|w| w[0] < w[1]).count()
}

pub fn sonar_sweep_2(depths: &[usize]) -> usize {
    let windows = depths.windows(3).map(|w| w.iter().sum());
    sonar_sweep_1(&windows.collect::<Vec<_>>())
}
