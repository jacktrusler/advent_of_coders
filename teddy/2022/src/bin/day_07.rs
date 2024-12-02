fn main() -> anyhow::Result<()> {
    let input = std::fs::read_to_string("inputs/day_07.txt")?;
    let mut dirs = vec![];
    let mut sizes = std::collections::HashMap::<Vec<&str>, u32>::new();

    for line in input
        .lines()
        .map(str::split_ascii_whitespace)
        .map(std::iter::Iterator::collect::<Vec<_>>)
    {
        match *line.as_slice() {
            ["$", "ls"] | ["dir", _] => (),
            ["$", "cd", ".."] => {
                dirs.pop();
            }
            ["$", "cd", dir] => dirs.push(dir),
            [size, _] => {
                for dir in dirs.iter().enumerate().map(|(i, &dir)| {
                    std::iter::once(dir)
                        .chain(dirs.iter().cloned().skip(1).take(i))
                        .collect()
                }) {
                    *sizes.entry(dir).or_default() += size.parse::<u32>()?;
                }
            }
            _ => unreachable!(),
        }
    }

    let p1 = sizes.values().filter(|&size| *size <= 100_000).sum::<u32>();
    let p2 = sizes
        .values()
        .filter(|&size| *size >= sizes[&vec!["/"]] - 40_000_000)
        .min()
        .unwrap();

    println!("{p1} {p2}");
    Ok(())
}
