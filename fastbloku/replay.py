from datetime import datetime

from board import Board
from pieces import Piece
import json

import players

def hor():
    print("---------------------------")

def main():

    file = open("/Users/tolga/src/algofun/fastbloku/data/bloku.2020-05-04_20:05:34.json", "r")
    data = []
    with file as f:
        for l in f:
            data.append(json.loads(l))

    score = 0
    board = Board()
    hor()
    board.draw()

    for rec in data:
        board = Board(rec["b"])
        pieces = [Piece(Piece.mat2str(p)) for p in rec["p"]]
        hor()
        hor()
        hor()
        for i in range(len(pieces)):
            print("Piece {}:".format(i + 1))
            pieces[i].draw()
            print('')

        moves = rec["m"]
        scores = rec["s"]

        hor()
        for i in range(len(moves)):
            p,r,c = moves[i]
            print("Move {}:".format(i + 1))
            p = Piece(Piece.mat2str(p))
            p.draw()
            print('To {}, {}'.format(r+1,c+1))
            hor()
            board.makeMove(p,r,c)
            board.draw()
            score += scores[i]
            print("Move Score: {}   Total Score: {}".format(scores[i], score))


if __name__ == '__main__':
    main()
