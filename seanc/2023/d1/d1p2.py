import string
import re

pattern = r"(one)|(two)|(three)|(four)|(five)|(six)|(seven)|(eight)|(nine)"

text_nums = {
             'one' : 'o1e', 
             'two' : 't2o', 
             'three' : 't3e', 
             'four' : 'f4r', 
             'five' : 'f5e', 
             'six' : 's6x', 
             'seven' : 's7n', 
             'eight' : 'e8t', 
             'nine' : 'n9e', 
             }

def resub(line):
    new_line = re.sub(pattern, lambda m: text_nums[m.group(0)],line)
    if re.search(pattern,new_line):
        return resub(new_line)
    return new_line


input = "input.txt"
calibration_values = []
with open(input) as f:
    lines = f.readlines()
for line in lines:
    line = resub(line)
    line = line.strip(string.ascii_letters + string.whitespace)
    nums = line[0] + line[-1]
    calibration_values.append(int(nums))
print(sum(calibration_values))