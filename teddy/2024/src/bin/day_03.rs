use regex::Regex;

fn main() {
    let input = advent_of_code_2024::read_input!();
    let re = Regex::new(r"(do)\(\)|(don't)\(\)|mul\((\d+),(\d+)\)").unwrap();
    let p1 = re.captures_iter(&input).fold(0, |acc, caps| {
        if let (Some(x), Some(y)) = (caps.get(3), caps.get(4)) {
            acc + (x.as_str().parse::<i32>().unwrap() * y.as_str().parse::<i32>().unwrap())
        } else {
            acc
        }
    });
    let (_, p2) = re
        .captures_iter(&input)
        .fold((true, 0), |(mut doit, acc), caps| {
            match (caps.get(1), caps.get(2), caps.get(3), caps.get(4)) {
                (Some(_), ..) => doit = true,
                (_, Some(_), ..) => doit = false,
                (.., Some(x), Some(y)) if doit => {
                    return (
                        doit,
                        acc + (x.as_str().parse::<i32>().unwrap()
                            * y.as_str().parse::<i32>().unwrap()),
                    );
                }
                _ => (),
            }
            (doit, acc)
        });

    println!("part 1: {p1}");
    println!("part 2: {p2}");
}
