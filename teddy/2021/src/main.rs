#![warn(clippy::all, clippy::nursery, rust_2018_idioms)]
#![allow(dead_code)]
#![windows_subsystem = "console"]
#![doc = include_str!("../../README.md")]

mod day_1;
mod day_2;
mod day_3;
mod day_4;

fn main() {
    // Day 1
    // let input_day1 = day_1::parse_input(include_str!("day_1/input.txt"));
    // println!("{}", day_1::sonar_sweep_1(&input_day1)); // 1215
    // println!("{}", day_1::sonar_sweep_2(&input_day1)); // 1150

    // Day 2
    // let input_day2 = day_2::parse_input(include_str!("day_2/input.txt"));
    // println!("{}", day_2::dive(&input_day2, day_2::Submarine::default())); // 1694130
    // println!("{}", day_2::dive(&input_day2, day_2::Submarine::with_aim())); // 1698850445

    // Day 3
    // let input_day3 = day_3::parse_input(include_str!("day_3/input.txt"));
    // println!("{}", day_3::power_consumption_1(&input_day3)); // 2250414
    // println!("{}", day_3::power_consumption_2(&input_day3)); // 6085575

    // Day 4
    let input_day4 = day_4::parse_input(include_str!("day_4/input.txt"));
    println!("{input_day4:?}");
    // println!("{}", day_4::bingo_1(&input_day4)); // 23177
    // println!("{}", day_4::bingo_2(&input_day4)); // 6804
}
