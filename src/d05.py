

def run_1(inp):
    '''
>>> from src import d05
>>> inp = """0
... 3
... 0
... 1
... -3"""
>>> d05.run_1(inp)
5
    '''
    instructions = [int(i) for i in inp.splitlines()]
    cpu = CPU(instructions)

    while cpu.step():
        pass

    return cpu.inst_cnt

def run_2(inp):
    '''
>>> from src import d05
>>> inp = """0
... 3
... 0
... 1
... -3"""
>>> d05.run_2(inp)
10
    '''
    instructions = [int(i) for i in inp.splitlines()]
    cpu = CPU(instructions)
    cpu.hobblestep = True

    while cpu.step():
        pass

    return cpu.inst_cnt


class CPU(object):
    def __init__(self, instructions):
        self.instructions = instructions
        self.inst_ptr = 0
        self.inst_cnt = 0
        self.hobblestep = False

    def step(self):
        self.inst_cnt += 1
        steps = self.instructions[self.inst_ptr]
        n_ptr = self.inst_ptr + steps
        self.instructions[self.inst_ptr] += self.step_modifier()
        self.inst_ptr = n_ptr

        if n_ptr >= len(self.instructions):
            return False
        else:
            return True

    def step_modifier(self):
        if self.hobblestep:
            if self.instructions[self.inst_ptr] >= 3:
                return -1
        return 1

    def __str__(self):
        s = "{}: ptr: {} mem: {}".format(self.inst_cnt, self.inst_ptr, " ".join([str(x) for x in self.instructions]))
        return s

