import unittest
from board import Board
from pieces import Piece
from players import LRPlayer

class BlokuTest(unittest.TestCase):
    def test_getMoves(self):

        board = Board([200, 385, 112, 129, 4, 145, 128, 1, 259])
        board.draw()

        pieces = []
        pieces.append(Piece('.  /.../.  '))
        pieces.append(Piece('  ./  ./...'))
        pieces.append(Piece('./././.'))
        for i in range(len(pieces)):
            print("Piece {}:".format(i+1))
            pieces[i].draw()
            print('')

        player = LRPlayer()

        moves = player.getMoves(board, pieces)

        for move in moves:
            if move is None:
                print("GAME OVER")
            else:
                (p, r, c) = move
                print("{} to {},{}.".format(p, r + 1, c + 1))
                board.makeMove(p, r, c)
                pieces.remove(p)
                board.draw()

        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
