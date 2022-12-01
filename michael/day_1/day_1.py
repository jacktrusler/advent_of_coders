#day_1 AOC 2022 python file
import time
FULL_DATA, TEST_DATA = "./michael/day_1/day_1.txt", "./michael/day_1/day_1_min.txt"

def execute_time(func):
	def wrapper(*args, **kwargs):
		start = time.process_time()
		result = func(*args, **kwargs)
		end = time.process_time()
		print(f"{func.__name__}: {result}\nRan in {end - start} seconds")
		return result
	return wrapper

@execute_time
def part_one(calories):
	return max(calories)

@execute_time
def part_two(calories):
	calories.sort()
	return sum(calories[-3:])


with open(FULL_DATA) as f:
	calorie_counts = [sum([int(calorie) for calorie in calorie_group.split("\n")]) for calorie_group in f.read().split("\n\n")]

part_one(calorie_counts)
part_two(calorie_counts)

