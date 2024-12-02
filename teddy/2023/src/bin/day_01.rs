use regex::Regex;

fn main() -> anyhow::Result<()> {
    let re_l = Regex::new(r"([1-9]|one|two|three|four|five|six|seven|eight|nine).*$")?;
    let re_r = Regex::new(r"^.*([1-9]|one|two|three|four|five|six|seven|eight|nine)")?;
    let (a, b) = advent_of_code_2023::read_input!()
        .lines()
        .filter_map(|l| {
            let mut digits1 = l.matches(|c: char| c.is_ascii_digit());
            let digits1_l = digits1.next()?;
            let digits1_r = digits1.next_back().unwrap_or(digits1_l);
            let digits2_l = &re_l.captures(l)?[1];
            let digits2_r = &re_r.captures(l)?[1];

            Some((
                digits1_l.parse::<i32>().ok()? * 10 + digits1_r.parse::<i32>().ok()?,
                parse(digits2_l) * 10 + parse(digits2_r),
            ))
        })
        .fold((0, 0), |(a, b), (n1, n2)| (a + n1, b + n2));

    println!("part 1: {a}");
    println!("part 2: {b}");

    Ok(())
}

fn parse(s: &str) -> i32 {
    match s {
        "one" | "1" => 1,
        "two" | "2" => 2,
        "three" | "3" => 3,
        "four" | "4" => 4,
        "five" | "5" => 5,
        "six" | "6" => 6,
        "seven" | "7" => 7,
        "eight" | "8" => 8,
        "nine" | "9" => 9,
        _ => unreachable!(),
    }
}
