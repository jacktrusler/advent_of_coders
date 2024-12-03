use regex::Regex;

fn main() {
    let input = advent_of_code_2024::read_input!();
    let re = Regex::new(r"(do)\(\)|(don't)\(\)|mul\((\d+),(\d+)\)").unwrap();
    let (mut p1, mut p2, mut doit) = (0, 0, true);
    for caps in re.captures_iter(&input) {
        match (caps.get(1), caps.get(2), caps.get(3), caps.get(4)) {
            (Some(_), ..) => doit = true,
            (_, Some(_), ..) => doit = false,
            (.., Some(x), Some(y)) => {
                let p = x.as_str().parse::<i32>().unwrap() * y.as_str().parse::<i32>().unwrap();
                p1 += p;
                if doit {
                    p2 += p;
                }
            }
            _ => unreachable!(),
        }
    }

    println!("part 1: {p1}");
    println!("part 2: {p2}");
}
