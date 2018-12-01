from collections import OrderedDict


class Tape(object):
    def __init__(self):
        self.slots = {}
        self.slots[0] = 0

    def store(self, pos, val):
        self.slots[pos] = val

    def retreive(self, pos):
        return self.slots.get(pos, 0)

    def count_ones(self):
        k = 0
        for _, v in self.slots.items():
            k += v
        return k

    def __str__(self):
        minp = 0
        maxp = 0
        for k, v in self.slots.items():
            if k < minp:
                minp = k
            if k > maxp:
                maxp = k
        exp_tape = []
        for j in range(minp, maxp+1):
            exp_tape.append(str(self.retreive(j)))
        return " ".join(exp_tape)


class TMachine(object):
    states = {
        "A": {
            0: {"v": 1, "d": 1, "s": "B"},
            1: {"v": 0, "d": -1, "s": "C"},
        },
        "B": {
            0: {"v": 1, "d": -1, "s": "A"},
            1: {"v": 1, "d": 1, "s": "D"},
        },
        "C": {
            0: {"v": 1, "d": 1, "s": "A"},
            1: {"v": 0, "d": -1, "s": "E"},
        },
        "D": {
            0: {"v": 1, "d": 1, "s": "A"},
            1: {"v": 0, "d": 1, "s": "B"},
        },
        "E": {
            0: {"v": 1, "d": -1, "s": "F"},
            1: {"v": 1, "d": -1, "s": "C"},
        },
        "F": {
            0: {"v": 1, "d": 1, "s": "D"},
            1: {"v": 1, "d": 1, "s": "A"},
        },
    }

    def __init__(self, tape=Tape()):
        self.tape = tape
        self.pos = 0
        self.ticks = 0
        self.state = "A"

    def tick(self):
        cv = self.tape.retreive(self.pos)
        inst = TMachine.states[self.state][cv]
        self.tape.store(self.pos, inst["v"])
        self.pos += inst["d"]
        self.state = inst["s"]

def  run_1(inp, verbose = False):
    """
>>> from src import d25
>>> d25.TMachine.states = {
...         "A": {
...             0: {"v": 1, "d": 1, "s": "B"},
...             1: {"v": 0, "d": -1, "s": "B"},
...         },
...         "B": {
...             0: {"v": 1, "d": -1, "s": "A"},
...             1: {"v": 1, "d": 1, "s": "A"},
...         }
...     }
>>> d25.run_1(6)
3
    """
    loops = int(inp)
    machina = TMachine()
    for i in range(loops):
        machina.tick()

        if verbose:
            print("{}: {}".format(i, machina.tape))
    return machina.tape.count_ones()


def run_2(inp):
    pass