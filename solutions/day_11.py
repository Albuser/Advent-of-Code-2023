import re
import itertools

myInput = [line.strip() for line in open("inputs/day_11.txt").readlines()]

# Get empty rows and columns
emptyRows = set([i for i in range(len(myInput)) if not '#' in myInput[i]])
emptyCols = set([i for i in range(len(myInput[0])) if not '#' in [myInput[j][i] for j in range(len(myInput))]])
# Find all the galaxies
galaxies = [[(row, col.start()) for col in re.finditer('(#)', myInput[row])] for row in range(len(myInput))]
galaxies = list(itertools.chain.from_iterable(galaxies))

def distance(gal1, gal2, rate):
    # Get the distance between a pair of gals, based on rate of expansion
    distance = abs(gal1[0] - gal2[0]) + abs(gal1[1] - gal2[1])
    for i in range(min(gal1[0], gal2[0]), max(gal1[0], gal2[0])):
        if i in emptyRows:
            distance += rate
    for i in range(min(gal1[1], gal2[1]), max(gal1[1], gal2[1])):
        if i in emptyCols:
            distance += rate
    return distance

pairLengthsPt1 = 0
pairLengthsPt2 = 0
for i in range(len(galaxies)):
    for j in range(i, len(galaxies)):
        pairLengthsPt1 += distance(galaxies[i], galaxies[j], 1)
        pairLengthsPt2 += distance(galaxies[i], galaxies[j], 999999)

print(pairLengthsPt1)
print(pairLengthsPt2)