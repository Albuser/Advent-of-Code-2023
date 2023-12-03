import re
import itertools

myInput = [line.strip() for line in open("inputs/day_3.txt").readlines()]

# Part One

partNumbers = set()
for i in range(len(myInput)):
    numLocs = [(j.start(), j.end()) for j in re.finditer(r'\d+', myInput[i])]
    for loc in numLocs:
        for (pos, x, y) in itertools.product(range(loc[0], loc[1]), range(-1,2), range(-1,2)):
            numTuple = (i, loc[0], loc[1], int(myInput[i][loc[0]:loc[1]]))
            rowBounds = ((i+x) >= 0) and ((i+x) < len(myInput))
            colBounds = ((pos+y) >= 0) and ((pos+y) < len(myInput[i]))
            if rowBounds and colBounds and re.match('[^(\d|\.)]', myInput[i+x][pos+y]):
                partNumbers.add(numTuple)
                break

print(sum([num[3] for num in partNumbers]))

# Part Two

def expandNum(string, start, end):
    while start > 0 and string[start-1].isdigit():
        start -= 1
    while end < len(string) and string[end].isdigit():
        end += 1
    if start == end:
        return int(string[start])
    return int(string[start:end])

gearSum = 0
for i in range(len(myInput)):
    lineLen = len(myInput[i])
    starLocs = [star.start() for star in re.finditer(r'\*', myInput[i])]
    for loc in starLocs:
        nums = []
        if (i > 0):
            above = myInput[i-1][max(0, loc-1):min(lineLen, loc+2)]
            matches = re.finditer(r'\d+', above)
            nums += [expandNum(myInput[i-1], match.start()+loc-1, match.end()+loc-1) for match in matches]
        if (i < len(myInput)-1):
            below = myInput[i+1][max(0, loc-1):min(lineLen, loc+2)]
            matches = re.finditer(r'\d+', below)
            nums += [expandNum(myInput[i+1], match.start()+loc-1, match.end()+loc-1) for match in matches]
        if (myInput[i][max(0, loc-1)].isdigit()): nums.append(expandNum(myInput[i], max(0, loc-1), max(0, loc-1)))
        if (myInput[i][min(lineLen-1,loc+1)].isdigit()): nums.append(expandNum(myInput[i], min(lineLen-1,loc+1), min(lineLen-1,loc+1)))
        if len(nums) == 2:
            gearSum += nums[0]*nums[1]

print(gearSum)