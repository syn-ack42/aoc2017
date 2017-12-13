from copy import deepcopy

import re


class RoutingTable(object):
    def __init__(self):
        self.routes = {}
        self.changes = 0
        self.found_nodes = set([])

    def register_route(self, from_node, to_node, route):
        self.found_nodes.add(to_node)
        rc = "{}->{}".format(from_node, to_node)
        if rc in self.routes:
            if len(self.routes[rc]) > len(route):
                self.routes[rc] = route
        else:
            self.routes[rc] = route
        self.changes += 1

    def __str__(self):
        rstrgs = sorted(["{}: {}".format(k, ",".join(v)) for k, v in self.routes.items()])
        return "\n".join(rstrgs)


class PingPacket(object):
    def __init__(self, source, route=[], ttl=None):
        self.source = source
        self.route = route
        self.ttl = ttl


class Node(object):
    route_table = RoutingTable()
    node_registry = {}

    def __init__(self, name, neighbours):
        self.name = name
        self.neighbours = neighbours
        self.queue = []
        self.node_registry[self.name] = self

    @classmethod
    def reset(cls):
        cls.route_table = RoutingTable()
        cls.node_registry = {}

    def tick(self):
        for p in self.queue:
            for n in self.neighbours:
                if not (n in self.node_registry):
                    raise RuntimeError("node {} not registered".format(n))
                self.node_registry[n].discover(deepcopy(p))
        self.queue = []

    def discover(self, ping_packet=None):
        if ping_packet is None: #I am source
            ping_packet = PingPacket(self.name)
            self.queue.append(ping_packet)
            self.route_table.register_route(self.name, self.name, [])
            while True:
                changes = self.route_table.changes
                for k, node in self.node_registry.items():
                    node.tick()
                if self.route_table.changes == changes:
                    return

        self.route_table.register_route(ping_packet.source, self.name, ping_packet.route)
        if not (self.name in ping_packet.route):
            ping_packet.route.append(self.name)
            self.queue.append(ping_packet)

def parse_routeline(line):
    r = re.match('^ *(\w+) <-> (.+)$', line)
    n = r.group(1)
    neighbours = r.group(2)
    neighbours = neighbours.split(", ")
    return n, neighbours

def run_1(inp):

    nodes = {}
    for l in inp.splitlines():
        n, neighbours = parse_routeline(l)
        nodes[n] = Node(n, neighbours)

    nodes["0"].discover()
    print(Node.route_table)
    return len(Node.route_table.routes)



def run_2(inp):
    """
    >>> from src import d12
    >>> inp = '''0 <-> 2
    ... 1 <-> 1
    ... 2 <-> 0, 3, 4
    ... 3 <-> 2, 4
    ... 4 <-> 2, 3, 6
    ... 5 <-> 6
    ... 6 <-> 4, 5'''
    >>> d12.run_2(inp)
    2
    """
    nodes = {}
    for l in inp.splitlines():
        n, neighbours = parse_routeline(l)
        nodes[n] = Node(n, neighbours)

    cnt = 0
    for name, node in Node.node_registry.items():
        if not (name in Node.route_table.found_nodes):
            cnt += 1
            node.discover()

    return cnt
