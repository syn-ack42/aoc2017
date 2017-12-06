

def run_1(inp):
    '''
>>> from src import d06
>>> inp = """0    2   7   0"""
>>> d06.run_1(inp)
1: 2 4 1 2
2: 3 1 2 3
3: 0 2 3 4
4: 1 3 4 1
5: 2 4 1 2
5
    '''
    memory = [int(i) for i in inp.split()]
    mm = MemMan(memory)

    ret = mm.clean_mem()

    return ret

def run_2(inp):
    '''
>>> from src import d06
>>> inp = """0    2   7   0"""
>>> d06.run_2(inp)
1: 2 4 1 2
2: 3 1 2 3
3: 0 2 3 4
4: 1 3 4 1
5: 2 4 1 2
4
    '''
    memory = [int(i) for i in inp.split()]
    mm = MemMan(memory)

    lcnt = mm.clean_mem()
    loop_state = mm.mem_str()
    first_occurr = mm.states_seen.index(loop_state)

    return lcnt - first_occurr


class MemMan(object):
    def __init__(self, memory):
        self.memory = memory
        self.states_seen = []
        self.states_seen.append(self.mem_str())

    def mem_str(self):
        r = [str(x) for x in self.memory]
        return " ".join(r)

    def clean_mem(self):
        cnt = 0
        for m in self.redistribution():
            cnt += 1
            print("{}: {}".format(cnt, m))
        return cnt

    def redistribution(self):
        while True:
            max_val, max_pos = self.find_first_max()
            mem_ptr = max_pos
            redist_blocks = max_val
            self.memory[mem_ptr] = 0
            while redist_blocks>0:
                mem_ptr = (mem_ptr + 1) % len(self.memory)
                self.memory[mem_ptr] += 1
                redist_blocks -= 1
            m_str = self.mem_str()
            if m_str in self.states_seen:
                yield m_str
                raise StopIteration
            else:
                self.states_seen.append(m_str)
                yield m_str



    def find_first_max(self):
        max_val = self.memory[0]
        max_pos = 0
        for i in range(len(self.memory)):
            if self.memory[i] > max_val:
                max_val = self.memory[i]
                max_pos = i
        return max_val, max_pos


