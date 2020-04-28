from board import Board
from cell import Cell
from pieces import Piece
import players

def main():

    board = Board()
    gameOver = False
    # player = HumanPlayer()
    player = players.BrutePlayer()
    pieces = []
    score = 0

    while not gameOver:

        print("Current score: {}".format(score))
        board.draw()
        board.resetFresh()

        if not pieces:
            pieces = [Piece.getRandomPiece() for _ in range(3)]

        for i in range(len(pieces)):
            print("Piece {}:".format(i+1))
            pieces[i].draw(i)

        move = player.getMove(board, pieces)
        if move is None:
            gameOver = True
        else:
            (p, r, c) = move
            score += board.makeMove(p, r, c)
            pieces.remove(p)

    print("Final score = {}".format(score))

if __name__ == '__main__':
    main()
