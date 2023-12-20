import re
import json
import itertools

with open("inputs/day_19.txt") as f:
    myInput = [line.strip() for line in f.readlines()]


# myInput = """px{a<2006:qkq,m>2090:A,rfg}
# pv{a>1716:R,A}
# lnx{m>1548:A,A}
# rfg{s<537:gd,x>2440:R,A}
# qs{s>3448:A,lnx}
# qkq{x<1416:A,crn}
# crn{x>2662:A,R}
# in{s<1351:px,qqz}
# qqz{s>2770:qs,m<1801:hdj,R}
# gd{a>3333:R,R}
# hdj{m>838:A,pv}

# {x=787,m=2655,a=1222,s=2876}
# {x=1679,m=44,a=2067,s=496}
# {x=2036,m=264,a=79,s=2244}
# {x=2461,m=1339,a=466,s=291}
# {x=2127,m=1623,a=2188,s=1013}""".split(
#     "\n"
# )


def getLambda(step):
    if not (("<" in step) or (">" in step)):
        return lambda x: step
    attribute, val, result = re.split("[<>:]", step)
    if "<" in step:
        return lambda x: result if x[attribute] < int(val) else False
    return lambda x: result if x[attribute] > int(val) else False


def getWorkflows(myInput):
    indx = 0
    workflows = {}
    while len(myInput[indx]) != 0:
        line = myInput[indx]
        name = line[: line.index("{")]
        lineWorkflows = line[line.index("{") + 1 : -1].split(",")
        workflows[name] = [getLambda(step) for step in lineWorkflows]
        indx += 1
    return workflows


def getItems(myInput):
    start = myInput.index("") + 1
    items = []
    for line in myInput[start:]:
        cleanLine = re.sub(r",", r',"', line)
        cleanLine = re.sub(r"=", r'":', cleanLine)
        cleanLine = re.sub(r"{", r'{"', cleanLine)
        items.append(json.loads(cleanLine))
    return items


workflows = getWorkflows(myInput)
items = getItems(myInput)


def isAccepted(item):
    status = "in"
    while status not in ["R", "A"]:
        curWorkflow = workflows[status]
        for step in curWorkflow:
            result = step(item)
            if result != False:
                status = result
                break
    return status == "A"


# Part One
total = 0
for item in items:
    status = "in"
    while status not in ["R", "A"]:
        curWorkflow = workflows[status]
        for step in curWorkflow:
            result = step(item)
            if result != False:
                status = result
                break
    if status == "A":
        total += sum(item.values())
print(total)

# Part Two
combos = 0
maxVal = 30
for x, m, a, s in itertools.product(
    range(maxVal), range(maxVal), range(maxVal), range(maxVal)
):
    item = {"x": x, "m": m, "a": a, "s": s}
    combos += int(isAccepted(item))
print(combos)
