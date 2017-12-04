def run_1(inp):
    return run(inp)


def run_2(inp):
    return run(inp, True)


def run(inp, q2=False):
    s = 0

    if not q2:
        for l in inp.splitlines():
            s += row_checksum(l)
    else:
        for l in inp.splitlines():
            s += row_even_div_val(l)
    return s


def row_checksum(row):
    mi = 99999999999999
    ma = 0
    nums = row.split()
    for n in nums:
        n = int(n)
        if n < mi:
            mi = n
        if n > ma:
            ma = n
    print("max: {} min: {} rsum: {}".format(ma, mi, ma - mi))
    return ma - mi


def row_even_div_val(row):
    row = row.split()
    for i in range(0, len(row) - 1):
        for k in range(i + 1, len(row)):
            r = even_div(row[i], row[k])
            if r:
                r = int(r)
                print("a: {} b: {} val: {}".format(row[i], row[k], r))
                return r


def even_div(a, b):
    a = int(a)
    b = int(b)
    if a > b:
        return (a / b) if (a % b == 0) else None
    if b > a:
        return (b / a) if (b % a == 0) else None
    return None
