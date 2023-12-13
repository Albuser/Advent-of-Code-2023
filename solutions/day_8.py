import re
import math

myInput = [line.strip() for line in open("inputs/day_8.txt").readlines()]

dirMap = {"R": 1, "L": 0}
directions = [dirMap[char] for char in myInput[0]]


def parseLine(line, mapMap):
    key, left, right = [
        re.search(regex, line).group(1) for regex in [r"^(\w+)", r"\((\w+)", r"(\w+)\)"]
    ]
    mapMap[key] = (left, right)


mapMap = {}
for line in myInput[2:]:
    parseLine(line, mapMap)

# Part One

curLoc = "AAA"
curIndx = 0
while curLoc != "ZZZ":
    curLoc = mapMap[curLoc][directions[curIndx % len(directions)]]
    curIndx += 1

print(curIndx)

# Part Two
# This doesn't work in general but it gave the right answer so :person-shrugging:

curLocs = [loc for loc in mapMap.keys() if loc[-1] == "A"]
startSteps = [0] * len(curLocs)
while not all([loc[-1] == "Z" for loc in curLocs]):
    pending = [loc for loc in enumerate(curLocs) if loc[1][-1] != "Z"]
    for loc in pending:
        curLocs[loc[0]] = mapMap[loc[1]][
            directions[startSteps[loc[0]] % len(directions)]
        ]
        startSteps[loc[0]] += 1

print(math.lcm(*startSteps))
