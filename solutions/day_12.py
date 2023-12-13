import itertools
import re
import copy
from inputs import day_12_examples as examples
from math import comb

myInput = [line.strip() for line in open("inputs/day_12.txt").readlines()]
myInput = examples.example1

numOptions = 0
for line in myInput:
    springs, target = line.split(' ')
    target = [int(x) for x in target.split(',')]
    unknown = [x.start() for x in re.finditer(r'\?', springs)]
    combos = itertools.combinations(unknown, sum(target)-len(re.findall(r'#', springs)))
    for combo in combos:
        tempSprings = list(springs)
        for loc in combo:
            tempSprings[loc] = '#'
        groups = [group.end() - group.start() for group in re.finditer(r'(#+)', ''.join(tempSprings))]
        if groups == target:
            numOptions += 1

# print(numOptions)

# Part Two (Work in Progress)
# Possible approach: Solve the problem recursively. Start at the largest group, figure out all the
# ways you could form that group, then call the count function on each of those paths for the second
# largest group until you've formed all the groups. Use a sliding window to see if you can form the groups.

# That was too slow. Next thought is to use Dynamic Programming. Tabulate all the ways you can form groups for each
# 'bucket', where a bucket is a consecutive sequence of # and ?. Recursively search the decision space.

# First, throw out any groups that are not adjustable


def prepLine(line, numCopies=1):
    springs, targets = line.split(' ')
    targets = [int(x) for x in targets.split(',')]*numCopies
    springs = '.' + '?'.join([springs for i in range(numCopies)]) + '.'

    fixedGroups = [x.end() - x.start() - 2 for x in re.finditer(r'\.(#+)\.', springs)]
    for group in fixedGroups:
        targets.remove(group)

    springs = re.sub(r'\.(#+)\.','.', springs)
    springs = re.sub(r'\.+', '.', springs)
    targets = list(targets)
    targets.sort(reverse=True)
    avail = [x for x in ''.join(springs).split('.') if len(x) != 0]
    indx = 0
    while targets[indx] == avail[indx] and indx < min(len(targets), len(avail))-1:
        indx += 1
    targets = targets[indx:]
    avail = avail[indx:]

    return avail, targets


def getNumOptions(springs, targets):
    if len(targets) == 0:
        return 1

    numOptions = 0
    
    for i in range(len(springs)-targets[0]):
        window = (i, targets[0] + i)
        if all(x != '.' for x in springs[window[0]:window[1]]):
            # print(window, ''.join(springs))
            tempSprings = copy.deepcopy(springs)
            newTargets = copy.deepcopy(targets)
            for j in range(window[0]-1, window[1]+1):
                tempSprings[j] = '.'
            numOptions += getNumOptions(tempSprings, newTargets[1:])
        # else:
            # print(window)

    return numOptions


def solveSubproblem(targets, bucket):
    return
    


def cacheSolutions(avail, targSums):
    solutions = {}
    numSolutions = 0
    for targGroups in itertools.product(*[range(x[1]+1) for x in targSums]):
        tempTargets = [(targSums[i][0], targGroups[i]) for i in range(len(targSums))]
        for bucket in set(avail):
            numSolutions += 1
            solutions[str(tempTargets)+str(bucket)] = solveSubproblem(tempTargets, bucket)
    print(numSolutions)
    return solutions


numOptions = 0
for line in myInput:
    avail, targets = prepLine(line, 5)
    targSums = [(y, len([x for x in targets if x == y])) for y in set(targets)]
    solutions = cacheSolutions(avail, targSums)