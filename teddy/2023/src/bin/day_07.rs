use std::{borrow::Cow, cmp::Ordering, collections::HashMap};

use itertools::{Itertools, Position};

struct Hand {
    values: Box<[usize]>,
    counts: HashMap<char, usize>,
    bid: usize,
}

fn parse_line(line: &str, ord: &str) -> Option<Hand> {
    let (hand, bid) = line.split_ascii_whitespace().collect_tuple()?;
    Some(Hand {
        values: hand.chars().filter_map(|c| ord.find(c)).collect(),
        counts: hand.chars().counts(),
        bid: bid.parse().ok()?,
    })
}

fn counts(hand: &Hand) -> String {
    hand.counts.values().sorted_unstable().join("")
}

fn counts_value(counts: impl AsRef<str>) -> usize {
    match counts.as_ref() {
        "5" => 6,     // Five of a kind
        "14" => 5,    // Four of a kind
        "23" => 4,    // Full house
        "113" => 3,   // Three of a kind
        "122" => 2,   // Two Pair
        "1112" => 1,  // One Pair
        "11111" => 0, // High Card
        _ => unreachable!(),
    }
}

fn cmp(value: impl Fn(&Hand) -> usize) -> impl FnMut(&Hand, &Hand) -> Ordering {
    move |a: &Hand, b: &Hand| match value(a).cmp(&value(b)) {
        Ordering::Equal => {
            for i in 0..5 {
                match a.values[i].cmp(&b.values[i]) {
                    Ordering::Equal => continue,
                    ord => return ord,
                }
            }
            unreachable!();
        }
        ord => ord,
    }
}

fn winnings(input: &str, ord: &str, cmp: impl FnMut(&Hand, &Hand) -> Ordering) -> usize {
    input
        .lines()
        .filter_map(|l| parse_line(l, ord))
        .sorted_unstable_by(cmp)
        .enumerate()
        .map(|(i, Hand { bid, .. })| (i + 1) * bid)
        .sum()
}

fn main() {
    let input = advent_of_code_2023::read_input!();
    let a = winnings(
        &input,
        "23456789TJQKA",
        cmp(|hand| counts_value(counts(hand))),
    );
    let b = winnings(
        &input,
        "J23456789TQKA",
        cmp(|hand| {
            counts_value(hand.counts.get(&'J').map_or_else(
                || Cow::from(counts(hand)),
                |&n| {
                    if n == 5 {
                        Cow::from("5")
                    } else {
                        Cow::from(
                            hand.counts
                                .iter()
                                .filter_map(|(k, v)| (k != &'J').then_some(v))
                                .sorted_unstable()
                                .with_position()
                                .map(|(pos, val)| match pos {
                                    Position::Last | Position::Only => val + n,
                                    _ => *val,
                                })
                                .join(""),
                        )
                    }
                },
            ))
        }),
    );

    println!("{a}");
    println!("{b}");
}
