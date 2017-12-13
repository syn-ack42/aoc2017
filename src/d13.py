import collections
import re


class FWLayer(object):
    def __init__(self, layer, range):
        self.layer = layer
        self.range = range
        self.scan_position = 0
        self.scan_direction = 1
        self.intruder_at = None
        self.intruder = None

    def reset(self):
        self.scan_position = 0
        self.scan_direction = 1
        self.intruder_at = None
        self.intruder = None

    def tick(self):
        self.intruder = None
        self.intruder_at = None
        if self.range > 0:
            self.scan_position += self.scan_direction
            if (self.scan_position % (self.range - 1)) == 0:
                self.scan_direction *= -1

    def intrude(self, intruder, position=0):
        self.intruder = intruder
        self.intruder_at = position
        if (self.range > 0) and (position == self.scan_position):
            intruder.caught(self.severity())
            return self.severity()
        else:
            return 0

    def severity(self):
        return self.layer * self.range

    def __str__(self):
        if self.range == 0:
            return "X" if self.intruder else "-"
        r = ""

        for i in range(self.range):
            if i == self.intruder_at:
                r += "8" if i == self.scan_position else "X"
            else:
                r += "O" if i == self.scan_position else "."
        return r


class Intruder(object):
    def __init__(self, firewall):
        self.layer = 0
        self.firewall = firewall
        self.score = 0
        self.detected = False

    def reset(self):
        self.layer = 0
        self.score = 0
        self.detected = False

    def tick(self):
        passed = self.firewall.sneek_through(self, self.layer)
        if passed:
            return True
        else:
            self.layer += 1
            return False

    def caught(self, severity):
        self.score += severity
        self.detected = True


class Firewall(object):
    def __init__(self, init_str):
        self.layers = []
        for s in init_str.splitlines():
            level, rng = self.parse_layer(s)
            if level > len(self.layers):
                for i in range(level - len(self.layers)):
                    self.layers.append(FWLayer(len(self.layers), 0))
            self.layers.append(FWLayer(level, rng))

    def sneek_through(self, intruder, layer, position=0):
        if layer >= len(self.layers):
            return True
        else:
            self.layers[layer].intrude(intruder, position)
            return False

    def tick(self):
        for l in self.layers:
            l.tick()

    def reset(self):
        for l in self.layers:
            l.reset()

    def parse_layer(self, l_str):
        r = re.match("^(\d+): (\d+)$", l_str)
        level = r.group(1)
        rng = r.group(2)
        return int(level), int(rng)

    def __str__(self):
        r = ""
        for i in range(len(self.layers)):
            r += "{}: {}\n".format(i, str(self.layers[i]))
        return r


def run_1(inp):
    """>>> from src import d13
>>> inp = '''0: 3
... 1: 2
... 4: 4
... 6: 4'''
>>> d13.run_1(inp)
24
"""
    fw = Firewall(inp)
    intr = Intruder(fw)
    passed = False
    while not passed:
        passed = intr.tick()
        fw.tick()
    return intr.score


def run_2(inp):
    """>>> from src import d13
>>> inp = '''0: 3
... 1: 2
... 4: 4
... 6: 4'''
>>> d13.run_2(inp)
10
"""
    fw = Firewall(inp)
    delay = 0
    maxreach = 0

    intruders = collections.OrderedDict()
    while True:
        it = Intruder(fw)
        intruders[delay] = it
#        print("{}: {} intruders active, max reach = {}".format(delay, len(intruders), maxreach))

        del_list = []
        for d, i in intruders.items():
            if i.tick():
                return d
            if i.detected:
                del_list.append(d)
            else:
                if i.layer > maxreach:
                    maxreach = i.layer
        for d in del_list:
            del intruders[d]

        fw.tick()
        delay += 1