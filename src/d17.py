
class Loop(object):
    def __init__(self, step_len = 356):
        self.buffer = [0]
        self.step_len = step_len
        self.cur_pos = 0
        self.cur_size = 1
        self.pos1 = None

    def step(self):
        self.cur_pos = ((self.cur_pos + self.step_len) % self.cur_size) +1
        self.buffer.insert(self.cur_pos, self.cur_size)
        self.cur_size += 1
        # return str(self)

    def step_x(self):
        self.cur_pos = ((self.cur_pos + self.step_len) % self.cur_size) +1
        if self.cur_pos == 1:
            self.pos1 = self.cur_size
        self.cur_size += 1

    def next_to_last(self):
        ntl = (self.cur_pos+1) % self.cur_size
        return self.buffer[ntl]

    def next_to_zero(self):
        if self.pos1:
            return self.pos1
        return self.buffer[1]

    def __str__(self):
        return " ".join([str(x) + ("*" if x == (self.cur_size -1) else "") for x in self.buffer[:self.cur_size]])

def run_1(inp):

    l = Loop(int(inp))
    for i in range(2017):
        l.step()
    print(str(l))
    return l.next_to_last()


def run_2(inp):
    l = Loop(int(inp))
    for i in range(50000000):
        l.step_x()
        if i % 1000 == 0:
            print(str(i))
    return l.next_to_zero()
