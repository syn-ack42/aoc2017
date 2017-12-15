
def number_sequence(start_value, factor, criteria=None):
    val = start_value
    limit = 2147483647
    trunc = int('ffff', 16)

    while True:
        val = (val * factor) % limit
        if (criteria is None) or (val % criteria == 0):
            trunc_val = trunc & val
            yield val, trunc_val


def run_1(inp, verbose=False):
    """>>> from src import d15
>>> d15.run_1('65,8921,5', True)
    1092455   430625591 False
 1181022009  1233683848 False
  245556042  1431495498 True
 1744312007   137874439 False
 1352636452   285222916 False
1
    """
    ivals = inp.split(",")
    sa = int(ivals[0])
    sb = int(ivals[1])
    rcount = int(ivals[2])
    gen_a = number_sequence(sa, 16807)
    gen_b = number_sequence(sb, 48271)

    same_count = 0
    for i in range(rcount):
        a, ta = gen_a.__next__()
        b, tb = gen_b.__next__()
        if (ta == tb):
            same_count +=1

        if verbose:
            print("{0: >11} {1: >11} {2}".format(a, b, ta == tb))
    return same_count


def run_2(inp, verbose = False):
    """>>> from src import d15
>>> d15.run_2('65,8921,5,4,8', True)
 1352636452  1233683848 False
 1992081072   862516352 False
  530830436  1159784568 False
 1980017072  1616057672 False
  740335192   412269392 False
0
    """
    ivals = inp.split(",")
    sa = int(ivals[0])
    sb = int(ivals[1])
    rcount = int(ivals[2])
    ca = int(ivals[3])
    cb = int(ivals[4])
    gen_a = number_sequence(sa, 16807, ca)
    gen_b = number_sequence(sb, 48271, cb)

    same_count = 0
    for i in range(rcount):
        a, ta = gen_a.__next__()
        b, tb = gen_b.__next__()
        if (ta == tb):
            same_count += 1

        if verbose:
            print("{0: >11} {1: >11} {2}".format(a, b, ta == tb))
    return same_count
