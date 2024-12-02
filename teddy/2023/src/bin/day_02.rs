use nom::{
    branch::alt,
    bytes::complete::tag,
    character::complete::{i32, u8},
    combinator::opt,
    multi::{fold_many1, many1},
    sequence::{pair, terminated, tuple},
    IResult,
};

struct Rgb {
    r: u8,
    g: u8,
    b: u8,
}

impl Rgb {
    const fn new() -> Self {
        Self { r: 0, g: 0, b: 0 }
    }

    const fn from(r: u8, g: u8, b: u8) -> Self {
        Self { r, g, b }
    }
}

struct Game {
    n: i32,
    sets: Vec<Rgb>,
}

fn main() {
    let input = advent_of_code_2023::read_input!();
    let rules_1 = Rgb::from(12, 13, 14);

    let (a, b) = input
        .lines()
        .filter_map(|l| parse_game(l).ok().map(|(_, game)| game))
        .fold((0, 0), |(a, b), Game { mut n, sets }| {
            let max = sets.into_iter().fold(Rgb::new(), |mut max, set| {
                if set.r > rules_1.r || set.g > rules_1.g || set.b > rules_1.b {
                    n = 0;
                }

                max.r = max.r.max(set.r);
                max.g = max.g.max(set.g);
                max.b = max.b.max(set.b);

                max
            });

            let power = i32::from(max.r) * i32::from(max.g) * i32::from(max.b);
            (a + n, b + power)
        });

    println!("part 1: {a}");
    println!("part 2: {b}");
}

fn parse_game(s: &str) -> IResult<&str, Game> {
    let (s, (_, n, _)) = tuple((tag("Game "), i32, tag(": ")))(s)?;
    let color = terminated(u8, tag(" "));
    let color = pair(color, alt((tag("red"), tag("green"), tag("blue"))));
    let color = terminated(color, opt(tag(", ")));
    let set = terminated(fold_many1(color, Rgb::new, parse_set), opt(tag("; ")));
    let (s, sets) = many1(set)(s)?;

    Ok((s, Game { n, sets }))
}

fn parse_set(mut rgb: Rgb, color: (u8, &str)) -> Rgb {
    match color {
        (n, "red") => rgb.r = n,
        (n, "green") => rgb.g = n,
        (n, "blue") => rgb.b = n,
        _ => (),
    }

    rgb
}
