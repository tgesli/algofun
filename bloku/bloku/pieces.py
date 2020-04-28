from cell import Cell
import random
import numpy as np

class Piece:

    pieces = {}

    __pieces = ['.', '..', '...', '....', '.....',
                './.', '././.', './././.', '././././.',
                '. / .', ' ./. ', '.  / . /  .', '  ./ . /.  ',
                '../..', '../. ', '../ .', '. /..', ' ./..',
                '.../ . ', ' . /...', '. /../. ', ' ./../ .',
                '.../ . / . ', ' . / . /...', '.  /.../.  ', '  ./.../  .',
                '.  /.  /...', '  ./  ./...', '.../.  /.  ', '.../  ./  .',
                ' ../.. ', '.. / ..', '. /../ .', ' ./../. ',
                '. ./...', '.../. .', '../. /..', '../ ./..']

    @staticmethod
    def getRandomPiece():
        if not Piece.pieces:
            for p in Piece.__pieces:
                Piece.pieces[p] = Piece(p)
        return random.choice(list(Piece.pieces.values()))


    def __init__(self, str):

        if not Piece.pieces:
            Piece.pieces['dummy'] = 'dummy'
            for p in Piece.__pieces:
                Piece.pieces[p] = Piece(p)
            del Piece.pieces['dummy']

        if not str:
            str = random.choice(self.__pieces)

        self.pid = self.__pieces.index(str)
        self.str = str
        rows = str.split('/')
        self.nrows = len(rows)
        self.ncols = len(rows[0])

        tmp = np.array([list(l) for l in list(str.split('/'))])
        tmp = np.where(tmp=='.', 1, tmp)
        tmp = np.where(tmp==' ', 0, tmp)
        self.bmat = tmp.astype(np.int16).astype(np.bool)

        self.bitmap = []
        self.cells = []
        self.grid = []
        self.points = str.count('.')

        for r in range(self.nrows):
            row = []
            bits = 0
            for c in range(self.ncols):
                bits <<= 1
                cell = Cell(r, c, 0, rows[r][c] == '.')

                row.append(cell)
                bits += 1
                self.cells.append(cell)
            self.grid.append(row)
            self.bitmap.append(bits)


    def __repr__(self):
        return "<Piece pid:{} '{}' bits={} size={},{}>".format(self.pid, self.str, self.bitmap,
                                                               self.nrows, self.ncols)

    def __str__(self):
        return "<Piece pid:{} '{}' {} size={},{}>".format(self.pid, self.str, self.bitmap,
                                                          self.nrows, self.ncols)

    def draw(self, id=None):
        if id is None:
            filled = '[ ]'
        else:
            filled = '[' + str(id) + ']'

        for r in range(self.nrows):
            for c in range(self.ncols):
                print(filled if self.grid[r][c].isFilled() else '   ', end = '')
            print('')


    def getSize(self):
        return self.nrows, self.ncols


    def getPoints(self):
        return self.points


    def getGrid(self):
        return self.grid


    def getCells(self):
        return self.cells


    def getBits(self):
        return self.bitmap

    @staticmethod
    def getPieces():
        return list(Piece.pieces.values())

