use nom::{
    IResult,
    bytes::complete::tag,
    character::complete::{i32, multispace1},
    combinator::opt,
    multi::many1,
    sequence::{terminated, tuple},
};

fn main() {
    let input = advent_of_code_2023::read_input!();
    let mut copies = vec![1; input.lines().count()];

    let a = input
        .lines()
        .filter_map(|l| {
            parse_line(l)
                .ok()
                .map(|(_, (winning, numbers))| (winning, numbers))
        })
        .enumerate()
        .fold(0, |a, (i, (winning, numbers))| {
            let n_wins = numbers.iter().filter(|n| winning.contains(n)).count();
            let curr = copies[i];

            for copy in &mut copies[i + 1..=i + n_wins] {
                *copy += curr;
            }

            a + n_wins.checked_sub(1).map_or(0, |n| 2_i32.pow(n as u32))
        });
    let b = copies.iter().sum::<i32>();

    println!("{a}");
    println!("{b}");
}

fn parse_line(s: &str) -> IResult<&str, (Vec<i32>, Vec<i32>)> {
    let tag_space = |s| terminated(tag(s), multispace1);
    let (s, _) = tuple((tag_space("Card"), i32, tag_space(":")))(s)?;
    let (s, winning) = terminated(many1(terminated(i32, multispace1)), tag_space("|"))(s)?;
    let (s, numbers) = many1(terminated(i32, opt(multispace1)))(s)?;
    Ok((s, (winning, numbers)))
}
