fn main() -> anyhow::Result<()> {
    let mut p1 = 0;
    let mut p2 = 0;

    for line in std::fs::read_to_string("2022/inputs/day_04.txt")?.lines() {
        let nums = line
            .split([',', '-'])
            .flat_map(str::parse::<u8>)
            .collect::<Vec<_>>();

        if (nums[0] >= nums[2] && nums[1] <= nums[3]) || (nums[2] >= nums[0] && nums[3] <= nums[1])
        {
            p1 += 1;
        }

        if nums[0] <= nums[3] && nums[2] <= nums[1] {
            p2 += 1;
        }
    }

    println!("{p1} {p2}");
    Ok(())
}
