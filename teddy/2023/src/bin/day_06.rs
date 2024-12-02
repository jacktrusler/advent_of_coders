fn main() -> anyhow::Result<()> {
    let input = advent_of_code_2023::read_input!();
    let input = input
        .lines()
        .map(|l| {
            l.split(':')
                .last()
                .map(|s| s.split(' ').collect::<Vec<_>>())
                .unwrap()
        })
        .collect::<Vec<_>>();
    let beat_record = |(time, record)| (1..time).filter(|t| (time - t) * t > record).count();
    let a = input[0]
        .iter()
        .copied()
        .flat_map(str::parse::<u64>)
        .zip(input[1].iter().copied().flat_map(str::parse::<u64>))
        .map(beat_record)
        .product::<usize>();
    let b_time = input[0].join("").parse::<u64>()?;
    let b_record = input[1].join("").parse::<u64>()?;
    let b = beat_record((b_time, b_record));

    println!("{a}");
    println!("{b}");

    Ok(())
}
