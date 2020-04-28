
class Cell:

    def __init__(self, r, c, b, isFilled):
        self.row = r
        self.col = c
        self.box = b
        self.f_or_e = isFilled
        self.fresh = False

    def __repr__(self):
        return "[Cell(row:{}, col:{}, box:{}) {}]".format(self.row, self.col, self.box,
                                                   "full" if self.f_or_e else "empty")

    def __str__(self):
        return "Cell ({}, {}) -- Box {} -- {}".format(self.row, self.col, self.box,
                                                       "full" if self.f_or_e else "empty")

    def picture(self):
        if self.f_or_e:
            if self.fresh:
                return '[.]'
            else:
                return '[#]'
        else:
            return '   '

    def isFilled(self):
        return self.f_or_e


    def isFresh(self):
        return self.fresh


    def getRow(self):
        return self.row


    def getCol(self):
        return self.col


    def getBox(self):
        return self.box


    def setFill(self, isFilled):
        self.f_or_e = isFilled


    def setFresh(self, fresh):
        self.fresh = fresh

