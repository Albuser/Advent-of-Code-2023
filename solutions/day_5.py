import re
import portion as I

myInput = [line.strip() for line in open("inputs/day_5.txt").readlines()]

# Part One

seeds = [int(num) for num in myInput[0].split(': ')[1].split(' ')]
levels = []  # Each element is a list, containing all the intervals for each conversion step
curIntervals = []  # Used to keep track of the intervals within a single step

for line in myInput[2:]:
    if re.match('(\d+|\b)+', line):
        # If the line has numbers, add them to curIntervals
        curIntervals.append((tuple(int(x) for x in re.findall('(\d+)', line))))
    elif line == '':
        # A blank line indicates a boundary
        levels.append(curIntervals)
    else:
        # This matches the "soil-fertilizer map:" or whatever lines. Reset the curIntervals.
        curIntervals = []
        continue
levels.append(curIntervals)  # Need to make sure we add the last map

for level in levels:  # Go through soil -> fertilizer -> ... and update the number
    for i in range(len(seeds)):
        for interval in level:
            if (seeds[i] >= interval[1]) and (seeds[i] < interval[1]+interval[2]):
                seeds[i] += (interval[0]-interval[1])
                break  # Break cause you should stop after the first match

print(min(seeds))


# Part Two

seeds = [int(num) for num in myInput[0].split(': ')[1].split(' ')]
seeds = [I.closed(seeds[2*i], seeds[2*i]+seeds[2*i+1]-1) for i in range(len(seeds)//2)]
seed = seeds[0]
for x in seeds[1:]:
    seed = seed | x

levels = []
curIntervals = []

def intervalIsEmpty(interval):
    left = int(interval.left == I.OPEN)
    right = int(interval.right == I.OPEN)
    return (left+interval.lower) >= (interval.upper-right)

for line in myInput[2:]:
    if re.match('(\d+|\b)+', line):
        # If the line has numbers, add them to curIntervals
        dest, source, num = (tuple(int(x) for x in re.findall('(\d+)', line)))
        curIntervals.append((I.closed(source, source+num-1), dest-source))
    elif line == '':
        # A blank line indicates a boundary
        levels.append(curIntervals)
    else:
        # This matches the "soil-fertilizer map:" or whatever lines. Reset the curIntervals.
        curIntervals = []
        continue
levels.append(curIntervals)  # Need to make sure we add the last map

for level in levels:
    newSeed = I.open(0,0)
    seedCopy = seed
    for interval in level:
        seedCopy = seedCopy - interval[0]
        if seed.overlaps(interval[0]):
            overlap = seed & interval[0]
            overlap = overlap.apply(lambda x: (x.left, x.lower + interval[1], x.upper + interval[1], x.right))
            newSeed = newSeed | overlap
    newSeed = newSeed | seedCopy
    seed = newSeed

cleaned = I.open(0,0)
for unit in seed:
    if not intervalIsEmpty(unit):
        cleaned = cleaned | unit

print(cleaned.enclosure)

var = 1
print(type(var))