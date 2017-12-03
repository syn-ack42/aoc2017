import collections
import math

def run(inp, q2=False):
    inp = int(inp)

    if q2:
        return run_2(inp)

    us = find_upper_square(inp)
    res = dist_to_middle(us, inp)

    return res

def find_upper_square(n):
    i = 1
    while True:
        if (i*i >= n):
            return i
        i += 2

def dist_to_middle(square_size, pos):
    pos = (pos - (square_size-2)**2)
    d_inw = (square_size -1 ) / 2
    d_round = abs((pos % (square_size-1)) - (square_size -1)/2)
    return int(d_inw + d_round)


def spiral_step():
    yield 0, 0
    x = 0
    y = 0
    r = 0

    while True:
        if (x == r) and (y == -r):
            r += 1
            x += 1
        elif (x == r) and (y < 0):
            y += 1
        elif (y == -r) and (x < r):
            x += 1
        elif (x == -r) and (y > -r):
            y -= 1
        elif (y == r) and (x > -r):
            x -= 1
        elif (x == r) and (y < r):
            y += 1
        else:
            raise RuntimeError("Ouch")

        yield x, y


def is_square_of_uneven(n):
    root = math.sqrt(n)
    root = int(root + 0.5)
    if (root % 2) == 0:
        return None

    if root ** 2 == n:
        return root
    else:
        return None

def sum_adjacent(arr, x ,y):
    if x == y == 0:
        return 1
    s = 0
    for xp in (-1, 0, 1):
        for yp in (-1, 0, 1):
            if xp == yp == 0:
                continue
            if (x + xp) in arr:
                if (y + yp) in arr[x + xp]:
                    s += arr[x + xp][y + yp]
    return s

def run_2(max_val):
    a = {0: {0: 1}}
    last = 1
    for x, y in spiral_step():
        s = sum_adjacent(a, x, y)
        if s > max_val:
            print("\nmax {}: ".format(max_val))
            od_x = collections.OrderedDict(sorted(a.items()))
            for k, row in od_x.items():
                tmp = []
                od_y = collections.OrderedDict(sorted(row.items()))
                for l, v in od_y.items():
                    tmp.append(str(v))
                print(" ".join(tmp))
            return s
        else:
            if not (x in a):
                a[x] = {}
            a[x][y] = s
            last = s


