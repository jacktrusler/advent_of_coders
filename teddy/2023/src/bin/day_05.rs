use itertools::Itertools;
use rayon::prelude::*;

fn main() {
    let input = advent_of_code_2023::read_input!();
    let mut input = input.split("\n\n");
    let seeds = input
        .next()
        .map(|s| {
            s.split(':')
                .last()
                .map(|s| s.split(' ').flat_map(str::parse::<i64>))
                .unwrap()
                .collect::<Vec<_>>()
        })
        .unwrap();
    let maps = input
        .map(|s| {
            s.lines()
                .skip(1)
                .filter_map(|l| {
                    let (destination, source, len) =
                        l.split(' ').flat_map(str::parse::<i64>).next_tuple()?;
                    Some((source..source + len, destination - source))
                })
                .collect::<Vec<_>>()
        })
        .collect::<Vec<_>>();
    let in_range = |seed| {
        maps.iter().fold(seed, |seed, map| {
            if let Some((_, delta)) = map.iter().find(|(source, _)| source.contains(&seed)) {
                seed + delta
            } else {
                seed
            }
        })
    };
    let a = seeds.par_iter().copied().map(in_range).min().unwrap();
    let b = seeds
        .into_iter()
        .tuples()
        .map(|(a, b)| a..a + b)
        .par_bridge()
        .flat_map(std::iter::IntoIterator::into_iter)
        .map(in_range)
        .min()
        .unwrap();

    println!("{a}");
    println!("{b}");
}
