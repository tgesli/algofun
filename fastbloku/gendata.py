from datetime import datetime
from board import Board
from pieces import Piece
import json
import players


def main():

    board = Board()
    gameOver = False
    player = players.SmartPlayer()
    score = 0
    start = datetime.now()

    file = open("data/bloku.{0:%Y-%m-%d_%H:%M:%S}.json".format(start), "w")
    plist = []
    Piece.initPieces()

    while not gameOver:
        buf = {}
        buf["b"] = board.numList()

        if not plist:
            plist = [Piece.getRandomPiece() for _ in range(3)]

        buf["p"] = [p.numList() for p in plist]

        mList = []
        sList = []

        moves  = player.getMoves(board, plist)
        if moves:
            for move in moves:
                if move is None:
                    gameOver = True
                else:
                    (p, r, c) = move
                    s = board.makeMove(p, r, c)
                    plist.remove(p)
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
