fn main() -> std::io::Result<()> {
    let input = std::fs::read_to_string("inputs/day_05.txt")?;
    let (crates, procedure) = input.split_once("\n\n").unwrap();

    #[allow(clippy::needless_collect)]
    let crates = crates
        .lines()
        .take(crates.len() - 1)
        .map(|line| {
            line.chars()
                .skip(1)
                .step_by(4)
                .enumerate()
                .filter_map(|(i, c)| if c != ' ' { Some((i, c)) } else { None })
        })
        .collect::<Vec<_>>();

    let mut crates1 = Vec::with_capacity(9);
    crates1.extend(std::iter::repeat(Vec::with_capacity(64)).take(9));

    for line in crates.into_iter().rev() {
        for (i, c) in line {
            crates1[i].push(c);
        }
    }

    let mut crates2 = crates1.clone();
    let mut instr = Vec::with_capacity(3);

    for line in procedure.lines() {
        instr.clear();
        instr.extend(
            line.split_ascii_whitespace()
                .skip(1)
                .step_by(2)
                .flat_map(str::parse::<usize>),
        );

        let from = instr[1] - 1;
        let to = instr[2] - 1;

        let len = crates1[from].len();
        let mut moved = crates1[from].split_off(len - instr[0]);
        moved.reverse();
        crates1[to].extend(moved);

        let len = crates2[from].len();
        let moved = crates2[from].split_off(len - instr[0]);
        crates2[to].extend(moved);
    }

    println!("{} {}", top(&crates1), top(&crates2));
    Ok(())
}

fn top(crates: &[Vec<char>]) -> String {
    crates
        .iter()
        .fold(String::with_capacity(9), |mut s, stack| {
            s.push(*stack.last().unwrap());
            s
        })
}
