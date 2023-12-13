from inputs import day_13_example as examples

with open("inputs/day_13.txt") as myInput:
    rawText = myInput.read().replace('.', '0').replace('#', '1')
    patterns = [x.split('\n') for x in rawText.split('\n\n')]

# patterns = examples.example_1

# Part One

def checkForMirror(ints):
    # Return the index of the reflection, if it exists. Otherwise, return 0.
    if ints[0] == ints[1]:
        return 1
    p1, p2 = (1, 2)
    while (p2 < len(ints)):
        hasReflection = True
        i = 0
        for i in range(min(p1+1, len(ints)-p2)):
            if ints[p1-i] != ints[p2+i]:
                hasReflection = False
                break
        if hasReflection:
            return p2
        p1 += 1
        p2 += 1
    return 0

def getSolution(checkFunction):
    noteSum = 0
    for pattern in patterns:
        rows = [int(row, 2) for row in pattern]
        cols = [int(''.join([pattern[j][col] for j in range(len(pattern))]), 2) for col in range(len(pattern[0]))]
        rowResult = checkFunction(rows)
        if rowResult:
            noteSum += 100*(rowResult)
        else:
            noteSum += checkFunction(cols)
    return noteSum

print(getSolution(checkForMirror))

# Part Two

def isSmudged(int1, int2):
    # Name is misleading. they could either be equal or off by a smudge
    if int1 == int2:
        return 1
    dist = sum([int(x) for x in bin(int1 ^ int2)[2:]])
    if dist == 1:
        return 1
    return 0

def checkForMirrorPt2(ints):
    if isSmudged(ints[0], ints[1]) and ints[0] != ints[1]:
        return 1
    p1, p2 = (1, 2)
    solutions = []
    while (p2 < len(ints)):
        smudgeCount = 0
        smudges = []
        hasReflection = True
        i = 0
        for i in range(min(p1+1, len(ints)-p2)):
            if not isSmudged(ints[p1-i], ints[p2+i]):
                hasReflection = False
                break
            elif ints[p1-i] != ints[p2+i]:
                smudgeCount += 1
                smudges.append((p1, p2, i, ints[p1-i], ints[p2+i]))
            if smudgeCount > 1:
                hasReflection = False
                break
        if hasReflection and smudgeCount == 1:
            return p2
        p1 += 1
        p2 += 1
    return 0

print(getSolution(checkForMirrorPt2))