from pieces import Piece
import numpy as np

class Board:

    BOARDSIZE = 9
    NBOXES = 9
    BOXSIZE = 3
    MASK = np.array(9*[True])

    def __init__(self):
        self.bmat = np.array(self.BOARDSIZE * [ self.BOARDSIZE * [False]])
        self.moves = 0


    def isLegalMove(self, piece:Piece, row:int, col:int):

        res = np.logical_and(piece.bmat, self.bmat[row:row+piece.nrows,
                                                   col:col+piece.ncols])
        return res.sum() == 0


    def placePiece(self, piece:Piece, row:int, col:int):
        self.bmat[row:row+piece.nrows, col:col+piece.ncols] += piece.bmat


    def getClearedCells(self):

        cleared_cells = np.array(self.BOARDSIZE * [self.BOARDSIZE * [False]])
        for i in range(self.BOARDSIZE):
            if np.count_nonzero(self.bmat[i, :]) == self.BOARDSIZE:
                cleared_cells[i, :] = self.MASK
            if np.count_nonzero(self.bmat[:, i]) == self.BOARDSIZE:
                cleared_cells[:, i] = self.MASK
            if np.count_nonzero(self.bmat[i//3*3:(i//3+1)*3, i%3*3:(i%3+1)*3]) == self.BOARDSIZE:
                cleared_cells[i//3*3:(i//3+1)*3, i%3*3:(i%3+1)*3] =\
                    self.MASK.reshape(self.BOXSIZE, self.BOXSIZE)

        return cleared_cells


    def makeMove(self, piece:Piece, row:int, col:int):
        if not self.isLegalMove(piece, row, col):
            return -1

        self.placePiece(piece, row, col)
        mask = self.getClearedCells()
        self.bmat *= np.logical_not(mask)
        self.moves += 1
        return piece.getPoints() + np.count_nonzero(mask)*2


    def findRoomForPiece(self, piece:Piece):
        positions = []
        for r in range(self.BOARDSIZE - piece.nrows + 1):
            for c in range(self.BOARDSIZE - piece.ncols + 1):
                if self.isLegalMove(piece, r, c):
                    positions.append((r, c))
        return positions


    def draw(self):

        def picture(isFull):
            return '[*]' if isFull else '   '

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

