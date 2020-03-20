
from itertools import product
from itertools import combinations

from random import shuffle
from random import sample

import time


class pokerDeck:
    ranks = ['2','3','4','5','6','7','8','9','10', 'J', 'Q', 'K', 'A']
    suits = ['s', 'h', 'c', 'd']  # ['♠', '♥', '♣', '♦']
    handTypes = ['HC', 'PR', '2P', 'TR', 'S8', 'FL', 'FH', 'QU', 'SF']
    
    rank_values = { } 
    
    def __init__(self):
        self.deck = list(product(self.ranks, self.suits))
        shuffle(self.deck)
        if not self.rank_values:
            for i in range(len(self.ranks)):
                self.rank_values[self.ranks[i]] = i+2
 

    def deal(self, nplayers):
        hands = []
        
        # first cards
        for p in range(nplayers):
            hands.append([self.deck.pop()])
            
        # second cards
        for p in range(nplayers):
            hands[p].append(self.deck.pop())
            
        return hands
        

    def nextCard(self):
        return self.deck.pop(0)


    def getSample(self, n):
        return sample(self.deck, n)
    
    
    def rankHands(self, hands, board):
        winners = []
        for hand in hands:
            maxScore = 0
            winner = board
            cards = hand + board
            for combo in combinations(cards, 5):
                score = handRank(combo)
                if score > maxScore:
                    maxScore = score
                    winner = combo
            winners.append(winner)
        return winners


    def handScore7(self, hand, board):

        hiscore = 0
        hihand = board
        for hand in combinations(hand + board, 5):
            sh,ht,sc = self.handScore5(hand)
            if sc > hiscore:
                hiscore = sc
                hihand = sh
                hitype = ht
                
        return hihand, hitype, hiscore
        
    
    def handScore5(self, hand):
        # return (sortedHand, handType, score)
        htype = "HC"
        score = 0
        
        handRanks = sorted([self.rank_values[card[0]] for card in hand], reverse=True)
        flush = len(set([card[1] for card in hand])) == 1  
        paired = len(set(handRanks))  < 5
        
        if paired:
            str8 = False
            htype = "PR" # at least one pair
            handRanks = sortPairs(handRanks)
        else:
            if handRanks[0] == 14 and handRanks[1] == 5: # Special case: Wheel
                handRanks.pop(0)
                handRanks.append(1)
            str8 = handRanks[0] - handRanks[-1] == 4


        if str8:
            htype = "S8"
            score = handRanks[0]
            if flush:
                htype = "SF"
        else:
            if flush:
                htype = "FL"
            else:
                if handRanks[0] == handRanks[3]:
                    htype = "QU"
                elif handRanks[0] == handRanks[2]:
                    if handRanks[3] == handRanks[4]:
                        htype = "FH"
                    else:
                        htype = "TR"
                else:
                    if handRanks[2] == handRanks[3]:
                        htype = "2P"

            seen = []
            for r in handRanks:
                if r not in seen:
                    score = 14*score + r
                    seen.append(r)
 
        score += self.handTypes.index(htype) * 1000000 
        
        return handRanks, htype, score 
        

def sortPairs(hr):
    freq = {}
    for r in hr:
        if r in freq:
            freq[r] += 1
        else:
            freq[r] = 1
    
    l = sorted([(freq[r], r) for r in freq], reverse=True)

    sr = []
    for f, r in l:
        for i in range(f):
            sr.append(r)

    return sr

    
def showCards(cardlist, title):
    str = title
    delim = ": "
    for rank, suit in cardlist:
        str += "{delim}{rank}{suit}".format(**locals())
        delim = ", "
    print(str)

        
def main():               
    nplayers = 9
    deck = pokerDeck()

    # deal hands to players
    hands = deal(deck, nplayers)
    for i in range(len(hands)):
        showCards(hands[i], "Player{i}".format(**locals()))

    # deal the board
    deck.pop() #burn
    board = [deck.pop() for _ in range(3)]
    deck.pop() #burn
    board.append(deck.pop())
    deck.pop() #burn
    board.append(deck.pop())
    showCards(board, "Board")

    # rank hands
    winners = rankHands(hands, board)


"""
          Lowest         Highest 
HC:      283,460         576,011
PR:      606,527         641,143
2P:      700,620         702,938
TR:      800,451         802,938
S8:      900,005         900,014
FL:    1,000,007       1,000,014
FH:    1,100,031       1,100,209  
QU:    1,200,031       1,200,209
SF:    1,300,005       1,300,014

"""

def runTest(deck, hand):
    showCards(hand, "Test Hand")
    sh, ht, sc = deck.handScore5(hand)
    print('Sorted ranks = {sh}\n'
          'Hand Type    = {ht}\n'
          'Score        = {sc}\n'
          '------------------------'.format(**locals()))


def parseCards(cards):
    lst = []
    for c in cards.split(' '):
        lst.append((c[:-1], c[-1]))
    return lst


def formatCards(cards):
    res = ''
    for c in cards:
        res += c[0] + c[1] + ' '
    return res


def runTests():
    deck = pokerDeck()
    
    # hand = [deck.nextCard() for _ in range(5)]
    runTest(deck, parseCards("Ah Kh Qh Jh 9h"))
    runTest(deck, parseCards("7h 2h 3h 4h 5h"))


def runPerfTest():
    deck = pokerDeck()
    strt = time.perf_counter()
    memo = []
    for _ in range(1000000):
        hand = deck.getSample(5)
        sh, ht, sc = deck.handScore(hand)
        memo.append((sc, hand, sh, ht))
    stop = time.perf_counter()
    print("Total ticks for 100,000 hand scores: %s"%(stop-strt))
    print("Top 100 hands:")

    # top hands
    memo = sorted(memo, reverse=True)
    for i in range(100):
        sc, hand, sh, ht = memo[i]
        print("{sc} : {hand} - {sh} - {ht}".format(**locals()))

    # stats
    d = { "SF": 0, "QU": 0, "FH": 0, "FL": 0, "S8" : 0, "TR": 0,
          "2P": 0,  "PR": 0, "HC" : 0 } 
    for ht in [res[3] for res in memo]:
        d[ht] += 1

    print(d)
        

def showTopN(lst):
    topN = len(lst)
    print("Top %s hands:"%topN)

    # top hands
    memo = sorted(lst, reverse=True)
    for i in range(topN):
        sc, hand, board, sh, ht = lst[i]
        handStr = formatCards(hand)
        boardStr = formatCards(board)
        print("{sc} : H({handStr}) B({boardStr}) - {sh} - {ht}".format(**locals()))
    print("--------------------------")


def showStats(stats, total):
     # stats
    print("Hand Type Stats:")
    for s, t in sorted([(stats[ht], ht) for ht in stats], reverse=True):
        pct = int((s/total)*10000)/100.0
        print("{t}: {s}  {pct}%".format(**locals()))
    print("--------------------------")


def runPerfTest7():
    stats = { "SF": 0, "QU": 0, "FH": 0, "FL": 0, "S8" : 0,
              "TR": 0, "2P": 0,  "PR": 0, "HC" : 0 } 
    strt = time.perf_counter()
    # memo = []
    numTests = 100000
    batchSize = 10000

    deck = pokerDeck()

    for n in range(numTests):

        if n>0 and n%batchSize == 0:
            showStats(stats, n)
            
        bh = deck.getSample(7)
        hand = bh[:2]
        board = bh[2:]

        handStr = formatCards(hand)
        boardStr = formatCards(board)
        
        sh, ht, sc = deck.handScore7(hand, board)
        # memo.append((sc, hand, board, sh, ht))

        stats[ht] += 1
        
    stop = time.perf_counter()
    
    print("Total ticks for %s hand scores: %s"%(numTests, stop-strt))
    print("--------------------------")

        
if __name__ == '__main__':
    # runTests()
    runPerfTest7()
