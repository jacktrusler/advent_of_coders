use std::fs::File;
use std::io::Read;

#[derive(Clone)]
struct Elf {
    pub item_calories: Vec<u32>,
    pub total_calories: u32,
}

fn load_file() -> Vec<String> {
    let mut file = File::open("src/day1/input.txt").expect("Unable to open file");
    let mut contents = String::new();
    file.read_to_string(&mut contents)
        .expect("Unable to read file");
    contents.lines().map(|s| s.to_string()).collect()
}

fn main() {
    // initialization
    let contents = load_file();
    // create a new vector of elves
    let mut elves: Vec<Elf> = Vec::new();
    let mut current_elf: Elf = Elf {
        item_calories: Vec::new(),
        total_calories: 0,
    };
    for item in contents.iter() {
        if item == "" {
            elves.push(current_elf);
            current_elf = Elf {
                item_calories: Vec::new(),
                total_calories: 0,
            };
            continue;
        }
        let value = item.parse::<u32>().unwrap();
        current_elf.item_calories.push(value);
        current_elf.total_calories += value;
    }
    let last_elf = elves.last().unwrap();
    if last_elf.total_calories != current_elf.total_calories {
        elves.push(current_elf);
    }
    // part 1
    current_elf = Elf {
        item_calories: Vec::new(),
        total_calories: 0,
    };
    let mut count = 0;
    for elf in elves.iter() {
        if elf.total_calories > current_elf.total_calories {
            current_elf = elf.clone();
            count += 1;
        }
    }
    println!("Elf {}: {}", count, current_elf.total_calories);
    //part 2
    // sort the elves by calories
    elves.sort_by(|a, b| b.total_calories.cmp(&a.total_calories));
    // get first three elements
    let top_3_elves = &elves[0..3];

    let mut total = 0;
    for elf in top_3_elves.iter() {
        total += elf.total_calories;
    }

    println!("Total calories of the top 3: {}", total);
}
