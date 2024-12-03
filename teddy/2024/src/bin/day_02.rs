fn main() {
    let input = advent_of_code_2024::read_input!()
        .lines()
        .map(|line| {
            line.split_ascii_whitespace()
                .flat_map(str::parse::<i32>)
                .collect::<Vec<_>>()
        })
        .collect::<Box<_>>();
    let p1 = input.iter().filter(safe).count();
    let p2 = input
        .iter()
        .filter(|&report| {
            (0..report.len()).any(|i| {
                let mut report = report.clone();
                report.remove(i);
                safe(&report)
            })
        })
        .count();

    println!("part 1: {p1}");
    println!("part 2: {p2}");
}

fn safe(s: &impl AsRef<[i32]>) -> bool {
    let s = s.as_ref();
    s.windows(2)
        .all(|w| (w[0] < w[1]) == (s[0] < s[1]) && (1..=3).contains(&(w[0] - w[1]).abs()))
}
