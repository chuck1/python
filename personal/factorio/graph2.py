import itertools
import numpy as np

class Edge:
    def __init__(self, src, dst, products):
        self.src = src
        self.dst = dst
        self.products = products

    def start(self):
        return self.src.position

    def v(self):
        return self.dst.position - self.src.position

    def x(self, k):
        return self.src.position + k * self.v()

    def length(self):
        return np.linalg.norm(self.v())

    def add_products(self, products):
        self.products += products

        groups = itertools.groupby(self.products, key=lambda t: t[0])

        self.products = [(k, sum(rate for _, rate in g)) for k, g in groups]

class Node:
    def __init__(self, g, name, process, position):
        self.g = g
        self.name = name
        self.process = process
        self.position = position

    def ancestors(self):
        for e in self.g.edges:
            if e.dst == self:
                yield e

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

    

