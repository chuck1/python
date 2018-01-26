import copy
import itertools
import numpy as np
import crayons
from product import *
import matplotlib.pyplot as plt
import scipy.optimize

from constants import *
from fact.graph.edge import *
from fact.graph.product import *

def leg_difference(l0, l1):
    products = []
    
    if l0 is not None:
        products += [RouteLegProduct(p.product, -p.rate) for p in l0.products]

    if l1 is not None:
        products += [RouteLegProduct(p.product, p.rate) for p in l1.products]
    
    products = sorted(products, key=lambda p: id(p.product))
    groups = itertools.groupby(products, key=lambda p: p.product)

    for k, g in groups:
        yield k, sum(p.rate for p in g)

class RouteLeg:
    def __init__(self, route, edge, products):
        self.route = route
        self.edge = edge
        self.products = products

    def slots(self):
        return sum(p.slots() for p in self.products)

    def get_product(self, product):
        return next(p for p in self.products if p.product == product)

    def prev(self):
        for l in self.route.legs:
            if l.edge.dst == self.edge.src:
                return l

    def next(self):
        for l in self.route.legs:
            if l.edge.src == self.edge.dst:
                return l

    def empty_slots(self):
        if self.slots() == self.route.slots():
            return self.route.slots_second() - self.slots()
        else:
            return self.route.slots() - self.slots()
    
    def empty_percent(self):
        if self.route.slots() > 0:
            return self.empty_slots() / self.route.slots() * 100
        else:
            return 0

    def show(self):
        print('\t{:24} -> {:24} empty slots: {:5.1f} {:5.1f}%'.format(self.edge.src.name, self.edge.dst.name, self.empty_slots(), self.empty_percent()))
        for p in self.products:
            p.show()



