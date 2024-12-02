use itertools::Itertools;

fn main() {
    let input = advent_of_code_2023::read_input!()
        .lines()
        .map(|l| {
            let l = l
                .split_ascii_whitespace()
                .flat_map(str::parse::<i32>)
                .collect::<Box<_>>();
            std::iter::successors(Some(l), |l| {
                (!l.iter().all(|n| n == &0)).then_some(
                    l.iter()
                        .tuple_windows::<(_, _)>()
                        .map(|(a, b)| b - a)
                        .collect(),
                )
            })
            .collect::<Box<_>>()
        })
        .collect::<Box<_>>();
    let a = input
        .iter()
        .map(|l| l.iter().filter_map(|l| l.last()).sum::<i32>())
        .sum::<i32>();
    let b = input
        .iter()
        .map(|l| {
            l.iter()
                .filter_map(|l| l.first())
                .rev()
                .fold(0, |acc, n| n - acc)
        })
        .sum::<i32>();

    println!("{a}");
    println!("{b}");
}
