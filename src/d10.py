

class Loop(object):
    def __init__(self, lengths=None, loop_len = 256, inp_str=None):
        self.loop_len = loop_len
        self.nodes = list(range(loop_len))
        self.lengths = lengths
        self.current = 0
        self.skip = 0
        self.dense_hash = []
        self.inp_str = inp_str
        if lengths is None:
            self.lengths = [ord(c) for c in inp_str]
            self.lengths += [17, 31, 73, 47, 23]

    def run(self):
        #print(",".join([str(x) for x in self.nodes]))
        for l in self.lengths:
            self.step(l)

    def run_full(self):
        for i in range(64):
            # l.reset()
            self.run()

    def checksum(self):
        return self.nodes[0] * self.nodes[1]

    def step(self, length):
        if length > self.loop_len:
            return
        slice_end = (self.current + length) % self.loop_len
        if slice_end > self.current:
            sublist = self.nodes[self.current:slice_end]
            sublist = list(reversed(sublist))
            self.nodes[self.current: slice_end] = sublist
        elif slice_end < self.current:
            sublist = self.nodes[self.current:] + self.nodes[:slice_end]
            sublist = list(reversed(sublist))
            cutoff = (self.loop_len - self.current)
            self.nodes[self.current:] = sublist[:cutoff]
            self.nodes[:slice_end] = sublist[cutoff:]

        self.current += (length + self.skip)
        self.current = self.current % self.loop_len
        self.skip += 1

        #print(",".join([str(x) for x in self.nodes]))

    def reset(self):
        self.nodes = list(range(self.loop_len))

    def make_dense_hash(self, blocksize=16):
        cnt = 0
        line = 0
        for n in self.nodes:
            cnt += 1
            line = line ^ n
            if cnt == blocksize:
                self.dense_hash.append(line)
                cnt = 0
                line = 0

    def repr_dense_hash(self):
        self.make_dense_hash()
        tmp = ["{:x}".format(x) for x in self.dense_hash]
        tmp = [x.zfill(2) for x in tmp]
        return "".join(tmp)



def run_1(inp, loop_len=256):
    inp = inp.split(",")
    inp = [int(x) for x in inp]
    #print(",".join([str(x) for x in inp]))
    l = Loop(inp, loop_len)
    l.run()
    return l.checksum()


def run_2(inp, loop_len=256):
    """
    >>> from src import d10
    >>> d10.run_2("")
    'a2582a3a0e66e6e86e3812dcb672a272'
    >>> d10.run_2("AoC 2017")
    '33efeb34ea91902bb2f59c9920caa6cd'
    >>> d10.run_2("1,2,3")
    '3efbe78a8d82f29979031a4aa0b16a9d'
    >>> d10.run_2("1,2,4")
    '63960835bcdc130f0b66d7ff4f6a5a8e'
    """

    l = Loop(inp_str=inp, loop_len=loop_len)

    l.run_full()

    l.make_dense_hash()
    return l.repr_dense_hash()