import re


class CPU(object):
    def __init__(self, instructions, ident=None, max_register="z"):
        self.raw_instructions = instructions
        self.instructions = self.parse_inst(instructions)
        self.registers = {chr(x): 0 for x in range(ord('a'), ord(max_register) + 1)}
        self.inst_ptr = 0
        self.id = ident
        self.terminated = False

    def parse_inst(self, instructions):
        ret = []
        for i in range(len(instructions)):
            r = re.match("^(\w\w\w) (([a-z]+)|(-?\d+))( (([a-z]+)|(-?\d+)))?", instructions[i])
            f = getattr(self, r.group(1))
            x_r = r.group(3)
            x_i = int(r.group(4)) if r.group(4) else None
            y_r = r.group(7)
            y_i = int(r.group(8)) if r.group(8) else None
            ret.append((f, x_r, x_i, y_r, y_i))
        return ret

    def step(self):
        if self.terminated:
            return False

        i = self.instructions[self.inst_ptr]
        if not i[0](i[1], i[2], i[3], i[4]):
            return False

        self.inst_ptr += 1

        if self.inst_ptr >= len(self.instructions):
            self.terminated = True
            return False

        return True

    def set(self, x_r, x_i, y_r, y_i):
        self.registers[x_r] = self.registers[y_r] if (y_i is None) else y_i
        return True

    def add(self, x_r, x_i, y_r, y_i):
        self.registers[x_r] += self.registers[y_r] if (y_i is None) else y_i
        return True

    def mul(self, x_r, x_i, y_r, y_i):
        self.registers[x_r] *= self.registers[y_r] if (y_i is None) else y_i
        return True

    def mod(self, x_r, x_i, y_r, y_i):
        self.registers[x_r] %= self.registers[y_r] if (y_i is None) else y_i
        return True

    def run(self):
        while self.step():
            pass
        self.terminated = True

class CPU18(CPU):
    def __init__(self, instructions, ident=None):
        super().__init__(instructions, ident=ident, max_register="z")
        self.last_frequency = None
        if not (ident is None):
            self.registers["p"] = ident
        self.peer = None
        self.queue = []
        self.send_cnt = 0

    def snd(self, x_r, x_i, y_r, y_i):
        if self.id is None:
            self.last_frequency = self.registers[x_r] if (x_i is None) else x_i
            return True
        else:
            v = self.registers[x_r] if (x_i is None) else x_i
            self.peer.queue.insert(0, v)
            self.send_cnt += 1
            return True



    def rcv(self, x_r, x_i, y_r, y_i):
        if self.id is None:
            x = self.registers[x_r] if (x_i is None) else x_i
            if x != 0:
                self.terminated = True
                return False
            return True
        else:
            if len(self.queue)>0:
                self.registers[x_r] = self.queue.pop()
                return True
            else:
                return False

    def jgz(self, x_r, x_i, y_r, y_i):
        x = self.registers[x_r] if (x_i is None) else x_i
        y = self.registers[y_r] if (y_i is None) else y_i
        if x > 0:
            jmp_to = self.inst_ptr + y
            if (jmp_to >= len(self.instructions)) or (jmp_to < 0):
                self.terminated = True
                return False
            self.inst_ptr = jmp_to - 1
        return True



def run_1(inp):
    '''
>>> from src import d18
>>> inp = """set a 1
... add a 2
... mul a a
... mod a 5
... snd a
... set a 0
... rcv a
... jgz a -1
... set a 1
... jgz a -2"""
>>> d18.run_1(inp)
4
    '''
    c = CPU18(inp.splitlines())
    c.run()
    return c.last_frequency


def run_2(inp):
    '''
>>> from src import d18
>>> inp = """snd 1
... snd 2
... snd p
... rcv a
... rcv b
... rcv c
... rcv d"""
>>> c0 = d18.CPU18(instructions=inp.splitlines(), ident=0)
>>> c1 = d18.CPU18(instructions=inp.splitlines(), ident=1)
>>> c0.peer = c1
>>> c1.peer = c0
>>> while True:
...     a = c0.step()
...     b = c1.step()
...     if not (a or b):
...         print(c1.send_cnt)
...         break
3
    '''
    c0 = CPU18(instructions=inp.splitlines(), ident=0)
    c1 = CPU18(instructions=inp.splitlines(), ident=1)
    c0.peer = c1
    c1.peer = c0
    while True:
        a = c0.step()
        b = c1.step()
        if not (a or b):
            return c1.send_cnt
