from board import Board
from pieces import Piece
from typing import List, Tuple
import copy
import random

from algofun.fastbloku import main


class Player:

    def getMove(self, board:Board, pieces: List[Piece]):
        pass


class HumanPlayer(Player):

    def getMove(self, board:Board, pieces: List[Piece]):
        p=-1
        while p==-1:
            p = int(input("Please enter the piece number:"))
            if p == 0:
                print("GAME OVER")
                return None
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
                return (pieces[p-1], r-1, c-1)
            else:
                print("This is an invalid choice. Try again...")
                r = -1


class RandomPlayer(Player):

    def getMove(self, board:Board, pieces: List[Piece]):

        # tempBoard = copy.deepcopy(board)
        move = None

        plist = [_ for _ in pieces]
        while plist:
            piece = random.choice(plist)
            positions = board.findRoomForPiece(piece)
            if positions:
                row, col = random.choice(positions)
                #position = positions[0]
                break
            else:
                plist.remove(piece)
                piece = None

        if piece is None:
            print("GAME OVER")
        else:
            input("Moving piece {} to {},{}. Press Enter to continue...".format(piece, row+1, col+1))
            move = (piece, row, col)

        return move


class RulePlayer(Player):

    def getMove(self, board:Board, pieces: List[Piece]):

        move = None
        tempboard = copy.deepcopy(board)
        maxscore = 0


        for piece in pieces:
            for row in range(Board.BOARDSIZE):
                for col in range(Board.BOARDSIZE):
                    score = tempboard.makeMove(piece, row, col)
                    if score > 0:  # legal move
                        newhi = 0
                        for p in Piece.getPieces():
                            newhi += len(tempboard.findRoomForPiece(p))
                        if newhi > maxscore:
                            maxscore = newhi
                            move = (piece, row, col)
                        tempboard = copy.deepcopy(board)

        if move is None:
            print("GAME OVER")
        else:
            piece,row,col = move
            print(
                "Maxscore = {}. Moving piece {} to {},{}. Press Enter to continue...".format(maxscore, piece, row + 1, col + 1))

        return move



class BrutePlayer(Player):

    def __init__(self):
        self.moveCount = 0
        self.cachedMoves = []
        self.maxtries = 300


    def getBestMoves(self, board:Board, pieces:List[Piece]):
        tempboard = copy.deepcopy(board)
        bestmove = []
        moves = []
        hiscore = 0

        for piece in pieces:
            h, w = piece.getSize()
            if len(pieces)>1:
                self.moveCount = 0
            for row in range(Board.BOARDSIZE - h + 1):
                for col in range(Board.BOARDSIZE - w + 1):
                    if self.moveCount < self.maxtries:
                        score = tempboard.makeMove(piece, row, col)
                        if score > 0:  # legal move
                            move = (piece, row, col)
                            newhi = 0
                            self.moveCount += 1
                            if self.moveCount == self.maxtries:
                                return hiscore, bestmove
                            rempieces = [p for p in pieces if p != piece]  # todo: move up after first for
                            if rempieces:      # more pieces remain
                                newhi, moves = self.getBestMoves(tempboard, rempieces)

                            else:   # no more pieces
                                for p in Piece.getPieces():
                                    newhi += len(tempboard.findRoomForPiece(p))
                            if newhi > hiscore:
                                hiscore = newhi
                                bestmove = [move] + moves
                        tempboard = copy.deepcopy(board)

        return hiscore, bestmove


    def getMove(self, board:Board, pieces: List[Piece]):

        move = None
        if not self.cachedMoves:
            self.moveCount = 0
            hiscore, self.cachedMoves = self.getBestMoves(board, pieces)

        if self.cachedMoves:
            move = self.cachedMoves.pop(0)
            piece,row,col = move

            main.hor()
            print("Move #{}: {} to {},{}.".
                        format(board.moves, piece, row + 1, col + 1))
        else:
            print("GAME OVER")

        return move



