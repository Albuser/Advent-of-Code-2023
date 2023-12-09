import re
myInput = [line.strip() for line in open("inputs/day_9.txt").readlines()]

def parseLine(line, endIndx=-1, factor=1):
    nums = [int(num) for num in re.findall(r'-?\d+', line)]
    extrapolated = nums[endIndx]
    while any([num != 0 for num in nums]):
        nums = [nums[i+1]-nums[i] for i in range(len(nums)-1)]
        extrapolated += nums[endIndx]*(factor)**(len(nums)+1)
    return extrapolated

# Part One

print(sum([parseLine(line) for line in myInput]))

# Part Two

print(sum([parseLine(line, 0, -1) for line in myInput]))