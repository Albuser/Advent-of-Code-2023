import re
from functools import reduce

myInput = open("inputs/day_2.txt").readlines()

# Part One


def parseLine(line):
    gameId = re.search(r"Game (\d+):", line).group(1)
    reds = [int(x) <= 12 for x in re.findall(r"(\d+) red", line)]
    greens = [int(x) <= 13 for x in re.findall(r"(\d+) green", line)]
    blues = [int(x) <= 14 for x in re.findall(r"(\d+) blue", line)]
    if all(reds) and all(greens) and all(blues):
        return int(gameId)
    return 0


print(sum([parseLine(line) for line in myInput]))

# Part Two


def parseLine(line):
    colors = [r"(\d+) red", r"(\d+) green", r"(\d+) blue"]
    maxNums = [
        max(set)
        for set in [[int(x) for x in re.findall(color, line)] for color in colors]
    ]
    return reduce((lambda x, y: x * y), maxNums)


print(sum([parseLine(line) for line in myInput]))
