fn main() -> anyhow::Result<()> {
    let mut elves = std::fs::read_to_string("2022/inputs/day_01.txt")?
        .split("\n\n")
        .map(|elf| elf.split('\n').flat_map(str::parse::<i32>).sum::<i32>())
        .collect::<Vec<_>>();
    elves.select_nth_unstable_by(2, |a, b| b.cmp(a));

    println!("{} {}", elves[0], elves[..3].iter().sum::<i32>());
    Ok(())
}
