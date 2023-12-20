import re

with open("inputs/day_18.txt") as f:
    myInput = [line.strip() for line in f.readlines()]

# myInput = """R 6 (#70c710)
# D 5 (#0dc571)
# L 2 (#5713f0)
# D 2 (#d2c081)
# R 2 (#59c680)
# D 2 (#411b91)
# L 5 (#8ceee2)
# U 2 (#caa173)
# L 1 (#1b58a2)
# U 2 (#caa171)
# R 2 (#7807d2)
# U 3 (#a77fa3)
# L 2 (#015232)
# U 2 (#7a21e3)""".split(
#     "\n"
# )

field = [list("." * 800) for x in range(500)]
# field = [list("." * 25) for x in range(25)]


def testInclusion(line, colIndx):
    loopBits = [char for char in line[colIndx:] if char not in ["-", "."]]
    numCrossings = 0
    indx = 0
    while indx < len(loopBits):
        if loopBits[indx] == "F" and loopBits[indx + 1] == "7":
            indx += 2
        elif loopBits[indx] == "L" and loopBits[indx + 1] == "J":
            indx += 2
        elif loopBits[indx] in ["F", "L"]:
            indx += 2
            numCrossings += 1
        else:
            numCrossings += 1
            indx += 1
    return bool(numCrossings % 2)


def countArea(field):
    area = 0
    for line in field:
        for colIndx in range(len(line)):
            if line[colIndx] != ".":
                area += 1
                continue
            area += int(testInclusion(line, colIndx))
    return area


cornerSymbols = {
    ("R", "R"): "-",
    ("L", "L"): "-",
    ("D", "D"): "|",
    ("U", "U"): "|",
    ("R", "L"): "-",
    ("R", "D"): "7",
    ("R", "U"): "J",
    ("L", "R"): "-",
    ("L", "D"): "F",
    ("L", "U"): "L",
    ("U", "R"): "F",
    ("U", "L"): "7",
    ("U", "D"): "|",
    ("D", "R"): "L",
    ("D", "L"): "J",
    ("D", "U"): "|",
}


def digEdge(loc, dir, dist, color):
    dist = int(dist)
    step = -1
    if dir in ["R", "D"]:
        step = 1
    field[loc["row"]][loc["col"]] = cornerSymbols[(loc["lastDir"], dir)]
    loc["lastDir"] = dir
    for i in range(dist):
        if dir in ["R", "L"]:
            loc["col"] += step
            if i != dist - 1:
                field[loc["row"]][loc["col"]] = "-"
        else:
            loc["row"] += step
            if i != dist - 1:
                field[loc["row"]][loc["col"]] = "|"


loc = {"col": int(len(field[0]) / 2), "row": int(len(field) / 2), "lastDir": "U"}

for line in myInput:
    digEdge(loc, *line.split(" "))

print(countArea(field))
