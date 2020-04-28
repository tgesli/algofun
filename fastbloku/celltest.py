import unittest
from cell import Cell
from pieces import Piece
from board import Board

class TestCells(unittest.TestCase):


    def test_init(self):
        c = Cell(6, 4, 7, True)
        self.assertTrue(c.isFilled())
        self.assertEqual(c.getRow(), 6)
        self.assertEqual(c.getCol(), 4)
        self.assertEqual(c.getBox(), 7)

    def test_toString(self):
        c = Cell(6, 4, 7, True)
        cstr = c.__repr__()
        self.assertEqual(cstr, '[Cell(row:6, col:4, box:7) full]')


class TestPieces(unittest.TestCase):

    def test_init(self):
        p = Piece('../. ')
        self.assertEqual(p.nrows, 2)
        self.assertEqual(p.ncols, 2)
        self.assertTrue(p.cells[0][1].isFilled())
        self.assertFalse(p.cells[1][1].isFilled())


class TestBoard(unittest.TestCase):

    def test_findRoomForPiece(self):
        b = Board()
        p = Piece('.')
        plist = b.findRoomForPiece(p)
        print(plist)
        self.assertEqual(len(plist), 81)


if __name__ == '__main__':
    unittest.main()
