from datetime import datetime
import random

from pieces import Piece
import numpy as np
import copy



def read_theta():
    theta_file = open("data/theta.txt", "r")
    return [float(s) for s in theta_file.read().split('\n')]


class Board:

    BOARDSIZE = 9
    NBOXES = 9
    BOXSIZE = 3
    MASK = np.array(9*[True])
    sFile = open("data/blokustates.{0:%Y-%m-%d_%H:%M:%S}.txt".format(datetime.now()), "w")
    outputSize = 0
    theta = read_theta()

    def __init__(self, blist=None):
        self.moveCount = 0
        self.bonus = False
        if blist:
            for r in blist:
                self.bmat = np.array([Piece.int2bits(r, self.BOARDSIZE) for r in blist])
        else:
            self.bmat = np.array(self.BOARDSIZE * [self.BOARDSIZE * [False]])


    def isLegalMove(self, piece:Piece, row:int, col:int):

        res = np.logical_and(piece.bmat, self.bmat[row:row+piece.nrows,
                                                   col:col+piece.ncols])
        return res.sum() == 0


    def placePiece(self, piece:Piece, row:int, col:int):
        self.bmat[row:row+piece.nrows, col:col+piece.ncols] += piece.bmat


    def getClearedCells(self):
        cleared_cells = np.array(self.BOARDSIZE * [self.BOARDSIZE * [False]])
        cleared_count = 0
        for i in range(self.BOARDSIZE):
            if np.count_nonzero(self.bmat[i, :]) == self.BOARDSIZE:
                cleared_cells[i, :] = self.MASK
                cleared_count += 1
            if np.count_nonzero(self.bmat[:, i]) == self.BOARDSIZE:
                cleared_cells[:, i] = self.MASK
                cleared_count += 1
            if np.count_nonzero(self.bmat[i//3*3:(i//3+1)*3, i%3*3:(i%3+1)*3]) == self.BOARDSIZE:
                cleared_cells[i//3*3:(i//3+1)*3, i%3*3:(i%3+1)*3] =\
                    self.MASK.reshape(self.BOXSIZE, self.BOXSIZE)
                cleared_count += 1
        return cleared_cells, cleared_count


    def makeMove(self, piece:Piece, row:int, col:int):
        if not self.isLegalMove(piece, row, col):
            return -1

        orig = np.array(self.bmat)
        self.placePiece(piece, row, col)
        mask, count = self.getClearedCells()
        self.bmat *= np.logical_not(mask)
        self.moveCount += 1

        points = np.count_nonzero(np.logical_not(orig) * self.bmat)
        if count == 0:
            self.bonus = False
        else:
            if self.bonus:
                points += 9
            self.bonus = True

        points += count * (count + 1) * 9
        return points


    def findRoomForPiece(self, piece:Piece, limit:int = 0):
        positions = []
        h, w = piece.getSize()
        for r in range(self.BOARDSIZE - h + 1):
            for c in range(self.BOARDSIZE - w + 1):
                if self.isLegalMove(piece, r, c):
                    positions.append((r, c))
        if limit and len(positions)>limit:
            positions = random.sample(positions, limit)
        return positions


    def __str__(self):
        return ' '.join(str(n) for n in self.numList())


    def logState(self, val):
        self.sFile.write(str(self) + ' ' + str(val) + '\n')
        Board.outputSize += 1
        if Board.outputSize % 1000 == 0:
            self.sFile.flush()


    def saveState(self):
        self.tempMat = copy.deepcopy(self.bmat)
        self.tempCount = self.moveCount


    def restoreState(self):
        self.bmat = copy.deepcopy(self.tempMat)
        self.moveCount = self.tempCount


    def getStateValue(self):
        val = 0
        for p in Piece.getPieces():
            rooms = self.findRoomForPiece(p)
            val += len(rooms)
        self.logState(val)
        return val


    def predictStateValue(self):
        prediction = self.theta[0]
        ti = 1
        for r in self.bmat:
            for c in r:
                if c:
                    prediction += self.theta[ti]
                ti += 1
        prediction = (prediction + 1) * 779 + 227
        return prediction


    def draw(self):

        def picture(isFull):
            return '[.]' if isFull else '   '

        print('    1  2  3   4  5  6   7  8  9')
        for r in range(self.BOARDSIZE):
            if r % self.BOXSIZE == 0:
                print('  +---------+---------+---------+');
            print('{} '.format(r+1), end='')
            for c in range(self.BOARDSIZE):
                if c%self.BOXSIZE == 0:
                    print('|', end='')
                print(picture(self.bmat[r, c]), end='')
            print('|')
        print('  +---------+---------+---------+');

        print(str(self))


    def numList(self):
        return Piece.bits2ints(self.bmat)

