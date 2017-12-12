"""
  \ n  /
nw +--+ ne
  /    \
-+      +-
  \    /
sw +--+ se
  / s  \
"""


class Node(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0

    def step(self, direction):
        if direction == "ne":
            self.x = self.x + 0
            self.y = self.y - 1
            self.z = self.z + 1
        elif direction == "n":
            self.x = self.x - 1
            self.y = self.y - 0
            self.z = self.z + 1
        elif direction == "nw":
            self.x = self.x - 1
            self.y = self.y + 1
            self.z = self.z + 0
        elif direction == "sw":
            self.x = self.x - 0
            self.y = self.y + 1
            self.z = self.z - 1
        elif direction == "s":
            self.x = self.x + 1
            self.y = self.y + 0
            self.z = self.z - 1
        elif direction == "se":
            self.x = self.x + 1
            self.y = self.y - 1
            self.z = self.z + 0


    def distance(self):

        return max(abs(self.x), abs(self.y),abs(self.z))


def run_1(inp):
    """
    >>> from src import d11
    >>> d11.run_1("ne,ne,ne")
    3
    >>> d11.run_1("ne,ne,sw,sw")
    0
    >>> d11.run_1("ne,ne,s,s")
    2
    >>> d11.run_1("se,sw,we,sw,sw")
    3
   """
    inp = inp.split(",")
    n = Node()
    for i in inp:
        n.step(i)
    return n.distance()


def run_2(inp):
    inp = inp.split(",")
    n = Node()
    furthest = 0
    for i in inp:
        n.step(i)
        d = n.distance()
        if d > furthest:
            furthest = d
    return furthest
