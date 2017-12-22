import numpy


class Worm(object):
    def __init__(self, mapstr):
        map = mapstr.splitlines()
        t = int(len(map)/2)
        self.pos = numpy.array([t, t])
        self.v = numpy.array([0, -1])
        self.infection_count = 0
        self.epi_list = {}
        self.init_epilist(map)

    def init_epilist(self, map):
        for y in range(len(map)):
            for x in range(len(map)):
                if map[y][x] == "#":
                    self.epi_list["{}.{}".format(x, y)] = "#"

    def turn(self, direction): #left: l, right: r, back: b
        if direction == "l":
            rot = numpy.array([[0, 1], [-1, 0]])
            self.v = rot @ self.v
        elif direction == "r":
            rot = numpy.array([[0, -1], [1, 0]])
            self.v = rot @ self.v
        elif direction == "b":
            self.v *= -1

    def crawl(self, verbose=False):
        p = "{}.{}".format(self.pos[0], self.pos[1])
        if p in self.epi_list:
            self.turn("r")
            del self.epi_list[p]
        else:
            self.turn("l")
            self.epi_list[p] = "#"
            self.infection_count += 1
        self.pos += self.v
        if verbose:
            self.print_grid()


    def crawl_2(self, verbose=False):
        p = "{}.{}".format(self.pos[0], self.pos[1])
        if p in self.epi_list:
            s = self.epi_list[p]
            if s == "W":
                self.epi_list[p] = "#"
                self.infection_count += 1
            elif s == "#":
                self.epi_list[p] = "F"
                self.turn("r")
            elif s == "F":
                self.turn("b")
                del self.epi_list[p]
        else:
            self.turn("l")
            self.epi_list[p] = "W"

        self.pos += self.v
        if verbose:
            self.print_grid()

    def print_grid(self):
        ma_x = 0
        mi_x = 0
        ma_y = 0
        mi_y = 0

        for k, v in self.epi_list.items():
            p = k.split(".")
            x = int(p[0])
            y = int(p[1])
            if x > ma_x:
                ma_x = x
            if x < mi_x:
                mi_x = x
            if y > ma_y:
                ma_y = y
            if y < mi_y:
                mi_y = y
        map = []
        for y in range(mi_y - 1, ma_y + 2):
            line = []
            for x in range(mi_x - 1, ma_x + 2):
                is_cpos=False
                if (self.pos[0] == x) and (self.pos[1] == y):
                    is_cpos = True
                if "{}.{}".format(x, y) in self.epi_list:
                    c = self.epi_list["{}.{}".format(x, y)]
                    if is_cpos:
                        line.append("({})".format(c))
                    else:
                        line.append(" {} ".format(c))
                else:
                    if is_cpos:
                        line.append("(.)")
                    else:
                        line.append(" . ")
            map.append("".join(line))
        r = "\n" + "\n\n".join(map) + "\n"
        print(r)


def run_1(inp):
    '''
>>> from src import d22
>>> inp = """..#
... #..
... ..."""
>>> w = d22.Worm(inp)
>>> for i in range(70):
...     w.crawl()
>>> w.infection_count
41
>>> w = d22.Worm(inp)
>>> for i in range(10000):
...     w.crawl()
>>> w.infection_count
5587
    '''
    w = Worm(inp)
    for i in range(10000):
        w.crawl()
    return w.infection_count


def run_2(inp):
    '''
>>> from src import d22
>>> inp = """..#
... #..
... ..."""
>>> w = d22.Worm(inp)
>>> for i in range(100):
...     w.crawl_2()
>>> w.infection_count
26
>>> w = d22.Worm(inp)
>>> for i in range(10000000):
...     w.crawl_2()
>>> w.infection_count
2511944
    '''
    w = Worm(inp)
    for i in range(10000000):
        w.crawl_2()
        if (i % 10000 == 0):
            print(i)
    return w.infection_count