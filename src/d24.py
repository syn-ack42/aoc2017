from copy import deepcopy

import re


class Bridge(object):
    bridges = []
    max_strength = 0
    max_length = 0
    max_length_strength = 0
    limit = 0

    def __init__(self, build_from=None, next_step=None, thingiepool=[]):

        self.thingiepool = thingiepool
        #self.children = []

        if build_from is None:
            self.thingies = []
            self.end_port = 0
            self.strength = 0
            for t in thingiepool:
                Bridge.limit += t.strength()
        else:
            self.end_port = build_from.end_port
            self.thingies = deepcopy(build_from.thingies)
            n = next_step.use_with(build_from.end_port)
            if n == False:
                raise RuntimeError("Screwup")
            else:
                self.thingies.append(next_step)
                self.end_port = n
            self.strength = build_from.strength + next_step.strength()
        if self.strength > Bridge.max_strength:
            #print("new max: {} of {} with length {} left {}".format(self.strength, self.limit, len(self.thingies), len(self.thingiepool)))
            Bridge.max_strength = self.strength
            #Bridge.bridges.append(self)
        if len(self.thingies) > Bridge.max_length:
            Bridge.max_length = len(self.thingies)
            Bridge.max_length_strength = self.strength
        elif len(self.thingies) == Bridge.max_length:
            if self.strength > Bridge.max_length_strength:
                Bridge.max_length = len(self.thingies)
                Bridge.max_length_strength = self.strength

        self._extend()

    def _extend(self):
        for i in range(len(self.thingiepool)):
            t = deepcopy(self.thingiepool[i])
            if t.use_with(self.end_port) == False:
                continue
            p = deepcopy(self.thingiepool)
            del p[i]
            b =Bridge(build_from=self, next_step=t, thingiepool=p)
            #self.children.append(Bridge(build_from=self, next_step=t, thingiepool=p))


class Thingy(object):
    def __init__(self, port_a, port_b):
        self.port_a = port_a
        self.port_b = port_b

    def strength(self):
        a = self.port_a or 0
        b = self.port_b or 0
        return a + b

    def use_with(self, ptype):
        if self.port_a == ptype:
            return self.port_b
        elif self.port_b == ptype:
            return self.port_a
        else:
            return False

    def has_port(self, ptype):
        return ((self.port_a == ptype) or (self.port_b == ptype))

    @classmethod
    def parse_from_str(cls, s):
        r = re.match("(\d+)\/(\d+)", s)
        return cls(int(r.group(1)), int(r.group(2)))


def run_1(inp):
    """
>>> inp = '''0/2
... 2/2
... 2/3
... 3/4
... 3/5
... 0/1
... 10/1
... 9/10'''
>>> run_1(inp)
31
"""
    ts = []
    for l in inp.splitlines():
        t = Thingy.parse_from_str(l)
        ts.append(t)
    b0 = Bridge(thingiepool=ts)
    return Bridge.max_strength



def run_2(inp):
    """
>>> inp = '''0/2
... 2/2
... 2/3
... 3/4
... 3/5
... 0/1
... 10/1
... 9/10'''
>>> run_2(inp)
19
"""
    ts = []
    for l in inp.splitlines():
        t = Thingy.parse_from_str(l)
        ts.append(t)
    b0 = Bridge(thingiepool=ts)
    return Bridge.max_length_strength
