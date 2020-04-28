from board import Board
from pieces import Piece
from typing import List
import copy


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

        tempBoard = copy.deepcopy(board)
        plist = List(pieces)
        while pick a random piece
        # find all the positions it can fit on the board
        # if not found:
        #     remove from the piece
        # else
        #
