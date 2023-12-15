import re
from inputs import day_14_examples as examples

with open("inputs/day_14.txt") as f:
    platform = [x.strip() for x in f.readlines()]


def calcLoad(platform):
    return sum(
        [
            (len(platform) - i) * len([x for x in platform[i] if x == "O"])
            for i in range(len(platform))
        ]
    )


def shiftRounds(row, direction):
    squares = [0, *[x.start() + 1 for x in re.finditer(r"#", row)], len(row) + 1]
    newRow = ""
    for i in range(len(squares) - 1):
        groupSize = squares[i + 1] - squares[i]
        numRounds = len(re.findall("O", row[squares[i] : squares[i + 1]]))
        if direction in ["R", "D"]:
            newRow += "#" + "." * (groupSize - numRounds - 1) + "O" * numRounds
        else:
            newRow += "#" + "O" * numRounds + "." * (groupSize - numRounds - 1)
    return newRow[1:]


def tilt(platform, direction):
    if direction == "R":
        for i in range(len(platform)):
            platform[i] = shiftRounds(platform[i], direction)
    elif direction == "L":
        for i in range(len(platform)):
            platform[i] = shiftRounds(platform[i], direction)
    elif direction in ["U", "D"]:
        cols = [
            "".join([platform[row][col] for row in range(len(platform))])
            for col in range(len(platform[0]))
        ]
        for j in range(len(cols)):
            col = cols[j]
            newCol = shiftRounds(col, direction)
            for i in range(len(col)):
                platform[i] = platform[i][:j] + newCol[i] + platform[i][j + 1 :]

    return platform


# Part One
print(calcLoad(tilt(platform, "U")))

# Part Two
with open("inputs/day_14.txt") as f:
    platform = [x.strip() for x in f.readlines()]

directions = ["U", "L", "D", "R"]
hashes = {}
for i in range(1000):
    for direction in directions:
        platform = tilt(platform, direction)
    curHash = hash(str(platform))
    if curHash in hashes:
        cycleStart = hashes[curHash][0]
        cycleLength = i - cycleStart
        break
    else:
        hashes[curHash] = (i, calcLoad(platform))

relativeIndex = (1000000000 - cycleStart - 1) % cycleLength
finalIndex = cycleStart + relativeIndex
print([x[1][1] for x in hashes.items() if x[1][0] == finalIndex][0])
