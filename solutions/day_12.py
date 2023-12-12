import re
import itertools
from inputs import day_12_examples as examples

myInput = [line.strip() for line in open("inputs/day_12.txt").readlines()]
# myInput = examples.example1

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

print(numOptions)

# Part Two (Work in Progress)
# Possible approach: Solve the problem recursively. Start at the largest group, figure out all the
# ways you could form that group, then call the count function on each of those paths for the second
# largest group until you've formed all the groups

def fact(n):
    num = 1
    indx = 1
    while indx <= n:
        num = num*indx
        indx += 1
    return num

numOptions = 0
for line in myInput:
    springs, target = line.split(' ')
    target = [int(x) for x in target.split(',')]
    springs = ''.join([*springs, '?', *springs, '?', *springs, '?', *springs, '?', *springs])
    target = [*target, *target, *target, *target, *target]
    unknown = [x.start() for x in re.finditer(r'\?', springs)]
    numUnk = len(unknown)
    numPos = sum(target) - len(re.findall(r'#', springs))
    numOptions += (int(fact(numUnk)/(fact(numUnk-numPos)*fact(numPos))))  # Totally Not Feasible

print(numOptions)