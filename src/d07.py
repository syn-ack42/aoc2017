import re


def run_1(inp):
    '''
>>> from src import d07
>>> inp = """pbga (66)
... xhth (57)
... ebii (61)
... havc (66)
... ktlj (57)
... fwft (72) -> ktlj, cntj, xhth
... qoyq (66)
... padx (45) -> pbga, havc, qoyq
... tknk (41) -> ugml, padx, fwft
... jptl (61)
... ugml (68) -> gyxo, ebii, jptl
... gyxo (61)
... cntj (57)"""
>>> d07.run_1(inp)
pbga (66) p:padx
xhth (57) p:fwft
ebii (61) p:ugml
havc (66) p:padx
ktlj (57) p:fwft
fwft (72) -> ktlj, cntj, xhth p:tknk
qoyq (66) p:padx
padx (45) -> pbga, havc, qoyq p:tknk
tknk (41) -> ugml, padx, fwft p:?
jptl (61) p:ugml
ugml (68) -> gyxo, ebii, jptl p:tknk
gyxo (61) p:ugml
cntj (57) p:fwft
'tknk'
    '''
    inp = inp.splitlines()

    nodes = []
    for l in inp:
        n = Node(l)
        nodes.append(n)

    root_node = None
    for n in nodes:
        for p in nodes:
            if p.has_child(n.name):
                n.parent = p.name
                break
        if n.parent is None:
            root_node = n
        print(n)
    return root_node.name


def run_2(inp):
    inp = inp.splitlines()
    stack = Stack()
    for l in inp:
        n = Node(l, stack)

    stack.allweights()

    print("\nunbalanced nodes:")
    for k, n in stack.nodes.items():
        if n.unbalanced:
            print(n)
            values = {}
            correct_weight = None
            for c in n.children:
                if c.get_sum_weight() in values:
                    values[c.get_sum_weight()]["count"] +=1
                    values[c.get_sum_weight()]["last"] = c
                    correct_weight = c.get_sum_weight()
                else:
                    values[c.get_sum_weight()] = {}
                    values[c.get_sum_weight()]["count"] =1
                    values[c.get_sum_weight()]["last"] = c

            for _, v in values.items():
                if v["count"] == 1:
                    odd_man_out = v["last"]
                    break
            print("odd man out: {}".format(odd_man_out))

            if not odd_man_out.unbalanced:
                print("!!! {}: my weight {} is wrong".format(odd_man_out.name, odd_man_out.weight))
                return correct_weight - odd_man_out.get_sum_weight() + odd_man_out.weight


class Stack(object):
    def __init__(self):
        self.nodes = {}

    def add_node(self, node):
        self.nodes[node.name] = node
        self.link_nodes()


    def link_nodes(self):
        for k, n in self.nodes.items():
            for c in n.child_names:
                if c in self.nodes:
                    self.nodes[c].parent = n.name
                    n.children.add(self.nodes[c])

    def allweights(self):
        for k, n in self.nodes.items():
            print("{}: {}, {} children unbalanced {}".format(n.name, n.get_sum_weight(), len(n.children), n.unbalanced))

class Node(object):
    '''
>>> from src import d07
>>> n = d07.Node('fwft (72) -> ktlj, cntj, xhth')
>>> print(n)
fwft (72) -> ktlj, cntj, xhth p:?
>>> n = d07.Node('fsdfdfs (3343)')
>>> print(n)
fsdfdfs (3343) p:?
    '''


    def __init__(self, str_rep, stack = None):
        self.parent = None
        self.stack = stack
        self.child_names = set([])
        self.children = set([])
        self.unbalanced = False

        p = re.search('^(\w*) \((\d*)\)( -> (.*))?', str_rep)
        self.name = p.group(1)
        self.weight = int(p.group(2))
        if p.group(4):
            cs = p.group(4)
            cs = cs.split(", ")
            self.child_names = set([x for x in cs])

        if self.stack:
            stack.add_node(self)

    def has_child(self, name):
        return (name in self.child_names)

    def get_sum_weight(self):
        s = self.weight
        c_wght = None
        for c in self.children:
            w = c.get_sum_weight()
            s += w
            if c_wght is None:
                c_wght = w
            if not (c_wght == w):
                self.unbalanced = True
        return s

    def __str__(self):
        s = "{} ({})".format(self.name, self.weight)
        if len(self.children) > 0:
            cinfo = ["{} ({})".format(c.name, c.get_sum_weight()) for c in self.children]
            s = "{} -> {}".format(s, ", ".join(cinfo))
        elif len(self.child_names) > 0:
            cinfo = ["{}".format(c) for c in self.child_names]
            s = "{} -> {}".format(s, ", ".join(cinfo))

        s = "{} p:{}".format(s, self.parent if self.parent else "?")
        return s
