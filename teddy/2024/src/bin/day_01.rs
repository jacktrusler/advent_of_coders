fn main() {
    let (mut left, mut right) = advent_of_code_2024::read_input!().lines().fold(
        (vec![], vec![]),
        |(mut left, mut right), line| {
            let mut nums = line.split_ascii_whitespace().flat_map(str::parse::<i32>);
            left.push(nums.next().unwrap());
            right.push(nums.next().unwrap());
            (left, right)
        },
    );
    left.sort_unstable();
    right.sort_unstable();
    let p1 = left
        .iter()
        .zip(right.iter())
        .map(|(x, y)| (x - y).abs())
        .sum::<i32>();
    let p2 = left
        .iter()
        .map(|x| x * right.iter().filter(|y| &x == y).count() as i32)
        .sum::<i32>();

    println!("part 1: {p1}");
    println!("part 2: {p2}");
}
