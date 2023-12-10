from inputs import day_10_examples as examples

myInput = [line.strip() for line in open("inputs/day_10.txt").readlines()]

# myInput = examples.example3

myInput.insert(0, '.'*len(myInput[0]))
myInput.append('.'*len(myInput[0]))
myInput = ['.'+line+'.' for line in myInput]
numRows = len(myInput)
numCols = len(myInput[0])

upPipes = ['7', 'F', '|', 'S']
downPipes = ['L', 'J', '|', 'S']
rightPipes = ['L', 'F', '-', 'S']
leftPipes = ['J', '7', '-', 'S']

def neighbors(loc):
    neighbors = []
    curPipe = myInput[loc[0]][loc[1]]
    newPipe = myInput[loc[0]-1][loc[1]]
    if (newPipe in upPipes and curPipe in downPipes):
        neighbors.append((loc[0]-1, loc[1]))
    newPipe = myInput[loc[0]+1][loc[1]]
    if (newPipe in downPipes and curPipe in upPipes):
        neighbors.append((loc[0]+1, loc[1]))
    newPipe = myInput[loc[0]][loc[1]-1]
    if (newPipe in rightPipes and curPipe in leftPipes):
        neighbors.append((loc[0], loc[1]-1))
    newPipe = myInput[loc[0]][loc[1]+1]
    if (newPipe in leftPipes and curPipe in rightPipes):
        neighbors.append((loc[0], loc[1]+1))
    return neighbors

def move(loc, prevLoc):
    return [x for x in neighbors(loc) if (x[0], x[1]) != prevLoc][0]

startLoc = [(i, myInput[i].find('S')) for i in range(len(myInput)) if 'S' in myInput[i]][0]

prevLoc = startLoc
curLoc = neighbors(startLoc)[0]
loopLocs = [curLoc]
while curLoc != startLoc:
    nextLoc = [x for x in neighbors(curLoc) if (x[0], x[1]) != prevLoc][0]
    prevLoc = curLoc
    curLoc = nextLoc
    loopLocs.append(curLoc)

print(len(loopLocs)/2)

# Part Two
def updateStart():
    # Need to decide what to do with the start symbol
    startNeighbors = neighbors(startLoc)
    vertDiff = startNeighbors[0][0]-startNeighbors[1][0]
    horDiff = startNeighbors[0][1]-startNeighbors[1][1]
    if vertDiff == 0:
        newLine = myInput[startLoc[0]][:startLoc[1]]+'-'+myInput[startLoc[0]][startLoc[1]+1:]
    elif horDiff == 0:
        newLine = myInput[startLoc[0]][:startLoc[1]]+'|'+myInput[startLoc[0]][startLoc[1]+1:]
    elif vertDiff == 1 and horDiff == 1:
        newLine = myInput[startLoc[0]][:startLoc[1]]+'7'+myInput[startLoc[0]][startLoc[1]+1:]
    elif vertDiff == 1 and horDiff == -1:
        newLine = myInput[startLoc[0]][:startLoc[1]]+'F'+myInput[startLoc[0]][startLoc[1]+1:]
    elif vertDiff == -1 and horDiff == 1:
        newLine = myInput[startLoc[0]][:startLoc[1]]+'J'+myInput[startLoc[0]][startLoc[1]+1:]
    else:
        newLine = myInput[startLoc[0]][:startLoc[1]]+'L'+myInput[startLoc[0]][startLoc[1]+1:]
    myInput[startLoc[0]] = newLine

area = 0
updateStart()
newInput = [[int(not (i, j) in loopLocs) for j in range(numCols)] for i in range(numRows)]

for row in range(numRows):
    rowArea = 0
    for col in range(numCols):
        loopBits = [myInput[row][x] for x in range(col, numCols) if newInput[row][x] == 0 and myInput[row][x] != '-']
        loopBits = ['.', *loopBits, '.']
        indx = 1
        numCrossings = 0
        while indx < len(loopBits) - 1:
            if loopBits[indx] == 'F' and loopBits[indx+1] == '7':
                indx += 2
            elif loopBits[indx] == 'L' and loopBits[indx+1] == 'J':
                indx += 2
            elif loopBits[indx] in ['F', 'L']:
                indx += 2
                numCrossings += 1
            else:
                numCrossings += 1
                indx += 1
        rowArea += newInput[row][col]*(numCrossings % 2)
    area += rowArea

print(area)