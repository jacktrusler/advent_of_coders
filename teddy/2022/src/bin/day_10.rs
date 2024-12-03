fn main() -> anyhow::Result<()> {
    let input = std::fs::read_to_string("2022/inputs/day_10.txt")?;
    let (mut x, mut cycle) = (1, 0_i32);
    let (mut p1, mut p2) = (0, String::new());

    for line in input
        .lines()
        .map(str::split_ascii_whitespace)
        .map(Iterator::collect::<Vec<_>>)
    {
        let (cycles, v) = match *line {
            ["noop"] => (1, 0),
            ["addx", v] => (2, v.parse()?),
            _ => unreachable!(),
        };

        for _ in 0..cycles {
            let lit = (cycle % 40).abs_diff(x) <= 1;
            cycle += 1;
            p1 += if cycle % 40 == 20 { cycle * x } else { 0 };
            p2.push(if lit { '#' } else { '.' });
            if cycle % 40 == 0 {
                p2.push('\n');
            }
        }

        x += v;
    }

    println!("{p1}\n{p2}");
    Ok(())
}
