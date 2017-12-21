import re

from math import sqrt


def make_library(inp):
    lib = {}
    for l in inp.splitlines():
        r = re.match("(.+) => (.+)", l)
        if r:
            f = r.group(1)
            t = r.group(2)
            for m in mutated_identifierts(matrixify(f)):
                lib[m] = matrixify(t)
    return lib

def matrixify(s):
    """
    #../.../..#
    """
    r = []
    for l in s.split("/"):
        line = [x for x in l]
        r.append(line)
    return r

def mutated_identifierts(m):
    r = []

    t = []
    u = []
    for i in range(len(m)):
        t.append(list(m[i]))
        u.append(list(reversed(m[i])))
    r.append(identifierize(t))
    r.append(identifierize(u))

    t = []
    u = []
    for i in range(len(m)):
        c = len(m)-i-1
        t.append(list(m[c]))
        u.append(list(reversed(m[c])))
    r.append(identifierize(t))
    r.append(identifierize(u))

    t = []
    u = []
    for i in range(len(m)):
        l = []
        for j in range(len(m)):
            l.append(m[j][i])
        t.append(list(l))
        u.append(list(reversed(l)))
    r.append(identifierize(t))
    r.append(identifierize(u))

    t = []
    u = []
    for k in range(len(m)):
        i = len(m)-k-1
        l = []
        for j in range(len(m)):
            l.append(m[j][i])
        t.append(list(l))
        u.append(list(reversed(l)))
    r.append(identifierize(t))
    r.append(identifierize(u))

    return r

def identifierize(m):
    return "/".join(["".join(x) for x in m])

def split_matrix(m):

    r = []
    step = 2 if (len(m) % 2 == 0) else 3
    splits = int(len(m) / step)
    for y in range(splits):
        for x in range(splits):
            bx = x * step
            by = y * step
            b = []
            for k in range(step):
                b.append(list(m[by + k][bx: bx+step]))
            r.append(list(b))
    return r

def join_matrix_from_blockline(bl):
    blocks_per_side = int(sqrt(len(bl)))
    dots_per_block = len(bl[0])
    r = []

    for by in range(blocks_per_side):
        for y in range(dots_per_block):
            line = []
            for bx in range(blocks_per_side):
                line += bl[by*blocks_per_side + bx][y]
            r.append(list(line))

    return r

def matrix_to_str(m):
    return "\n".join(["".join(s) for s in m])


def expand_matrix(m, lib):
    return lib[identifierize(m)]

def run_1(inp, iter=5):
    """
>>> from src import d21
>>> inp = '''../.# => ##./#../...
... .#./..#/### => #..#/..../..../#..#'''
>>> d21.run_1(inp, 2)
    """
    lib = make_library(inp)
    mstr = """.#./..#/###"""
    m = matrixify(mstr)
    print("iteration: {}".format(0))
    print(matrix_to_str(m))
    for i in range(iter):
        bl = split_matrix(m)
        nbl = []
        for b in bl:
            nbl.append(expand_matrix(b, lib))
        m = join_matrix_from_blockline(nbl)
        print("iteration: {}".format(i+1))
        print(matrix_to_str(m))
    tmp = identifierize(m)
    return tmp.count("#")


def run_2(inp):
    return run_1(inp, 18)