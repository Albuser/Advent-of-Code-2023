import functools
import copy

myInput = [line.strip() for line in open("inputs/day_7.txt").readlines()]

pt1LetterMapping = {"T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}
pt2LetterMapping = {"T": 10, "Q": 11, "K": 12, "A": 13, "J": 0}


def parseCard(char, mapping):
    if char.isdigit():
        assert int(char) > 1
        return int(char)
    assert char in mapping
    return mapping.get(char)


class Hand:
    def __init__(self, inputLine, isPartTwo=False):
        curMap = pt1LetterMapping
        if isPartTwo:
            curMap = pt2LetterMapping
        self.isPartTwo = isPartTwo
        self.cards = [parseCard(char, curMap) for char in inputLine.split(" ")[0]]
        self.bid = int(inputLine.split(" ")[1])
        self.type = self.getHandType()
        assert len(self.cards) == 5
        assert self.type in range(7)

    def getHandType(self):
        if self.isPartTwo:
            tempCards = copy.deepcopy(self.cards)
            jokerLocs = [i for i in range(5) if self.cards[i] == 0]
            if len(jokerLocs) == 5:
                return 6  # 5 of a kind

            cardFreqs = [
                (len([card for card in tempCards if card == curCard]), curCard)
                for curCard in set(tempCards)
                if curCard != 0
            ]
            bestCard = sorted(cardFreqs, reverse=True)[0][1]

            for jokerLoc in jokerLocs:
                tempCards[jokerLoc] = bestCard
        else:
            tempCards = self.cards

        cardFreqs = [
            len([card for card in tempCards if card == curCard])
            for curCard in set(tempCards)
        ]
        pairs = [val for val in cardFreqs if val == 2]

        if len(cardFreqs) == 5:  # High Card
            return 0
        if len(cardFreqs) == 4:  # One Pair
            return 1
        if len(pairs) == 2:  # Two Pair
            return 2
        if len(cardFreqs) == 3:
            return 3  # Three of a Kind
        if len(pairs) == 1:
            return 4  # Full House
        if len(cardFreqs) == 2:
            return 5  # Four of a Kind
        return 6  # Five of a Kind

    def compareHands(self, otherHand):
        if self.type != otherHand.type:
            return self.type - otherHand.type
        for i in range(5):
            if self.cards[i] != otherHand.cards[i]:
                return self.cards[i] - otherHand.cards[i]
        return 0


# Part One

hands = [Hand(line) for line in myInput]
hands = sorted(hands, key=functools.cmp_to_key(lambda a, b: a.compareHands(b)))

print(sum([hands[i].bid * (i + 1) for i in range(len(hands))]))

# Part Two

hands = [Hand(line, isPartTwo=True) for line in myInput]
hands = sorted(hands, key=functools.cmp_to_key(lambda a, b: a.compareHands(b)))

print(sum([hands[i].bid * (i + 1) for i in range(len(hands))]))
