# Part One

myInput = open("inputs/day_1.txt").readlines()

def parseLine(myLine):
    myLine = list(filter(lambda c: c.isdigit(), myLine))
    return int(myLine[0])*10+int(myLine[-1])

print(sum(list(map(lambda line: parseLine(line), myInput))))

# Part Two

numMap = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9'
}

def parseLine(myLine):
    nums = []
    for i in range(len(myLine)):
        if (myLine[i].isdigit()):
            nums += [myLine[i]]
        for (key, num) in numMap.items():
            isLongEnough = (len(myLine) - i) >= len(key)
            if isLongEnough and (myLine[i:i+len(key)] == key):
                nums += [num]
    return int(nums[0]+nums[-1])

print(sum(list(map(lambda line: parseLine(line), myInput))))