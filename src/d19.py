

class Maze(object):
    def __init__(self, inp):
        self.raw_inp = inp
        rows = inp.splitlines()
        self.width = len(rows[0])
        self.height = len(rows)
        self.maze = []
        for l in rows:
            if self.width < len(l):
                self.width = len(l)
            ln = list(l)
            self.maze.append(ln)

        for i in range(len(self.maze)):
            if len(self.maze[i]) < self.width:
                self.maze[i] += [" "] * (self.width - len(self.maze[i]))

        self.entry_x = self.maze[0].index("|")
        self.entry_y = 0

    def pipe_at(self, x, y):
        if (x >= self.width) or (x < 0) or (y >= self.height) or (y < 0):
            return False
        else:
            return self.maze[y][x]

    def next_pos(self, x, y, dir):
        squish = None
        wiggle = None
        if dir == "S":
            squish = (0, 1)
            wiggle = (1, 0)
            bend = ("E", "W")
        elif dir == "N":
            squish = (0, -1)
            wiggle = (1, 0)
            bend = ("E", "W")
        elif dir == "E":
            squish = (1, 0)
            wiggle = (0, 1)
            bend = ("S", "N")
        elif dir == "W":
            squish = (-1, 0)
            wiggle = (0, 1)
            bend = ("S", "N")

        p = self.pipe_at(x + squish[0], y + squish[1])
        if ((p==" ") or (p== False)):
            p = self.pipe_at(x + wiggle[0], y + wiggle[1])
            if not ((p==" ") or (p== False)):
                return x + wiggle[0], y + wiggle[1], p, bend[0]

            p = self.pipe_at(x - wiggle[0], y - wiggle[1])
            if not ((p==" ") or (p== False)):
                return x - wiggle[0], y - wiggle[1], p, bend[1]

            raise RuntimeWarning("Done")
            #raise RuntimeError("dead end x {} y {} dir {}".format(x, y, dir))
        else:
            return x + squish[0], y + squish[1], p, dir


class Seeker(object):
    def __init__(self, maze):
        self.maze = maze
        self.x = maze.entry_x
        self.y = maze.entry_y
        self.direction = "S"
        self.travelog = []

    def seek(self):
        try:
            self.x, self.y, character, self.direction = self.maze.next_pos(self.x, self.y, self.direction)
            if not (character in ("+", "|", "-", False)):
                self.travelog.append(character)
            return False
        except RuntimeWarning:
            return "".join(self.travelog)


def run_1(inp):
    """
>>> from src import d19
>>> inp = '''     |
...      |  +--+
...      A  |  C
...  F---|----E|--+
...      |  |  |  D
...      +B-+  +--+
...
... '''
>>> d19.run_1(inp)
'ABCDEF'
    """
    m = Maze(inp)
    s = Seeker(m)
    i = 0
    while s.seek() == False:
        i += 1
        #print("{}: x {} y {} d {}".format(i, s.x, s.y, s.direction))
    return "".join(s.travelog)


def run_2(inp):
    """
>>> from src import d19
>>> inp = '''     |
...      |  +--+
...      A  |  C
...  F---|----E|--+
...      |  |  |  D
...      +B-+  +--+
...
... '''
>>> d19.run_2(inp)
38
    """
    m = Maze(inp)
    s = Seeker(m)
    i = 0
    while s.seek() == False:
        i += 1
        # print("{}: x {} y {} d {}".format(i, s.x, s.y, s.direction))
    return i + 1