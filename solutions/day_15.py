import re

with open("inputs/day_15.txt") as f:
    myInput = f.read().strip()


def parseStep(curVal, step):
    for char in step:
        curVal = (17 * (curVal + ord(char))) % 256
    return curVal


# Part One:
print(sum([parseStep(0, step) for step in myInput.split(",")]))

# Part Two:
boxes = {}
for step in myInput.split(","):
    label = re.split(r"[-=]", step)[0]
    curHash = parseStep(0, label)

    if not curHash in boxes:
        boxes[curHash] = []

    match = list(filter(lambda lens: lens[0] == label, boxes[curHash]))
    if "=" in step:
        if len(match) == 0:
            boxes[curHash].append((label, int(step[-1])))
        else:
            for i, lens in enumerate(boxes[curHash]):
                if lens[0] == label:
                    boxes[curHash][i] = (label, int(step[-1]))
                    break
    else:
        match = list(filter(lambda lens: lens[0] == label, boxes[curHash]))
        if len(match) == 1:
            boxes[curHash].remove(match[0])

totalPower = 0
for box, lenses in boxes.items():
    for i, lens in enumerate(lenses):
        totalPower += (box + 1) * (i + 1) * (lens[1])

print(totalPower)
