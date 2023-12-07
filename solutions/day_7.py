import re
import functools
import copy
myInput = [line.strip() for line in open("inputs/day_7.txt").readlines()]

pt1LetterMapping = {'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
pt2LetterMapping = {'T': 10, 'Q': 11, 'K': 12, 'A': 13, 'J': 0}

def parseCard(char, mapping):
    if char.isdigit():
        return int(char)
    return mapping.get(char)

class Hand:
    def __init__(self, inputLine, isPartTwo=False):
        if isPartTwo:
            curMap = pt2LetterMapping
        else:
            curMap = pt1LetterMapping
        self.cards = [parseCard(char, curMap) for char in inputLine.split(' ')[0]]
        self.bid = int(inputLine.split(' ')[1])
        self.type = self.getHandType(isPartTwo)
    
    def getHandType(self, isPartTwo):
        if isPartTwo:
            tempCards = copy.deepcopy(self.cards)
            jokerLocs = [i for i in range(5) if self.cards[i] == 0]
            if len(jokerLocs) == 5: return 6  # 5 of a kind

            cardFreqs = [(len([card for card in tempCards if card == curCard]), curCard) for curCard in set(tempCards) if curCard != 0]
            bestCard = sorted(cardFreqs, reverse=True)[0][1]

            for jokerLoc in jokerLocs:
                tempCards[jokerLoc] = bestCard
        else:
            tempCards = self.cards

        multiplicities = [len([card for card in tempCards if card == curCard]) for curCard in set(tempCards)]
        pairs = [val for val in multiplicities if val == 2]
        assert(sum(multiplicities) == 5)
        if len(multiplicities) == 5:  # High Card
            return 0
        if len(multiplicities) == 4:  # One Pair
            return 1
        if len(pairs) == 2:  # Two Pair
            return 2
        if (len(multiplicities) == 3):
            return 3  # Three of a Kind
        if len(pairs) == 1:
            return 4  # Full House
        if (len(multiplicities) == 2):
            return 5  # Four of a Kind
        return 6  # Five of a Kind
    
    def compareHands(self, otherHand):
        if self.type != otherHand.type:
            return self.type - otherHand.type
        for i in range(5):
            if self.cards[i] != otherHand.cards[i]:
                return self.cards[i] - otherHand.cards[i]
            
def compareHands(card1, card2):
    return card1.compareHands(card2)

# Part One

hands = [Hand(line) for line in myInput]
hands = sorted(hands, key=functools.cmp_to_key(compareHands))

print(sum([hands[i].bid*(i+1) for i in range(len(hands))]))

# Part Two

hands = [Hand(line, True) for line in myInput]
hands = sorted(hands, key=functools.cmp_to_key(compareHands))

print(sum([hands[i].bid*(i+1) for i in range(len(hands))]))