import re

myInput = open("inputs/day_4.txt").readlines()

# Part One
# Store the winning nums in a set for fast lookup
# Go through line by line and count the matches

def parse_line(line):
    line = line.split(':')[1]
    winningNums = set(re.findall('\d+', line.split('|')[0]))
    myNums = re.findall('\d+', line.split('|')[1])
    numMatches = len([num for num in myNums if num in winningNums])
    if numMatches > 0: return 2**(numMatches-1)
    return 0

print(sum([parse_line(line) for line in myInput]))


# Part Two
# Store the number of matches on each card in a dict
# Store the number of card copies you have in a dict
# Populate the match nums, and set each copy number to 1
# Loop through the cards, adding as many copies as needed

def parse_line(line, matchDict, cardsDict):
    # Get the number of matches, set num copies to 1
    ID, line = line.split(':')
    ID = int(re.search('\d+', ID).group())
    winningNums = set(re.findall('\d+', line.split('|')[0]))
    myNums = re.findall('\d+', line.split('|')[1])
    matchDict[ID] = len([num for num in myNums if num in winningNums])
    cardsDict[ID] = 1

matchDict = {}  # ID : number of matches
cardsDict = {}  # ID : number of copies

for line in myInput:
    parse_line(line, matchDict, cardsDict)

for card, numMatches in matchDict.items():
    # This loops through in insertion order
    for i in range(card+1, card+numMatches+1):
        cardsDict[i] += cardsDict[card]

print(sum(cardsDict.values()))