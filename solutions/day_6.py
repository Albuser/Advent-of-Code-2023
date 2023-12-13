import re
from functools import reduce

myInput = [line.strip() for line in open("inputs/day_6.txt").readlines()]

# Part One

times = [int(x) for x in re.findall(r"(\d+)", myInput[0])]
distances = [int(x) for x in re.findall(r"(\d+)", myInput[1])]
races = zip(times, distances)

nums = [
    len([x for x in range(race[0]) if ((race[0] - x) * x > race[1])]) for race in races
]
print(reduce(lambda a, b: a * b, nums))

# Part Two

raceTime = int("".join(re.findall(r"(\d+)", myInput[0])))
raceDist = int("".join(re.findall(r"(\d+)", myInput[1])))

print(len([x for x in range(raceTime) if ((raceTime - x) * x > raceDist)]))
print(raceTime)
print(raceDist)
