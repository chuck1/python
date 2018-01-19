import itertools
import numpy as np

from product import *

def cargo_wagons_per_second(products):
    w = 0
    for k, r in products:
        process, product = k
        if not isinstance(product, IntermediateProduct): continue
        w += r / product.stack_size / 40
    return w

class RouteLegProduct:
    def __init__(self, product, rate):
        self.product = product
        self.rate = rate
    
    def __str__(self):
        return '{:22} {:8.1f}'.format(self.product.name, self.rate)

    def show(self):
        print('\t\t' + str(self))

    def slots(self):
        if isinstance(self.product, IntermediateProduct):
            return self.rate / self.product.stack_size
        else:
            return 0

class RouteLeg:
    def __init__(self, route, edge, products):
        self.route = route
        self.edge = edge
        self.products = products

    def slots(self):
        return sum(p.slots() for p in self.products)

    def get_product(self, product):
        return next(p for p in self.products if p.product == product)

    def empty_slots(self):
        if self.slots() == self.route.slots():
            return self.route.slots_second() - self.slots()
        else:
            return self.route.slots() - self.slots()

    def show(self):
        print('\t{:24} -> {:24} empty slots: {:-4.1f}'.format(self.edge.src.name, self.edge.dst.name, self.empty_slots()))
        for p in self.products:
            p.show()

class Route:
    def __init__(self, node, legs):
        self.id_ = Routes.next_id()
        self.node = node
        self.legs = legs

    def slots_second(self):
        seq = [l.slots() for l in self.legs if l.slots() != self.slots()]
        
        if not seq:
            return self.slots()

        return max(seq)

    def slots(self):
        return max(l.slots() for l in self.legs)

    def show(self):
        print('route {:2}: {}'.format(self.id_, self.node.process.name))
        for leg in self.legs:
            leg.show()
    
    def leg(self, edge, products):
        leg = RouteLeg(self, edge, products)

        if any(l.edge == leg.edge for l in self.legs):
            l = next(l for l in self.legs if l.edge == leg.edge)
            l.products += leg.products
            return l

        self.legs.append(leg)
        return leg

    def find_leg(self, edge):
        for l in self.legs:
            if l.edge == edge:
                return l

class Routes:
    routes = []
    _next_id = 0

    @classmethod
    def next_id(cls):
        i = cls._next_id
        cls._next_id += 1
        
        if i == 0: return 'A'

        s = ''
        while i > 0:
            m = i % 26
            s += chr(ord('A') + m)
            i -= m
            i /= 26

        return s[::-1]

    @classmethod
    def add_route(cls, route):
        cls.routes.append(route)

    @classmethod
    def find_route(cls, process, edge):
        for r in cls.routes:
            if r.node.process == process:
                for l in r.legs:
                    if l.edge == edge:
                        yield r
                        break

class Edge:
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst

    def routes(self):
        for r in Routes.routes:
            for l in r.legs:
                if l.edge == self:
                    yield r, l
                    break

    def start(self):
        return self.src.position

    def v(self):
        return self.dst.position - self.src.position

    def x(self, k):
        return self.src.position + k * self.v()

    def length(self):
        return np.linalg.norm(self.v())

    def label_lines(self):

        for r, l in self.routes():
            yield 'Route {:2} empty: {:4.1f}'.format(r.id_, l.empty_slots())
            for p in l.products:
                yield str(p)


        #for k, r in self.products:
        #    w = cargo_wagons_per_second([(k, r)])
        #    yield '{:18} {:6.0f} -> {:22} {:4.1f} wag/sec'.format(k[1].name, r, k[0].name, w) 

    def products(self):
        products = list(set([p.product for r, l in self.routes() for p in l.products]))

        print('edge: {:24} -> {:24}'.format(self.src.name, self.dst.name))

        for product in products:
            print('\tproduct: {:24}'.format(product.name))

            for r, l in self.routes():
                try:
                    p = next(p for p in l.products if p.product == product)
                except StopIteration:
                    continue

                print('\t\tRoute {:2} rate: {:8.1f}'.format(r.id_, p.rate))

    def balance_routes(self):
        print('edge: {:24} -> {:24}'.format(self.src.name, self.dst.name))

        sources = [(r, l, l.empty_slots()) for r, l in self.routes() if l.empty_slots() > 0]
        sinks = [(r, l, l.empty_slots()) for r, l in self.routes() if l.empty_slots() < 0]

        for r, l in self.routes():
            print('\troute {:2} empty: {:5.1f}'.format(r.id_, l.empty_slots()))
        
        sources = sorted(sources, key=lambda t: -t[2])
        sinks = sorted(sinks, key=lambda t: t[2])

        for r0, l0, slots0 in sources:
            for r1, l1, slots1 in sinks:
                slots = min(slots0, -slots1)
                transfer(l0, l1, slots)

def common_products(leg0, leg1):
    p0 = set([p.product for p in leg0.products])
    p1 = set([p.product for p in leg0.products])
    return list(p0 & p1)

def transfer(l0, l1, slots):
    print('transfer {:6.1f} slots from route {} to {}'.format(slots, l0.route.id_, l1.route.id_))
    
    print()
    l0.show()
    print()
    l1.show()
    print()
    print('common products')

    products = common_products(l0, l1)
    for p in products:
        print('\t{}'.format(p.name))
    
    if len(products) != 1: return

    product = products[0]

    print()

    print('slots of {}'.format(product.name))
    print('{:8.1f}'.format(l0.get_product(product).slots()))
    print('{:8.1f}'.format(l1.get_product(product).slots()))

    p1 = l1.get_product(product)

    if p1.slots() < slots:
        print('the sink does not have enough slots of {} to transfer'.format(product))

    print()

class Node:
    def __init__(self, g, name, process, product, position):
        self.g = g
        self.name = name
        self.process = process
        self.product = product
        self.position = position

    def ancestors(self):
        for e in self.g.edges:
            if e.dst == self:
                yield e

    def inputs(self, process0=None):
        if process0 is None:
            process0 = self.process
            print('inputs for process', self.process.name)

        for e in self.ancestors():
            products = [(k, r) for k, r in e.products if k[0] == process0]
            
            if products:
                e.src.inputs(process0)

                print('\t{:24} -> {:24}'.format(e.src.name, e.dst.name))
                for k, r in products:
                    process, product = k
                    print('\t\t{:18} {:6.0f}'.format(k[1].name, r))


    def rank(self):
        r = 0
        for a in self.ancestors():
            r = max(a.src.rank(), r)
        return r + 1

    def neighbors(self):
        for e in self.g.edges:
            if e.src == self:
                yield e, e.dst
            elif e.dst == self:
                yield e, e.src

    def is_ancestor(self, n):
        for e in self.g.edges:
            if e.dst == self:
                if e.src == n:
                    return True
                if e.src.is_ancestor(n): return True
        return False

    def path(self, n):
        for e in self.g.edges:
            if e.dst == self:
                if e.src == n:
                    yield e
                    return
                elif e.src.is_ancestor(n):
                    yield from e.src.path(n)
                    yield e
                    return
       

    def neighbor_center(self):
        p = np.array([0.,0.])
        c = 0

        for e, n in self.neighbors():
            p += n.position
            c += 1

        p = p / c

        return p

def cross(e0, e1):

    if e0.src == e1.src: return
    if e0.src == e1.dst: return
    if e0.dst == e1.src: return
    if e0.dst == e1.dst: return

    o0 = e0.start()
    o1 = e1.start()
    v0 = e0.v()
    v1 = e1.v()
    
    k1 = (o0[0] - o1[0] - v0[0] / v0[1] * (o0[1] - o1[1]))/(v1[1] - v1[1] * v0[0] / v0[1])

    k0 = (o1[0] + k1 * v1[0] - o0[0]) / v0[0]

    if k0 < 0: return
    if k0 > 1: return
    if k1 < 0: return
    if k1 > 1: return

    return (k0, k1)

if __name__ == '__main__':

    n0 = Node(np.array([0,1]))
    n1 = Node(np.array([1,0]))
    n2 = Node(np.array([0,0]))
    n3 = Node(np.array([1,1]))
    e0 = Edge(n0, n1)
    e1 = Edge(n2, n3)
    
    print(cross(e0, e1))

    

