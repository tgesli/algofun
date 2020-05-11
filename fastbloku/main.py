from datetime import datetime
from board import Board
from pieces import Piece
import players

def hor():
    print("---------------------------")

def main():

    board = Board()
    gameOver = False
    player = players.LRPlayer()
    pieces = []
    score = 0
    start = datetime.now()
    Piece.init_pieces()

    hor()
    board.draw()

    while not gameOver:

        if not pieces:
            pieces = [Piece.getRandomPiece() for _ in range(3)]

        hor()
        for i in range(len(pieces)):
            print("Piece {}:".format(i+1))
            pieces[i].draw()
            print('')

        moves = player.getMoves(board, pieces)
        for move in moves:
            if move is None:
                gameOver = True
                print("GAME OVER")
            else:
                (p, r, c) = move
                hor()
                print("Move #{}: {} to {},{}.".
                      format(board.moveCount, p, r + 1, c + 1))
                score += board.makeMove(p, r, c)

                pieces.remove(p)
                hor()
                print("Current score: {}".format(score))
                board.draw()

    print("Final score = {}".format(score))
    print("Total moves = {}".format(board.moveCount))
    print("Start time: {} \nEnd time: {}".format(start, datetime.now()))

if __name__ == '__main__':
    main()
