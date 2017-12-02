
def run(inp, q2=False):
    res = 0
    off = 1
    l = len(inp)

    if q2:
        off = int(l/2)

    for i in range(0, l):
        if inp[i] == inp[(i + off) % l]:
            res += int(inp[i])

    return res

