use std::{cmp::Ordering, collections::HashMap};

fn main() {
    let input = advent_of_code_2024::read_input!();
    let (ordering, mut pages) = input
        .split_once("\n\n")
        .map(|(ordering, pages)| {
            (
                ordering.lines().filter_map(|l| l.split_once('|')).fold(
                    HashMap::<_, Vec<_>>::new(),
                    |mut acc, (k, v)| {
                        acc.entry(k)
                            .and_modify(|e| e.push(v))
                            .or_insert_with(|| vec![v]);
                        acc
                    },
                ),
                pages
                    .lines()
                    .map(|l| l.split(',').collect::<Box<[_]>>())
                    .collect::<Box<_>>(),
            )
        })
        .unwrap();

    let (mut p1, mut p2) = (vec![], vec![]);
    for l in &mut pages {
        if l.iter().enumerate().all(|(i, &p)| {
            ordering
                .get(p)
                .unwrap()
                .iter()
                .filter(|&v| l.contains(v))
                .all(|v| l.iter().position(|p| p == v).unwrap() > i)
        }) {
            p1.push(str::parse::<i32>(l[l.len() / 2]).unwrap());
        } else {
            l.sort_unstable_by(|&a, &b| {
                if ordering.get(a).unwrap().contains(&b) {
                    Ordering::Less
                } else if ordering.get(b).unwrap().contains(&a) {
                    Ordering::Greater
                } else {
                    Ordering::Equal
                }
            });
            p2.push(str::parse::<i32>(l[l.len() / 2]).unwrap());
        }
    }

    println!("part 1: {}", p1.iter().sum::<i32>());
    println!("part 2: {}", p2.iter().sum::<i32>());
}
