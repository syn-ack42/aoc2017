from d18 import CPU

class CPU23(CPU):
    def __init__(self, inst):
        super().__init__(instructions=inst, ident=0, max_register="h")
        self.mulcount = 0
        self.step_cnt = 0

    def mul(self, x_r, x_i, y_r, y_i):
        super().mul(x_r, x_i, y_r, y_i)
        self.mulcount += 1
        return True

    def sub(self, x_r, x_i, y_r, y_i):
        self.registers[x_r] -= self.registers[y_r] if (y_i is None) else y_i
        return True

    def jnz(self, x_r, x_i, y_r, y_i):
        x = self.registers[x_r] if (x_i is None) else x_i
        y = self.registers[y_r] if (y_i is None) else y_i
        if x != 0:
            jmp_to = self.inst_ptr + y
            if (jmp_to >= len(self.instructions)) or (jmp_to < 0):
                self.terminated = True
                return False
            self.inst_ptr = jmp_to - 1
        return True

    def step(self, verbose=False):
        h = self.registers["h"]
        r = super().step()
        if h != self.registers["h"]:
            print("{}: {} !!!".format(self.step_cnt, " ".join(["{}:{}".format(k, v) for k, v in self.registers.items()])))
        self.step_cnt += 1
        if self.step_cnt % 100000 == 0:
            print("{}: {}".format(self.step_cnt, " ".join(["{}:{}".format(k, v) for k, v in self.registers.items()])))
        return r

def run_1(inp):
    c = CPU23(inp.splitlines())
    c.run()
    return c.mulcount


def run_2(inp):
    reduced_pgm = """set b 93
set c b
jnz a 2
jnz 1 5
mul b 100
sub b -100000
set c b
sub c -17000
set f 1
set d 2
set a b
mod a d
jnz a 2
jnz 1 6
sub d -1
set g d
sub g b
jnz g -7
jnz f 2
sub h -1
set g b
sub g c
jnz g 2
jnz 1 3
sub b -17
jnz 1 -17"""
    c = CPU23(reduced_pgm.splitlines())
    c.registers["a"] = 1
    c.run()
    return c.registers["h"]
