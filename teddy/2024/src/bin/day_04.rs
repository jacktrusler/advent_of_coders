fn main() {
    let input = advent_of_code_2024::read_input!()
        .lines()
        .map(|l| l.chars().collect::<Box<[_]>>())
        .collect::<Box<_>>();
    #[rustfmt::skip]
    let offsets1 = [
        ( 1, -1), ( 1, 0), ( 1, 1),
        ( 0, -1),          ( 0, 1),
        (-1, -1), (-1, 0), (-1, 1),
    ];
    let search1 = ['X', 'M', 'A', 'S'];
    let offsets2 = [(1, -1), (1, 1), (-1, -1), (-1, 1)];
    let search2 = ["MMSS", "SSMM", "MSMS", "SMSM"];

    let (mut p1, mut p2) = (0, 0);
    for (i, row) in input.iter().enumerate() {
        for (j, letter) in row.iter().enumerate() {
            if letter == &'X' {
                for (di, dj) in offsets1 {
                    if (1..search1.len()).all(|k| {
                        let (ni, nj) = (i as i32 + di * k as i32, j as i32 + dj * k as i32);
                        input
                            .get(ni as usize)
                            .and_then(|r| r.get(nj as usize))
                            .is_some_and(|c| c == &search1[k])
                    }) {
                        p1 += 1;
                    }
                }
            }

            if letter == &'A' {
                let letters = offsets2
                    .iter()
                    .filter_map(|(di, dj)| {
                        let (ni, nj) = (i as i32 + di, j as i32 + dj);
                        input.get(ni as usize)?.get(nj as usize)
                    })
                    .collect::<String>();
                if search2.contains(&&*letters) {
                    p2 += 1;
                }
            }
        }
    }

    println!("part 1: {p1}");
    println!("part 2: {p2}");
}
