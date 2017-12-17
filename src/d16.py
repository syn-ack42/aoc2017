import re


class CPU(object):
    def __init__(self, memsize, instructions):
        self.memsize = memsize
        self.instructions = instructions
        self.pars_inst()
        self.mem = [chr(x) for x in range(97, 97 + memsize)]
        self.orig_mem = self.mem
        self.ops = None
        self.mutations = { x: x for x in self.mem }
        self.translations = []

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



    def run(self):
        # for i in self.instructions:
        #     getattr(self, i[0])(i[1], i[2])
        if not self.translations:
            self.detect_op()
        self.run_op()


    def detect_op(self):
        for i in self.instructions:
            if i[0]=="s" or i[0]=="x":
                getattr(self, i[0])(i[1], i[2])
            else:
                kx =None
                ky = None
                for k, v in self.mutations.items():
                    if v == i[1]:
                        kx = k
                    if v == i[2]:
                        ky = k
                self.mutations[kx] = i[2]
                self.mutations[ky] = i[1]

        for i in range(self.memsize):
            comes_from = self.orig_mem.index(self.mem[i])
            self.translations.append(comes_from)

        self.mem = [chr(x) for x in range(97, 97 + self.memsize)]


    def run_op(self):
        new = []
        for comes_from in self.translations:
            new.append(self.mutations[self.mem[comes_from]])
        self.mem = new
        # for i in range(len(self.mem)):
        #     self.mem[i] = self.mutations[self.mem[i]]



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
    firstpattern = ["".join(c.mem)]
    max = 1000000000
    i = 0
    while i < max:
        c.run()

        # # if "".join(c.mem) == firstpattern:
        # #     print("found {} again after {} runs".format("".join(c.mem), i))
        # #     max = max % i
        #     i = 0
        if i % 100000 == 0:
            print("loop {}".format(i))
        i += 1
    return "".join(c.mem)
