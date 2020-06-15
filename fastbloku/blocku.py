import players
from pieces import Piece
from board import Board


def randomPieceGenerator():
    return [Piece.getRandomPiece() for _ in range(3)]


def getPiecesFromConsole():
    plist = []
    i = 0
    for p in Piece.pieces:
        print('{}: {}'.format(i, p))
        i += 1
    s = input("Enter the 3 pieces, delimited by space:")
    pidList = [int(id) for id in s.split()]
    for pid in pidList:
        plist.append(Piece.pieces[Piece.__piece_str[pid]])
    return plist


class Blocku:

    def __init__(self, player, pieceSource="random"):
        self.board = Board()
        self.gameOver = False
        self.player = player

        self.pieces = []
        self.score = 0

        Piece.initPieces()
        if pieceSource=="random":
            self.pieceGenerator = randomPieceGenerator
        elif pieceSource == "console":
            self.pieceGenerator = getPiecesFromConsole
        else:
            raise RuntimeError("Invalid parameter pieceSource={}".format(pieceSource))


    @staticmethod
    def horizontalLine(len):
        print(len*'-')


    def displayGameState(self):
        self.horizontalLine(40)
        print("Current score: {}".format(self.score))
        self.board.draw()
        for i in range(len(self.pieces)):
            print("Piece {}:".format(i + 1))
            self.pieces[i].draw()
            print('')


    def displayMove(self, move):
        (p, r, c) = move
        self.horizontalLine(40)
        print("Move #{}:".format(self.board.moveCount))
        p.draw()
        print("place at row {}, column {}.".format(r + 1, c + 1))


    def run(self):
        while not self.gameOver:
            if not self.pieces:
                self.pieces = self.pieceGenerator()
            self.displayGameState()
            moves = self.player.getMoves(self.board, self.pieces)
            for move in moves:
                if move is None:
                    self.gameOver = True
                else:
                    (p, r, c) = move
                    self.score += self.board.makeMove(p, r, c)
                    self.displayMove(move)
                    self.pieces.remove(p)
                    self.displayGameState()

        print("GAME OVER")
        return {"score": self.score,
                "moves": self.board.moveCount
               }
