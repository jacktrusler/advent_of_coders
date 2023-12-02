import string

input = "input.txt"
calibration_values = []
with open(input) as f:
    lines = f.readlines()
for line in lines:
    # print(line)
    line = line.strip(string.ascii_letters + string.whitespace)
    # print(line)
    nums = line[0] + line[-1]
    calibration_values.append(int(nums))
print(sum(calibration_values))