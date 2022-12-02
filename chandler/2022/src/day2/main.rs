use std::collections::HashMap;
use std::fs::File;
use std::io::Read;

#[derive(Clone, Copy, PartialEq)]
enum Shapes {
    Rock,
    Paper,
    Scissors,
}

fn load_file() -> Vec<String> {
    let mut file = File::open("src/day2/input.txt").expect("Unable to open file");
    let mut contents = String::new();
    file.read_to_string(&mut contents)
        .expect("Unable to read file");
    contents.lines().map(|s| s.to_string()).collect()
}

fn win_logic(hand1: Shapes, hand2: Shapes) -> bool {
    hand1 == Shapes::Rock && hand2 == Shapes::Scissors
        || hand1 == Shapes::Paper && hand2 == Shapes::Rock
        || hand1 == Shapes::Scissors && hand2 == Shapes::Paper
}

fn main() {
    let mut lookup_table: HashMap<char, Shapes> = HashMap::new();
    let hand_strings = vec!["A", "B", "C", "X", "Y", "Z"];
    let possible_hands = vec![
        Shapes::Rock,
        Shapes::Paper,
        Shapes::Scissors,
        Shapes::Rock,
        Shapes::Paper,
        Shapes::Scissors,
    ];
    for i in 0..6 {
        lookup_table.insert(hand_strings[i].chars().nth(0).unwrap(), possible_hands[i]);
    }

    let contents = load_file();

    let mut my_total_score = 0;

    for item in contents {
        let mut score: u32 = 0;
        let first_item = item.chars().nth(0).unwrap();
        let second_item = item.chars().nth(2).unwrap();

        let opponent_hand = lookup_table.get(&first_item).unwrap();
        let my_hand = lookup_table.get(&second_item).unwrap();

        score += (*my_hand as u32) + 1;

        if my_hand == opponent_hand {
            score += 3;
        } else if win_logic(*my_hand, *opponent_hand) {
            score += 6;
        }

        my_total_score += score;
    }

    println!("Score: {}", my_total_score);
}
