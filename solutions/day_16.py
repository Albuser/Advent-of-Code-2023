with open("inputs/day_16.txt") as f:
    myInput = [x.strip() for x in f.readlines()]


# myInput = r""".|...\....
# |.-.\.....
# .....|-...
# ........|.
# ..........
# .........\
# ..../.\\..
# .-.-/..|..
# .|....-|.\
# ..//.|....""".split(
#     "\n"
# )


def add(t1, t2):
    return tuple(sum(x) for x in zip(t1, t2))


def trans(t1):
    return tuple(x for x in t1[::-1])


def neg(t1):
    return tuple(-x for x in t1)


class node:
    def __init__(self, location, direction):
        self.loc = location
        self.dir = direction

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __repr__(self):
        return str(self.loc) + " " + str(self.dir)


def isInBounds(myInput, loc):
    if (loc[0] >= len(myInput)) or (loc[0] < 0):
        return False
    elif (loc[1] >= len(myInput[0])) or (loc[1] < 0):
        return False
    return True


def addNode(visited, toVisit, loc, dir):
    if node(loc, dir).__hash__() in visited:
        return
    toVisit.append(node(loc, dir))


# Part One
def countTiles(start):
    visitedNodes = set()
    toVisit = [start]
    while len(toVisit) > 0:
        curNode = toVisit.pop()
        if not isInBounds(myInput, curNode.loc):
            continue
        visitedNodes.add(curNode)
        curVal = myInput[curNode.loc[0]][curNode.loc[1]]
        if (
            (curVal == ".")
            or (curVal == "-" and curNode.dir[0] == 0)
            or (curVal == "|" and curNode.dir[1] == 0)
        ):
            newDirs = [curNode.dir]
        elif curVal == "/":
            newDirs = [neg(trans(curNode.dir))]
        elif curVal == "\\":
            newDirs = [trans(curNode.dir)]
        elif curVal in ["|", "-"]:
            newDirs = [neg(trans(curNode.dir)), trans(curNode.dir)]
        for newDir in newDirs:
            addNode(visitedNodes, toVisit, add(curNode.loc, newDir), newDir)

    visitedLocs = list(set([x.loc for x in visitedNodes]))
    return len(visitedLocs)


# Part One
print(countTiles(node((0, 0), (0, 1))))

# Part Two
right = max([countTiles(node((i, 0), (0, 1))) for i in range(len(myInput))])
left = max(
    [countTiles(node((i, len(myInput[0])), (0, -1))) for i in range(len(myInput))]
)
down = max([countTiles(node((0, j), (1, 0))) for j in range(len(myInput[0]))])
up = max([countTiles(node((len(myInput), j), (-1, 0))) for j in range(len(myInput[0]))])
print(max([right, left, up, down]))
