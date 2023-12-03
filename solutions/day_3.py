import re
import itertools

myInput = [line.strip() for line in open("inputs/day_3.txt").readlines()]

# Part One:
# Go through each line and extract the numbers. Then check all the adjacent spaces for symbols.
# If there's an adjacent symbol, add the number to a set. Last, sum all the numbers in the set.

partNumbers = set()
for i in range(len(myInput)):
    numLocs = [(j.start(), j.end()) for j in re.finditer(r'\d+', myInput[i])] # Find all the nums in the line
    for loc in numLocs:
        for (pos, x, y) in itertools.product(range(loc[0], loc[1]), range(-1,2), range(-1,2)):
            # This for-loop handles searching the adjacent spaces. 
            # pos - current location within the number
            # x   - vertical offset
            # y   - horizontal offset
            numTuple = (i, loc[0], loc[1], int(myInput[i][loc[0]:loc[1]]))
            # The set will store numbers as a tuple, so we can identify duplicates
            rowBounds = ((i+x) >= 0) and ((i+x) < len(myInput))
            colBounds = ((pos+y) >= 0) and ((pos+y) < len(myInput[i]))
            # Ensure we don't go out of bounds
            if rowBounds and colBounds and re.match('[^(\d|\.)]', myInput[i+x][pos+y]):
                partNumbers.add(numTuple)
                break

print(sum([num[3] for num in partNumbers]))

# Part Two
# Go through each line and find the asterisks.
# For each asterisk, check for adjacent numbers above, below, and to the left and right
# If there are exactly two adjacent, add their product to a running sum

def expandNum(string, start, end):
    # A helper function that takes a slice of the input representing part of a number
    # and expands it on either side until it finds the complete number
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
    starLocs = [star.start() for star in re.finditer(r'\*', myInput[i])]  # Asterisk positions in the current line
    for loc in starLocs:
        nums = []  # Keep track of adjacent numbers
        if (i > 0):  # If this isn't the first line, check the adjacent spaces in the previous line
            above = myInput[i-1][max(0, loc-1):min(lineLen, loc+2)]
            matches = re.finditer(r'\d+', above)
            nums += [expandNum(myInput[i-1], match.start()+loc-1, match.end()+loc-1) for match in matches]
        if (i < len(myInput)-1):  # If this isn't the last line, check the adjacent spaces in the next line
            below = myInput[i+1][max(0, loc-1):min(lineLen, loc+2)]
            matches = re.finditer(r'\d+', below)
            nums += [expandNum(myInput[i+1], match.start()+loc-1, match.end()+loc-1) for match in matches]
        if (myInput[i][max(0, loc-1)].isdigit()):  # Check to the left
            nums.append(expandNum(myInput[i], max(0, loc-1), max(0, loc-1)))
        if (myInput[i][min(lineLen-1,loc+1)].isdigit()):  # Check to the right
            nums.append(expandNum(myInput[i], min(lineLen-1,loc+1), min(lineLen-1,loc+1)))
        if len(nums) == 2:
            gearSum += nums[0]*nums[1]

print(gearSum)