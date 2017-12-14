from d10 import Loop

def hex2bin(inp):
    return bin(int(inp, 16))[2:].zfill(128)


class Node(object):
    regions = 0
    nodes = {}
    def __init__(self, x, y, occupied):
        self.gridlimit = 128
        self.x = x
        self.y = y
        self.occupied = occupied
        self.region = None
        self.nodes["{}-{}".format(x,y)] = self

    def discover(self, region=None):
        if not self.occupied:
            return
        if region is None:
            Node.regions += 1
            self.region = Node.regions
        else:
            if not (self.region is None):
                if self.region == region:
                    return
                else:
                    raise RuntimeError("screwed")

            self.region = region

        if self.x > 0:
            self.nodes["{}-{}".format(self.x -1, self.y)].discover(region=self.region)
        if self.x < (self.gridlimit -1):
            self.nodes["{}-{}".format(self.x + 1, self.y)].discover(region=self.region)
        if self.y > 0:
            self.nodes["{}-{}".format(self.x, self.y -1)].discover(region=self.region)
        if self.y < (self.gridlimit -1):
            self.nodes["{}-{}".format(self.x, self.y + 1)].discover(region=self.region)


def init_grid(inp):
    gridlines = []

    for i in range(128):
        l = Loop(inp_str="{}-{}".format(inp, i))
        l.run_full()

        gridlines.append(l)

    grid_strs = [s.repr_dense_hash() for s in gridlines]
    grid_strs = [hex2bin(s)for s in grid_strs]

    return gridlines, grid_strs

def run_1(inp):
    """
>>> from src import d14
>>> d14.run_1("flqrgnkx")
8108"""
    gridlines, grid_strs = init_grid(inp)
    res_str = "\n".join(grid_strs)
    return res_str.count("1")

def run_2(inp):
    """
>>> from src import d14
>>> d14.run_2("flqrgnkx")
1242"""
    gridlines, grid_strs = init_grid(inp)

    nodes = []
    y = 0
    for l in grid_strs:
        x = 0
        for n in l:
            if n in ("0", "1"):
                nodes.append(Node(x, y, occupied=(n == "1")))
            x +=1
        y += 1
    for n in nodes:
        if (n.occupied) and (n.region is None):
            n.discover()
    return Node.regions