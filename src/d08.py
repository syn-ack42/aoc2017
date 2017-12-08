import re

class CPU(object):
    def __init__(self, program):
        self.program = program
        self.inst_ptr = 0
        self.registers = {}
        self.max_seen_val = None

    def run(self):
        while self.inst_ptr < len(self.program):
            self.step()
            print(" ".join(sorted([ "{}->{}".format(k, v) for k, v in self.registers.items()])))

    def largest_reg_val(self):
        max = None
        for k, v in self.registers.items():
            if (max is None) or (v > max):
                max = v
        return max

    def step(self):
        reg, inst, inst_val, cmp_reg, cond_f, cond_val = self.parse_inst(self.program[self.inst_ptr])
        c_f = self.__getattribute__(cond_f)
        if c_f(cmp_reg, cond_val):
            inst_f = self.__getattribute__(inst)
            inst_f(reg, inst_val)
            v = self.registers[reg]
            if (self.max_seen_val is None) or (v > self.max_seen_val):
                self.max_seen_val = v

        self.inst_ptr += 1

    def inc(self, reg, val):
        if not (reg in self.registers):
            self.registers[reg] = 0
        self.registers[reg] += val

    def dec(self, reg, val):
        if not (reg in self.registers):
            self.registers[reg] = 0
        self.registers[reg] -= val

    def greater(self, reg, val):
        if not (reg in self.registers):
            self.registers[reg] = 0
        return self.registers[reg] > val
    def smaller(self, reg, val):
        if not (reg in self.registers):
            self.registers[reg] = 0
        return self.registers[reg] < val
    def greater_eq(self, reg, val):
        if not (reg in self.registers):
            self.registers[reg] = 0
        return self.registers[reg] >= val
    def smaller_eq(self, reg, val):
        if not (reg in self.registers):
            self.registers[reg] = 0
        return self.registers[reg] <= val
    def eq(self, reg, val):
        if not (reg in self.registers):
            self.registers[reg] = 0
        return self.registers[reg] == val
    def neq(self, reg, val):
        if not (reg in self.registers):
            self.registers[reg] = 0
        return self.registers[reg] != val


    def parse_inst(self, inst):
        r = re.match("(\w+) (\w+) (\-?\d+) if (\w+) (\S+) (\-?\d+)", inst)
        reg = r.group(1)
        inst = r.group(2)
        inst_val = int(r.group(3))
        cmp_reg = r.group(4)

        cond_f = r.group(5)
        if cond_f == ">":
            cond_f = "greater"
        elif cond_f == "<":
            cond_f = "smaller"
        elif cond_f == ">=":
            cond_f = "greater_eq"
        elif cond_f == "<=":
            cond_f = "smaller_eq"
        elif cond_f == "==":
            cond_f = "eq"
        elif cond_f == "!=":
            cond_f = "neq"

        cond_val = int(r.group(6))

        return reg, inst, inst_val, cmp_reg, cond_f, cond_val



def run_1(inp):
    """
>>> from src import d08
>>> inp = '''b inc 5 if a > 1
... a inc 1 if b < 5
... c dec -10 if a >= 1
... c inc -20 if c == 10'''
>>> d08.run_1(inp)
a->0
a->1 b->0
a->1 b->0 c->10
a->1 b->0 c->-10
1
    """
    c = CPU(inp.splitlines())
    c.run()
    return c.largest_reg_val()


def run_2(inp):
    """
>>> from src import d08
>>> inp = '''b inc 5 if a > 1
... a inc 1 if b < 5
... c dec -10 if a >= 1
... c inc -20 if c == 10'''
>>> d08.run_2(inp)
a->0
a->1 b->0
a->1 b->0 c->10
a->1 b->0 c->-10
10
    """
    c = CPU(inp.splitlines())
    c.run()
    return c.max_seen_val
