//! [Day 2](https://adventofcode.com/2021/day/2): Submarine movement.

pub fn parse_input(input: &str) -> Vec<(Direction, i32)> {
    input
        .split_whitespace()
        .collect::<Vec<_>>()
        .chunks_exact(2)
        .map(|c| (Direction::try_from(c[0]).unwrap(), c[1].parse().unwrap()))
        .collect()
}

#[derive(Clone, Copy, strum::EnumString)]
#[strum(serialize_all = "lowercase")]
pub enum Direction {
    Forward,
    Down,
    Up,
}

#[derive(Default)]
pub struct Submarine {
    aim: Option<i32>,
    x: i32,
    y: i32,
}

impl Submarine {
    pub const fn with_aim() -> Self {
        Self { aim: Some(0), x: 0, y: 0 }
    }

    fn travel(&mut self, direction: Direction, distance: i32) {
        match (self.aim, direction) {
            (None, Direction::Forward) => self.x += distance,
            (None, Direction::Down) => self.y += distance,
            (None, Direction::Up) => self.y -= distance,

            (Some(a), Direction::Forward) => {
                self.x += distance;
                self.y += a * distance;
            }
            (Some(a), Direction::Down) => self.aim = Some(a + distance),
            (Some(a), Direction::Up) => self.aim = Some(a - distance),
        }
    }
}

pub fn dive(commands: &[(Direction, i32)], mut sub: Submarine) -> i32 {
    for &(dir, dist) in commands {
        sub.travel(dir, dist);
    }
    sub.x * sub.y
}
