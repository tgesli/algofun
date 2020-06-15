from board import Board
from pieces import Piece
from typing import List, Tuple
from itertools import permutations
import copy
import random


class Player:

    def getMoves(self, board:Board, pieces: List[Piece]):
        return [None]


class HumanPlayer(Player):

    def getMoves(self, board:Board, pieces: List[Piece]):
        p=-1
        while p==-1:
            p = int(input("Please enter the piece number:"))
            if p == 0:
                return [None]
            elif p > 0 and p <= len(pieces):
                print("You picked piece #{}: ")
                pieces[p-1].draw()
            else:
                print("This is an invalid choice. Try again...")
                p=0

        r=-1
        while r==-1:
            s = input("Enter row,col to place upper left of this piece:")
            r, c = [int(n) for n in s.split(',')]
            if r in range(1, 10) and c in range(1, 10) \
                                 and board.isLegalMove(pieces[p-1], r-1, c-1):
                return [(pieces[p-1], r-1, c-1)]
            else:
                print("This is an invalid choice. Try again...")
                r = -1


class RandomPlayer(Player):

    def getMoves(self, board:Board, pieces: List[Piece]):

        move = None
        plist = [_ for _ in pieces]
        while plist:
            piece = random.choice(plist)
            positions = board.findRoomForPiece(piece)
            if positions:
                row, col = random.choice(positions)
                move = (piece, row, col)
                break
            else:
                plist.remove(piece)

        return [move]


class RulePlayer(Player):

    def getMoves(self, board:Board, pieces: List[Piece]):
        tempboard = copy.deepcopy(board)
        maxscore = 0
        move = None
        for piece in pieces:
            h, w = piece.getSize()
            for row in range(Board.BOARDSIZE - h + 1):
                for col in range(Board.BOARDSIZE - w + 1):
                    score = tempboard.makeMove(piece, row, col)
                    if score > 0:  # legal move
                        newhi = 0
                        for p in Piece.getPieces():
                            newhi += len(tempboard.findRoomForPiece(p))
                        if newhi > maxscore:
                            maxscore = newhi
                            move = (piece,row,col)
                        tempboard = copy.deepcopy(board)

        return [move]


class BrutePlayer(Player):

    def __init__(self):
        self.moveLimit = 10
        self.cachedMoves = []
        self.maxTries = 100

    def getBestMoves(self, board:Board, pieces:List[Piece]):
        tempBoard = copy.deepcopy(board)
        bestMove = []
        moves = []
        hiScore = 0

        for piece in pieces:
            h, w = piece.getSize()
            remPieces = [p for p in pieces if p != piece]
            depth = 3 - len(remPieces)

            if depth == 2:
                self.moveLimit = 0

            for row in range(Board.BOARDSIZE - h + 1):
                for col in range(Board.BOARDSIZE - w + 1):
                    score = tempBoard.makeMove(piece, row, col)
                    if score > 0:  # legal move
                        move = (piece, row, col)
                        newHi = 0
                        self.moveLimit += 1
                        if remPieces:      # more pieces remain
                            newHi, moves = self.getBestMoves(tempBoard, remPieces)
                        else:   # no more pieces
                            for p in Piece.getPieces():
                                newHi += len(tempBoard.findRoomForPiece(p))
                        if newHi > hiScore:
                            hiScore = newHi
                            bestMove = [move] + moves
                        if depth == 3 and self.moveLimit >= self.maxTries:
                            return hiScore, bestMove
                    tempBoard = copy.deepcopy(board)

        return hiScore, bestMove


    def getMoves(self, board:Board, pieces: List[Piece]):
        self.moveLimit = 0
        _, self.cachedMoves = self.getBestMoves(board, pieces)
        return self.cachedMoves


class SmartPlayer(Player):

    def __init__(self, sampleSize=0):
        self.cachedMoves = []
        self.sampleSize = sampleSize
        self.tmc = 0  # total moves considered


    def getMoves(self, board:Board, pieces: List[Piece]):
        hiReward = 0
        hiValue = 0
        bestMoves = []
        self.tmc = 0
        for p0, p1, p2 in permutations(pieces):
            for r0, c0 in board.findRoomForPiece(p0, self.sampleSize):
                b0 = copy.deepcopy(board)
                rew0 = b0.makeMove(p0, r0, c0)
                for r1, c1 in b0.findRoomForPiece(p1, self.sampleSize):
                    b1 = copy.deepcopy(b0)
                    rew1 = b1.makeMove(p1, r1, c1)
                    for r2, c2 in b1.findRoomForPiece(p2, self.sampleSize):
                        b2 = copy.deepcopy(b1)
                        rew2 = b2.makeMove(p2, r2, c2)
                        self.tmc += 1
                        reward = rew0 + rew1 + rew2
                        if reward > hiReward:
                            bestMoves = [ [p0, r0, c0], [p1, r1, c1], [p2, r2, c2] ]
                            hiReward = reward
                            hiValue = b2.getStateValue()
                        elif reward == hiReward:
                            value = b2.getStateValue()
                            if value>hiValue:
                                hiValue = value
                                bestMoves = [[p0, r0, c0], [p1, r1, c1], [p2, r2, c2]]
        if len(bestMoves) < 3:
            bestMoves.append(None)

        return bestMoves


class LRPlayer(Player):

    def __init__(self):
        self.cachedMoves = []
        self.tmc = 0  # total moves considered


    def getBestMoves(self, board:Board, pieces:List[Piece], indices: List[int]):
        tempBoard = copy.deepcopy(board)
        bestMove = []
        moves = []
        hiScore = 0

        for idx in indices:
            piece = pieces[idx]
            remIndices = [i for i in indices if i != idx]
            posList = tempBoard.findRoomForPiece(piece)

            for row, col in posList:
                tempBoard.makeMove(piece, row, col)
                move = (piece, row, col)
                if remIndices:      # more pieces remain
                    newHi, moves = self.getBestMoves(tempBoard, pieces, remIndices)
                else:   # final move in series
                    newHi = tempBoard.predictStateValue()
                    self.tmc += 1

                if newHi > hiScore:
                    hiScore = newHi
                    bestMove = moves + [move]

                tempBoard = copy.deepcopy(board)

        return hiScore, bestMove


    def getMoves(self, board:Board, pieces: List[Piece]):
        self.moveLimit = 0
        self.tmc = 0
        idx = [0, 1, 2]
        _, self.cachedMoves = self.getBestMoves(board, pieces, idx)

        if len(self.cachedMoves)<3:
            return None, None
        return self.cachedMoves


class SmartLRPlayer(Player):
    # TODO: DNRY - refactor these so that there aren't so much common code
    #       in these classes

    def __init__(self, sampleSize=0):
        self.cachedMoves = []
        self.sampleSize = sampleSize
        self.tmc = 0  # total moves considered


    def getMoves(self, board:Board, pieces: List[Piece]):
        hiReward = 0
        hiValue = 0
        bestMoves = []
        self.tmc = 0
        for p0, p1, p2 in permutations(pieces):
            for r0, c0 in board.findRoomForPiece(p0, self.sampleSize):
                b0 = copy.deepcopy(board)
                rew0 = b0.makeMove(p0, r0, c0)
                for r1, c1 in b0.findRoomForPiece(p1, self.sampleSize):
                    b1 = copy.deepcopy(b0)
                    rew1 = b1.makeMove(p1, r1, c1)
                    for r2, c2 in b1.findRoomForPiece(p2, self.sampleSize):
                        b2 = copy.deepcopy(b1)
                        rew2 = b2.makeMove(p2, r2, c2)
                        self.tmc += 1
                        reward = rew0 + rew1 + rew2
                        if reward > hiReward:
                            bestMoves = [ [p0, r0, c0], [p1, r1, c1], [p2, r2, c2] ]
                            hiReward = reward
                            hiValue = b2.predictStateValue()
                        elif reward == hiReward:
                            value = b2.predictStateValue()
                            if value>hiValue:
                                hiValue = value
                                bestMoves = [[p0, r0, c0], [p1, r1, c1], [p2, r2, c2]]
        if len(bestMoves) < 3:
            bestMoves.append(None)

        return bestMoves
