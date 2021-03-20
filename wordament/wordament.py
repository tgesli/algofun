
def is_valid_coordinate(c):
    return c>=0 and c<=3

class Dictionary :

    def __init__(self, file_name):
        with open(file_name) as f:
            self.words = f.readlines()

    def get_words(self):
        return self.words


class Tile :
    letter_values = { 'a': 2, 'b': 5, 'c': 3, 'd': 3, 'e': 1, 'f': 5, 'g': 4, 'h': 4, 'i': 2,
                      'j': 8, 'k': 6, 'l': 3, 'm': 4, 'n': 2, 'o': 2, 'p': 4, 'q': 8, 'r': 2,
                      's': 2, 't': 2, 'u': 4, 'v': 6, 'w': 6, 'x': 9, 'y': 5, 'z': 8 }

    def __init__(self, str, value=0):
        self.str = str
        if len(str) == 1:
            self.type = 'Letter'
        elif str[1] == '/':
            self.type = 'Either'
        elif str[-1] == '-':
            self.type = 'Starts'
        elif len(str) > 1:
            self.type = 'Digram'

        if value == 0 and self.type == 'Letter':
            if self.str.isupper():
                self.str = self.str.lower()
                value = 10
            else:
                value = Tile.letter_values[str]

        self.value = value

    def __str__(self):
        return f"<{self.str} ({self.value})>"

    def get_str(self):
        return self.str

    def get_value(self):
        return self.value


class Puzzle :

    def __init__(self, puzzle):
        self.tiles = []
        # tiles = puzzle.split(',')
        tiles = list(puzzle)
        for r in range(4):
            row = [Tile(tiles[r*4 + c]) for c in range(4)]
            self.tiles.append(row)

    def show(self):
        for r in self.tiles:
            for c in r:
                print(c, end=' ')
            print()

    def find_tile(self, str):
        res = []
        for r in range(4):
            for c in range(4):
                if self.tiles[r][c].str == str:
                    res.append((r,c))
        return res

    def get_neighbors(self, loc):
        neighbors = []
        for yoff in range(-1, 2):
            for xoff in range(-1, 2):
                y = loc[0] + yoff
                x = loc[1] + xoff
                if is_valid_coordinate(x) and is_valid_coordinate(y):
                    neighbors.append((y, x))
        return neighbors

    def get_tile(self, loc):
        r,c = loc
        return self.tiles[r][c]

    def find_rest(self, s, path):
        if s:
            for loc in self.get_neighbors(path[-1]):
                if loc not in path and self.get_tile(loc).get_str() == s[0]:
                    new_path = self.find_rest(s[1:], path + [loc])
                    if new_path:
                        return new_path
            return []  # not found
        else:
            return path

    def find(self, w):
        for loc in self.find_tile(w[0]):
            path = self.find_rest(w[1:], [loc])
            if path:
                return path
        return []  # not found

    def solve(self, d: Dictionary):
        solutions = []
        for w in d:
            w = w.rstrip('\n')
            if len(w) > 2:
                p = self.find(w)
                if p:
                    pts = 0
                    for l in p:
                        pts += self.get_tile(l).get_value()
                    factor = 1
                    if len(p) > 7:
                        factor = 2.5
                    elif len(p) > 5:
                        factor = 2
                    elif len(p) == 4:
                        factor = 1.5
                    solutions.append((w, p, int(factor*pts)))
        return solutions

def sort_results(res):
    res.sort(key=lambda x: x[2], reverse=True)
    return res


#------------ Execution start ---------------
def test_points():
    points = { 'thurible': 57,
               'bluets': 34,
               'billie': 32,
               'ruliest': 32,
               'rustle': 28,
               'hurtle': 32,
               'shrill': 32,
               'arranges': 42,
               'amnesia': 30,
               'faring': 34,
               'karamu': 40,
               'fakes': 24,
               'slit': 9,
               'spin': 10,
               'tan': 6,
               'ran': 6,
               'brominisms': 67,
               'soprano': 36
               }

    for w in points:
        p=points[w]
        tiles = [ Tile(c) for c in w ]
        tot = sum(t.get_value() for t in tiles)
        print(f"{w:16} total={tot}  len={len(tiles)}  point={p}")

def cheat():
    dict = Dictionary('wordlist.txt')

    while True:
        puzzle = input('Enter puzzle:')
        if puzzle == '':
            exit(0)

        puzzle = Puzzle(puzzle)
        puzzle.show()

        print(f"searching for {len(dict.get_words())} words...")
        sols = sort_results(puzzle.solve(dict.get_words()))

        print(f"Found {len(sols)} solutions:")
        cnt = 0
        tot = 0
        for w, p, pts in sols:
            print(f"{pts} {w}")
            cnt += 1
            tot += pts
            if cnt == 40:
                break
        print(f"total={tot}")
def main():
    cheat()

if __name__ == '__main__':
    main()
