fn main() {
    let input = advent_of_code_2023::read_input!()
        .lines()
        .map(|l| l.chars().collect::<Box<[char]>>())
        .collect::<Box<_>>();
    let (start_i, start_j) = input
        .iter()
        .enumerate()
        .find_map(|(i, l)| l.iter().position(|c| c == &'S').map(|j| (i, j)))
        .unwrap();

    println!("{start_i}, {start_j}");
}
