use nom::{
    IResult,
    bytes::complete::tag,
    character::complete::alpha1,
    sequence::{delimited, terminated, tuple},
};

enum Direction {
    L,
    R,
}

struct Node<'a> {
    l: &'a str,
    r: &'a str,
}

fn parse_line(s: &str) -> IResult<&str, (&str, Node<'_>)> {
    let (s, name) = terminated(alpha1, tag(" = "))(s)?;
    let (s, (l, _, r)) = delimited(tag("("), tuple((alpha1, tag(", "), alpha1)), tag(")"))(s)?;
    Ok((s, (name, Node { l, r })))
}

fn lcm(a: usize, b: usize) -> usize {
    a * b / gcd(a, b)
}

fn gcd(a: usize, b: usize) -> usize {
    if b == 0 { a } else { gcd(b, a % b) }
}

fn main() {
    let input = advent_of_code_2023::read_input!();
    let mut input = input.lines();
    let (instructions, nodes) = (
        input
            .next()
            .unwrap()
            .chars()
            .map(|c| match c {
                'L' => Direction::L,
                'R' => Direction::R,
                _ => unreachable!(),
            })
            .collect::<Box<_>>(),
        input
            .flat_map(parse_line)
            .map(|(_, parsed)| parsed)
            .collect::<std::collections::HashMap<_, _>>(),
    );

    let (mut a, mut node) = (0, "AAA");
    while node != "ZZZ" {
        node = match instructions[a % instructions.len()] {
            Direction::L => nodes[node].l,
            Direction::R => nodes[node].r,
        };
        a += 1;
    }

    let b = nodes
        .keys()
        .copied()
        .filter(|k| k.ends_with('A'))
        .fold(vec![], |mut acc, node| {
            let mut node = node;
            let mut cycle = 0;
            for (i, dir) in instructions.iter().cycle().enumerate() {
                node = match dir {
                    Direction::L => nodes[node].l,
                    Direction::R => nodes[node].r,
                };
                if node.ends_with('Z') {
                    if cycle == 0 {
                        cycle = i;
                    } else {
                        cycle = i - cycle;
                        break;
                    }
                }
            }
            acc.push(cycle);
            acc
        })
        .into_iter()
        .fold(1, lcm);

    println!("{a}");
    println!("{b}");
}
