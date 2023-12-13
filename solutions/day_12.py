import re
from functools import lru_cache

myInput = [line.strip() for line in open("inputs/day_12.txt").readlines()]


def prepLine(line, numCopies=1):
    springs, targets = line.split(" ")
    targets = [int(x) for x in targets.split(",")] * numCopies
    springs = "." + "?".join([springs for i in range(numCopies)]) + "."
    return springs, tuple(targets)


@lru_cache(maxsize=None)
def numOptions(springs, targets):
    if len(targets) == 0:
        return int(not "#" in springs)
    if "#" in springs:
        substr = "." + springs[: springs.find("#") + targets[0] + 1]
    else:
        substr = "." + springs
    regex = r"(?=[.?][#?]{" + str(targets[0]) + r"}[.?])"
    options = [x.start() + targets[0] for x in re.finditer(regex, "." + substr)]
    return sum([numOptions(springs[x:], targets[1:]) for x in options])


print(sum([numOptions(*prepLine(line, 1)) for line in myInput]))  # Part One
print(sum([numOptions(*prepLine(line, 5)) for line in myInput]))  # Part Two
