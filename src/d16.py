import re


class CPU(object):
    def __init__(self, memsize, instructions):
        self.memsize = memsize
        self.instructions = instructions
        self.pars_inst()
        self.mem = [chr(x) for x in range(97, 97 + memsize)]
        self.mem_1 = [chr(x) for x in range(97, 97 + memsize)]
        self.orig_mem = list(self.mem)
        self.ops = None
        self.mutations = {x: x for x in self.mem}
        self.translations = []

        self.detect_op()

    def s(self, n, _=None):
        n = int(n)
        a = self.mem[:self.memsize - n]
        b = self.mem[self.memsize - n:]
        self.mem = b + a

    def x(self, a, b):
        a = int(a)
        b = int(b)
        x = self.mem[a]
        self.mem[a] = self.mem[b]
        self.mem[b] = x

    def p(self, x, y):
        px = self.mem.index(x)
        py = self.mem.index(y)
        self.x(px, py)

    def pars_inst(self):
        for i in range(len(self.instructions)):
            r = re.match("(\w)(\w+)(\/?(\w+)+)?", self.instructions[i])
            self.instructions[i] = (r.group(1), r.group(2), r.group(4))

    def test_run(self):
        mem_1 = self.run_op()
        self.run()
        assert self.mem == mem_1

    def run(self):
        for i in self.instructions:
            getattr(self, i[0])(i[1], i[2])

    def run_x(self):
        self.mem = self.run_op()

    def detect_op(self):
        for i in self.instructions:
            getattr(self, i[0])(i[1], i[2])
        t = list(self.mem)
        self.mem = list(self.orig_mem)
        for i in self.instructions:
            if (i[0] == "s") or (i[0] == "x"):
                getattr(self, i[0])(i[1], i[2])

        for i in range(self.memsize):
            comes_from = self.orig_mem.index(self.mem[i])
            self.mutations[self.mem[i]] = t[i]
            self.translations.append(comes_from)
        self.mem = list(self.orig_mem)

    def run_op(self):
        new = []
        for comes_from in self.translations:
            new.append(self.mutations[self.mem[comes_from]])

        return new


def run_1(inp):
    """>>> from  src import d16
>>> c = d16.CPU(5, ["s1", "x3/4", "pe/b"])
>>> c.run()
>>> "".join(c.mem)
'baedc'
    """
    inp = inp.split(",")
    c = CPU(memsize=16, instructions=inp)
    c.run()
    return "".join(c.mem)


def run_2(inp):
    """>>> from  src import d16
    >>> c = d16.CPU(5, ["s1", "x3/4", "pe/b"])
    >>> max = 2
    >>> i = 0
    >>> while i < max:
    ...     c.run()
    ...     i += 1
    ...
    >>> "".join(c.mem)
    'ceadb'
    """
    inp = inp.split(",")
    c = CPU(memsize=16, instructions=inp)

    max = 1000000000
    i = 0
    init = "".join(c.mem)
    while i < max:
        c.run_x()
        if init == "".join(c.mem):
            print("same after {}".format(i))
            max %= (i+1)
            i = 0
            continue

        if i % 1000000 == 0:
            print("loop {}".format(i))
        i += 1
    return "".join(c.mem)
