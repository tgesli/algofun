import random
import numpy as np
import math


class Piece:

    piece_str = ['.', '..', '...', '....', '.....', './.', '././.',
                 './././.', '././././.', '. / .', ' ./. ',
                 '.  / . /  .', '  ./ . /.  ', '../..', '../. ',
                 '../ .', '. /..', ' ./..', '.../ . ', ' . /...',
                 '. /../. ', ' ./../ .', '.../ . / . ', ' . / . /...',
                 '.  /.../.  ', '  ./.../  .', '.  /.  /...',
                 '  ./  ./...', '.../.  /.  ', '.../  ./  .',
                 ' ../.. ', '.. / ..', '. /../ .', ' ./../. ',
                 '. ./...', '.../. .', '../. /..', '../ ./..',
                 '../. /. ', '../ ./ .', ' ./ ./..', '. /. /..',
                 '.  /...', '  ./...', '.../.  ', '.../  .', ' . /.../ . '
                 ]
    pieces = {}

    @staticmethod
    def initPieces():
        for p in Piece.piece_str:
            Piece.pieces[p] = Piece(p)


    @staticmethod
    def getRandomPiece():
        return random.choice(list(Piece.pieces.values()))


    @staticmethod
    def bits2ints(mat):
        buf = []
        for r in mat:
            v = 0
            for c in r:
                v <<= 1
                if c:
                    v += 1
            buf.append(v)
        return buf

    @staticmethod
    def int2bits(n, b=0):
        bits = []
        d = 0
        while n:
            bits.insert(0, bool(n % 2))
            n >>= 1
            d += 1

        if b:
            for i in range(b-d):      # always return 9 bits
                bits.insert(0, False)

        return bits

    @staticmethod
    def mat2str(p):
        nBits = int(math.log(max(p), 2)) + 1
        mat = [Piece.int2bits(n, nBits) for n in p]
        buf = ''
        delim = ''
        for r in mat:
            row = ''.join(['.' if c else ' ' for c in r])
            buf += delim + row
            delim = '/'
        return buf


    def __init__(self, str):

        if not str:
            str = random.choice(self.piece_str)

        self.str = str
        rows = str.split('/')
        self.nrows = len(rows)
        self.ncols = len(rows[0])

        tmp = np.array([list(l) for l in list(str.split('/'))])
        tmp = np.where(tmp=='.', 1, tmp)
        tmp = np.where(tmp==' ', 0, tmp)
        self.bmat = tmp.astype(np.int16).astype(np.bool)
        self.points = np.count_nonzero(self.bmat)


    def numList(self):
        return Piece.bits2ints(self.bmat)


    def __str__(self):
        return "Piece <{}>".format(self.str)


    def draw(self, id=None):
        if id is None:
            filled = '[*]'
        else:
            filled = '[' + str(id) + ']'

        for r in range(self.nrows):
            for c in range(self.ncols):
                print(filled if self.bmat[r,c] else '   ', end = '')
            print('')


    def getSize(self):
        return self.nrows, self.ncols


    def getPoints(self):
        return self.points


    def getBits(self):
        return self.bmat

    @staticmethod
    def getPieces():
        return list(Piece.pieces.values())
