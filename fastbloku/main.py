from datetime import datetime

from board import Board
from pieces import Piece
import players

def hor():
    print("---------------------------")

def main():

    board = Board()
    gameOver = False
    # player = HumanPlayer()
    player = players.BrutePlayer()
    pieces = []
    score = 0
    start = datetime.now()

    while not gameOver:

        hor()
        print("Current score: {}".format(score))
        hor()
        board.draw()

        if not pieces:
            pieces = [Piece.getRandomPiece() for _ in range(3)]

        hor()
        for i in range(len(pieces)):
            print("Piece {}:".format(i+1))
            pieces[i].draw()
            print('')

        move = player.getMove(board, pieces)
        if move is None:
            gameOver = True
        else:
            (p, r, c) = move
            score += board.makeMove(p, r, c)
            pieces.remove(p)

    print("Final score = {}".format(score))
    print("Total moves = {}".format(board.moves))
    print("Start time: {} \nEnd time: {}".format(start, datetime.now()))

if __name__ == '__main__':
    main()
