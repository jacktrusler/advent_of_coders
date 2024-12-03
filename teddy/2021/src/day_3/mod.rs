//! [Day 3](https://adventofcode.com/2021/day/3): Submarine power consumption.

use std::collections::HashMap;

pub fn parse_input(input: &str) -> Vec<u32> {
    input.chars().filter_map(|c| c.to_digit(10)).collect()
}

pub fn power_consumption_1(input: &[u32]) -> u32 {
    let (rows, cols) = (input.len() / 12, 12);
    let (gamma, epsilon) = transpose(input, rows, cols)
        .as_slice()
        .chunks_exact(rows)
        .map(|col| frequencies(col.iter().copied()))
        .fold(
            (String::with_capacity(cols), String::with_capacity(cols)),
            |(gamma, epsilon), freqs| {
                if freqs[&0] > freqs[&1] {
                    (gamma + "0", epsilon + "1")
                } else {
                    (gamma + "1", epsilon + "0")
                }
            },
        );

    u32::from_str_radix(&gamma, 2).unwrap() * u32::from_str_radix(&epsilon, 2).unwrap()
}

pub fn power_consumption_2(input: &[u32]) -> u32 {
    recurse(input, "gt", 0) * recurse(input, "le", 0)
}

fn transpose(list: &[u32], x: usize, y: usize) -> Vec<u32> {
    let mut transposed = Vec::with_capacity(x * y);
    for i in 0..y {
        for j in 0..x {
            transposed.push(list[j * y + i]);
        }
    }
    transposed
}

fn frequencies<T: Iterator<Item = u32>>(iter: T) -> HashMap<u32, u32> {
    iter.fold(HashMap::with_capacity(2), |mut freqs, n| {
        *freqs.entry(n).or_insert(0) += 1;
        freqs
    })
}

fn recurse(input: &[u32], op: &str, idx: usize) -> u32 {
    let rows = input.chunks_exact(12).map(|row| row[idx]);
    let freqs = frequencies(rows);

    let min_max = match op {
        "gt" => u32::from(freqs[&0] <= freqs[&1]),
        "le" => u32::from(freqs[&0] > freqs[&1]),
        _ => unreachable!(),
    };

    let filtered = input
        .chunks_exact(12)
        .filter(|row| row[idx] == min_max)
        .collect::<Vec<_>>();

    if filtered.len() == 1 {
        u32::from_str_radix(
            &filtered[0]
                .iter()
                .filter_map(|&d| char::from_digit(d, 10))
                .collect::<String>(),
            2,
        )
        .unwrap()
    } else {
        recurse(
            &filtered.into_iter().flatten().copied().collect::<Vec<_>>(),
            op,
            idx + 1,
        )
    }
}
