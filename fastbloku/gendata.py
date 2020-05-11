from datetime import datetime
from board import Board
from pieces import Piece
import json
import players


def main():

    board = Board()
    gameOver = False
    player = players.LRPlayer()
    score = 0
    start = datetime.now()

    file = open("data/bloku.{0:%Y-%m-%d_%H:%M:%S}.json".format(start), "w")
    pieces = []

    while not gameOver:
        buf = {}
        buf["b"] = board.numList()

        if not pieces:
            pieces = [Piece.getRandomPiece() for _ in range(3)]

        buf["p"] = [p.numList() for p in pieces]

        mList = []
        sList = []

        moves  = player.getMoves(board, pieces)
        if moves:
            for move in moves:
                if move is None:
                    gameOver = True
                else:
                    (p, r, c) = move
                    s = board.makeMove(p, r, c)
                    pieces.remove(p)
                    score += s
                    mList.append((p.numList(), r, c))
                    sList.append(s)
                    progress(board.moveCount)

        buf["m"] = mList
        buf["s"] = sList

        file.write(json.dumps(buf) + '\n')
        file.flush()

    print("\nFinal score = {}".format(score))
    print("Total moves = {}".format(board.moveCount))
    print("Start time: {} \nEnd time: {}".format(start, datetime.now()))


def progress(m):
    print('.', end='' if m % 100 else '\n')

if __name__ == '__main__':
    main()
