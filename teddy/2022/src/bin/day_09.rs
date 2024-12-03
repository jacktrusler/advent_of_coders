use std::collections::HashSet;

fn main() -> anyhow::Result<()> {
    let input = std::fs::read_to_string("2022/inputs/day_09.txt")?;
    let mut p1 = HashSet::new();
    let mut p2 = HashSet::new();
    let mut rope = [(0_i32, 0_i32); 10];

    for (dir, n) in input.lines().map(|l| l.split_once(' ').unwrap()) {
        let delta = match dir {
            "U" => (0, 1),
            "D" => (0, -1),
            "L" => (-1, 0),
            "R" => (1, 0),
            _ => unreachable!(),
        };

        for _ in 0..n.parse::<i32>()? {
            rope[0].0 += delta.0;
            rope[0].1 += delta.1;

            for t in 1..10 {
                let (head, tail) = (rope[t - 1], &mut rope[t]);
                if head.0.abs_diff(tail.0) > 1 || head.1.abs_diff(tail.1) > 1 {
                    tail.0 += (head.0 - tail.0).signum();
                    tail.1 += (head.1 - tail.1).signum();
                } else {
                    break;
                }
            }

            p1.insert(rope[1]);
            p2.insert(rope[9]);
        }
    }

    println!("{}, {}", p1.len(), p2.len());
    Ok(())
}
