import copy
import itertools
import numpy as np
import crayons
from product import *
import matplotlib.pyplot as plt
import scipy.optimize

from constants import *
from fact.graph.leg import *

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

    def trains_per_second(self):
        cargo_wagons_per_second = self.slots() / 40
        trains_per_second = cargo_wagons_per_second / Constants.wagons_per_train
        return trains_per_second

    def slots(self):
        # cargo wagon slots per second
        return max(l.slots() for l in self.legs)

    def show(self):
        print('route {:2}: {}'.format(self.id_, self.node.process.name))
        print('\ttrains per second: {:8.2f}'.format(self.trains_per_second()))
        print('\tlegs:')
        for leg in self.legs:
            leg.show()
    
    def leg(self, edge, products):

        products = [copy.copy(p) for p in products]

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
            i //= 26

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



