import re
import copy
from math import floor, ceil, sqrt


class Particle(object):
    def __init__(self, id, p, v, a):
        self.id = id
        self.p0 = copy.deepcopy(p)
        self.p = p
        self.v = v
        self.a = a

    def advance_ticks(self, t):
        for i in range(3):
            for n in range(t):
                self.v[i] += self.a[i]
                self.p[i] += self.v[i]

            # if self.a[i] >0:
            #     a = ceil(self.a[i]/2) if self.v[i] > 0 else floor(self.a[i]/2)
            # else:
            #     a = ceil(self.a[i] / 2) if self.v[i] < 0 else floor(self.a[i] / 2)
            # self.p[i] = self.p0[i] + (self.v[i]) * t + (a* t*t)

    def __str__(self):
        return "{}.{}.{}".format(self.p[0], self.p[1], self.p[2])

    def distance_to_0(self):
        return abs(self.p[0]) + abs(self.p[1]) + abs(self.p[2])

    def abs_acc(self):
        return sqrt(self.a[0]**2 + self.a[1]**2 + self.a[2]**2)

def parse_particle(line, id):
    r = re.match('p=<\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)>, v=<\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)>, a=<\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)>', line)
    tmp = []
    for i in range(1,10):
        tmp.append(int(r.group(i)))
    p = tmp[:3]
    v = tmp[3:6]
    a = tmp[6:]
    return Particle(id, p, v, a)

def run_1(inp):
    """
>>> from src import d20
>>> p = d20.parse_particle('p=<3,0,0>, v=<2,0,0>, a=<-1,0,0>',0)
>>> p.advance_ticks(1)
>>> str(p)
'4.0.0'
>>> p.advance_ticks(1)
>>> str(p)
'4.0.0'
>>> p.advance_ticks(1)
>>> str(p)
'3.0.0'
>>> p = d20.parse_particle('p=< 4,0,0>, v=< 0,0,0>, a=<-2,0,0>',0)
>>> p.advance_ticks(1)
>>> str(p)
'2.0.0'
>>> p.advance_ticks(1)
>>> str(p)
'-2.0.0'
>>> p.advance_ticks(1)
>>> str(p)
'-8.0.0'
>>> inp ='''p=<3,0,0>, v=<2,0,0>, a=<-1,0,0>
... p=<4,0,0>, v=<0,0,0>, a=<-2,0,0>'''
>>> d20.run_1(inp)
0
    """
    ps = []
    min_d = 9999999999999
    nearest = None
    i = 0
    min_a = 999999999
    slowest = None
    for l in inp.splitlines():
        p = parse_particle(l, i)
        ps.append(p)
        p.advance_ticks(40000)
        d = p.distance_to_0()
        if d < min_d:
            min_d = d
            nearest = i
        acc = p.abs_acc()
        if acc < min_a:
            min_a = acc
            slowest = i
        i += 1

    return nearest


def run_2(inp):
    ps = []
    i = 0
    for l in inp.splitlines():
        p = parse_particle(l, i)
        ps.append(p)
        i += 1

    for i in range(10000):
        locs = {}
        del_lst = set([])
        for k in range(len(ps)):
            ploc = str(ps[k])
            if ploc in locs:
                del_lst.add(k)
                del_lst.add(locs[ploc])
            else:
                locs[ploc] = k
                ps[k].advance_ticks(1)
        if len(del_lst) > 0:
            print("{}: deleting {} paticles".format(i, len(del_lst)))

            tmp = []
            for j in range(len(ps)):
                if not (j in del_lst):
                    tmp.append(ps[j])
            ps = tmp

    return len(ps)