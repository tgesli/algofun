from cell import Cell
from pieces import Piece
import numpy as np

class Board:

    BOARDSIZE = 9
    NBOXES = 9
    BOXSIZE = 3

    def __init__(self):
        self.cells = []
        self.grid = []
        self.stack = []
        for r in range(self.BOARDSIZE):
            row = []
            for c in range(self.BOARDSIZE):
                box = r//3 * 3 + c//3
                cell = Cell(r, c, box, False)
                row.append(cell)
                self.cells.append(cell)
            self.grid.append(row)
            self.bitmap.append(0)
        self.bmat = np.zeros((self.BOARDSIZE, self.BOARDSIZE), dtype=np.bool)


    def isLegalMove(self, piece:Piece, row:int, col:int):

        # bits = piece.getBits()
        # shift = self.BOARDSIZE - piece.ncols - col
        # for r in range(piece.nrows):
        #     if self.grid[row+r].bitmap & ( bits[r] << shift):
        #         return False

        res = np.logical_and(piece.bmat, self.bmat[row:row+piece.nrows,
                                                   col:col+piece.ncols])
        return res.sum() == 0

    #    for r in range(piece.nrows):
    #        for c in range(piece.ncols):
    #            if not (row+r in range(self.BOARDSIZE) \
    #                    and col+c in range(self.BOARDSIZE)):
    #                return False
    #            if piece.grid[r][c].isFilled():
    #                cell = self.grid[row+r][col+c]
    #                if cell.isFilled():
    #                    return False
    #     return True


    @staticmethod
    def allFull(cells):
        for c in cells:
            if not c.isFilled():
                return False
        return True


    @staticmethod
    def add2dict0lists(d, k, v):
        if k in d:
            d[k].append(v)
        else:
            d[k] = [v]

    def placePiece(self, piece:Piece, row:int, col:int):
        if not self.isLegalMove(piece, row, col):
            raise Exception("Illegal move")

        fresh = []
        for r in range(piece.nrows):
            for c in range(piece.ncols):
                if piece.grid[r][c].isFilled():
                    bcell = self.grid[row+r][col+c]
                    bcell.setFill(True)
                    bcell.setFresh(True)
                    fresh.append((r,c))
        return fresh


    def removePiece(self, fresh):
        for r, c in fresh:
            cell = self.grid[r][c]
            cell.setFill(False)
            cell.setFresh(False)


    def getClearedCells(self):
        row_mask = 511
        column_mask = 256
        box_mask = 7
        cleared_cells = 9 * [9 * [0]]

        for i in range(9):

        rcb = {}
        for cell in self.cells:
            Board.add2dict0lists(rcb, 'R-' + str(cell.getRow() + 1), cell)
            Board.add2dict0lists(rcb, 'C-' + str(cell.getCol() + 1), cell)
            Board.add2dict0lists(rcb, 'B-' + str(cell.getBox() + 1), cell)
        bag = set([])
        for k in rcb.keys():
            if Board.allFull(rcb[k]):
                bag.update(rcb[k])
        return bag


    def makeMove(self, piece:Piece, row:int, col:int):
        if not self.isLegalMove(piece, row, col):
            return -1

        self.placePiece(piece, row, col)
        bag = self.getClearedCells()

        for cell in bag:
            cell.setFill(False)

        score = piece.getPoints()
        if bag:
            score += 2*len(bag)

        return score


    def findRoomForPiece(self, piece:Piece):
        w, h = piece.getSize()
        positions = []
        for r in range(self.BOARDSIZE - h + 1):
            for c in range(self.BOARDSIZE - w + 1):
                if self.isLegalMove(piece, r, c):
                    positions.append((r, c))
        return positions


    def draw(self):

        # print('    1  2  3   4  5  6   7  8  9')
        # print('  +---------+---------+---------+');
        # print('1 |[#][#][#]|[#][#][#]|[#][#][#]|');
        # print('2 |[#][#][#]|[#][#][#]|[#][#][#]|');
        # print('3 |[#][#][#]|[#][#][#]|[#][#][#]|');
        # print('  +---------+---------+---------+');
        # print('4 |[#][#][#]|[#][#][#]|[#][#][#]|');
        # print('5 |[#][#][#]|[#][#][#]|[#][#][#]|');
        # print('6 |[#][#][#]|[#][#][#]|[#][#][#]|');
        # print('  +---------+---------+---------+');
        # print('7 |[#][#][#]|[#][#][#]|[#][#][#]|');
        # print('8 |[#][#][#]|[#][#][#]|[#][#][#]|');
        # print('9 |[#][#][#]|[#][#][#]|[#][#][#]|');
        # print('  +---------+---------+---------+');

        print('    1  2  3   4  5  6   7  8  9')
        for r in range(self.BOARDSIZE):
            if r % 3 == 0:
                print('  +---------+---------+---------+');
            print('{} '.format(r+1), end='')
            for c in range(self.BOARDSIZE):
                if c%3 == 0:
                    print('|', end='')
                print(self.grid[r][c].picture(), end='')
            print('|')
        print('  +---------+---------+---------+');


    def resetFresh(self):
        for cell in self.cells:
            cell.setFresh(False)