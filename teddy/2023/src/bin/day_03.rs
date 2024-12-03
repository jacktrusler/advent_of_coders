#![feature(let_chains)]

fn main() {
    #[rustfmt::skip]
    let deltas = [
        (-1, -1), (-1, 0), (-1, 1),
        (0,  -1),          (0,  1),
        (1,  -1), (1,  0), (1,  1),
    ];
    let input: Vec<Vec<char>> = advent_of_code_2023::read_input!()
        .lines()
        .map(str::chars)
        .map(Iterator::collect)
        .collect();
    let line_len = input[0].len();

    let char_from_offset = |i: usize, j: usize, di: i32, dj: i32| {
        if let Ok(i) = usize::try_from(i as i32 + di)
            && let Ok(j) = usize::try_from(j as i32 + dj)
            && let Some(row) = input.get(i)
            && let Some(c) = row.get(j)
        {
            Some((c, i, j))
        } else {
            None
        }
    };
    let is_part_number = |i: usize, j: usize| {
        deltas.iter().any(|&(di, dj)| {
            char_from_offset(i, j, di, dj).is_some_and(|(c, ..)| !c.is_ascii_digit() && c != &'.')
        })
    };
    let maybe_gear = |i: usize, j: usize| {
        let adjacent_parts = deltas
            .iter()
            .filter_map(|&(di, dj)| {
                if let Some((c, i, j)) = char_from_offset(i, j, di, dj)
                    && c.is_ascii_digit()
                {
                    Some((i, j))
                } else {
                    None
                }
            })
            .collect::<Vec<_>>();

        if adjacent_parts.len() >= 2 {
            Some(adjacent_parts)
        } else {
            None
        }
    };

    let (a, groups, gears) = input.iter().enumerate().fold(
        (0, Vec::new(), Vec::new()),
        |(a, mut groups, mut gears), (i, line)| {
            let (line_sum, _) = line.iter().enumerate().fold(
                (0, Vec::new()),
                |(mut line_sum, mut group), (j, c)| {
                    if c.is_ascii_digit() {
                        group.push((i, j, c));
                    } else if c == &'*'
                        && let Some(adjacent_parts) = maybe_gear(i, j)
                    {
                        gears.push(adjacent_parts);
                    }

                    if (!c.is_ascii_digit() || j == line_len - 1) && !group.is_empty() {
                        if group.iter().any(|&(_, j, _)| is_part_number(i, j)) {
                            let sum = group
                                .iter()
                                .map(|(_, _, c)| c.to_digit(10).unwrap())
                                .fold(0, |acc, n| acc * 10 + n);
                            line_sum += sum;
                            groups.push((
                                group.iter().map(|&(i, j, _)| (i, j)).collect::<Vec<_>>(),
                                sum,
                            ));
                        }

                        group = Vec::new();
                    }

                    (line_sum, group)
                },
            );

            (a + line_sum, groups, gears)
        },
    );

    let b = gears.into_iter().fold(0, |b, adjacent_parts| {
        let mut part_numbers = Vec::new();
        let (count, _) =
            adjacent_parts
                .into_iter()
                .fold((0, None), |(mut count, mut group), (i, j)| {
                    let prev = group;
                    group = groups.iter().position(|group| group.0.contains(&(i, j)));

                    if group != prev
                        && let Some(k) = group
                    {
                        count += 1;
                        part_numbers.push(groups[k].1);
                    }
                    (count, group)
                });

        if count == 2 {
            b + part_numbers.iter().product::<u32>()
        } else {
            b
        }
    });

    println!("part 1: {a}");
    println!("part 2: {b}");
}
