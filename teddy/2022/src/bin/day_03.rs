fn main() -> std::io::Result<()> {
    let input = std::fs::read_to_string("inputs/day_03.txt")?;

    let p1 = input
        .lines()
        .map(|line| {
            let (c1, c2) = line.split_at(line.len() / 2);
            c1.chars().find(|&c| c2.contains(c)).unwrap()
        })
        .map(priority)
        .sum::<u32>();

    let p2 = input
        .lines()
        .collect::<Vec<_>>()
        .chunks(3)
        .map(|chunk| {
            chunk[0]
                .chars()
                .find(|&c| chunk[1].contains(c) && chunk[2].contains(c))
                .unwrap()
        })
        .map(priority)
        .sum::<u32>();

    println!("{p1} {p2}");
    Ok(())
}

const fn priority(c: char) -> u32 {
    (if c.is_ascii_lowercase() {
        c as u8 - b'a' + 1
    } else {
        c as u8 - b'A' + 27
    }) as u32
}
