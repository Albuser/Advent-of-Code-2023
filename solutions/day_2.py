import re

myInput = open("inputs/day_2.txt").readlines()

# Part One

def parseLine(line):
    gameId = re.search(r'Game (\d+):', line).group(1)
    reds =   [int(x) <= 12 for x in re.findall(r'(\d+) red',   line)]
    greens = [int(x) <= 13 for x in re.findall(r'(\d+) green', line)]
    blues =  [int(x) <= 14 for x in re.findall(r'(\d+) blue',  line)]
    if all(reds) and all(greens) and all(blues):
        return int(gameId)
    return 0

print(sum(list(map(lambda line: parseLine(line), myInput))))

# Part Two

def parseLine(line):
    reds =   [int(x) for x in re.findall(r'(\d+) red',   line)]
    greens = [int(x) for x in re.findall(r'(\d+) green', line)]
    blues =  [int(x) for x in re.findall(r'(\d+) blue',  line)]
    return max(reds)*max(greens)*max(blues)

print(sum(list(map(lambda line: parseLine(line), myInput))))