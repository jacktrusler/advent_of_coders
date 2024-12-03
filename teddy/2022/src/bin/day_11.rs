// struct Monkey {
//     items: Vec<u64>,
//     op: Op,
//     test: u64,
//     next: Box<Monkey>,
//     prev: Box<Monkey>,
// }

// #[derive(Clone, Copy)]
// enum Op {
//     Add(u64),
//     Mul(u64),
//     Double,
//     Square,
// }

fn main() -> anyhow::Result<()> {
    let _input = std::fs::read_to_string("2022/inputs/day_11.txt")?;
    // let monkeys: Vec<i32> = vec![];
    // let groups = input.split("\n\n").map(|g| {
    //     let mut lines = g.lines();
    //     let items = get_digits(&mut lines);
    //     // let op = lines.
    //     let test = get_digits(&mut lines);
    //     let (if_true, if_false) = (get_digits(&mut lines), get_digits(&mut lines));
    // });

    // println!("{p1} {p2}");
    Ok(())
}

// fn get_digits<'a, I: Iterator<Item = &'a str>>(lines: &mut I) -> Vec<u64> {
//     lines
//         .next()
//         .unwrap()
//         .split_ascii_whitespace()
//         .map(|s| s.chars().filter(char::is_ascii_digit).collect::<String>())
//         .flat_map(|s| s.parse::<u64>())
//         .collect()
// }
