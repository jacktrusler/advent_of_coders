fn main() -> anyhow::Result<()> {
    let mut p1 = 0;
    let mut p2 = 0;

    for mut chars in std::fs::read_to_string("inputs/day_02.txt")?
        .lines()
        .map(|line| line.chars().filter(char::is_ascii_alphabetic))
    {
        let abc = chars.next().unwrap() as u8 - b'A';
        let xyz = chars.next().unwrap() as u8 - b'X';
        p1 += u32::from((xyz + 1) + ((xyz + 1 + (3 - abc)) % 3 * 3));
        p2 += u32::from(((xyz + abc + 2) % 3 + 1) + (xyz * 3));
    }

    println!("{p1} {p2}");
    Ok(())
}
