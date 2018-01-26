import copy
import itertools
import numpy as np
import crayons
from product import *
import matplotlib.pyplot as plt
import scipy.optimize

from constants import *
from fact.graph.route import *

def common_products(leg0, leg1):
    p0 = set([p.product for p in leg0.products])
    p1 = set([p.product for p in leg0.products])
    return list(p0 & p1)


def transfer(l0, l1, slots):
    print('transfer {:6.1f} slots from route {} to {}'.format(slots, l0.route.id_, l1.route.id_))

    products = common_products(l0, l1)
    
    if False:
        print()
        l0.show()
        print()
        l1.show()
        print()
        print('common products')

        for p in products:
            print('\t{}'.format(p.name))
    
    if len(products) != 1: return

    product = products[0]

    #print()

    p0 = l0.get_product(product)
    p1 = l1.get_product(product)

    #print('slots of {}'.format(product.name))
    #print('{:8.1f}'.format(p0.slots()))
    #print('{:8.1f}'.format(p1.slots()))

    if p1.slots() < slots:
        print('the sink does not have enough slots of {} to transfer'.format(product))
    
    t = slots * product.stack_size

    p0.rate = p0.rate + t
    p1.rate = p1.rate - t
   
    if False:
        print('after transfer')
        print()
        l0.route.show()
        print()
        l1.route.show()
        print()

class Edge:
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst

    def show(self):
        
        lines = math.ceil(self.trains_per_second() / Constants.train_line_capacity())

        print(crayons.blue('edge: {:24} -> {:24}'.format(self.src.name, self.dst.name), bold=True))
        print('\ttrains per second:    {:8.3f}'.format(self.trains_per_second()))
        print('\ttrains line capacity: {:8.3f}'.format(Constants.train_line_capacity()))
        print('\ttrains lines:         {:8.3f}'.format(lines))

    def routes(self):
        for r in Routes.routes:
            for l in r.legs:
                if l.edge == self:
                    yield r, l
                    break

    def trains_per_second(self):
        return sum(r.trains_per_second() for r, l in self.routes())

    def legs(self):
        for r in Routes.routes:
            for l in r.legs:
                if l.edge == self:
                    yield l
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
            yield 'Route {:2} empty: {:5.1f} {:5.1f}%'.format(r.id_, l.empty_slots(), l.empty_percent())
            for p in l.products:
                yield p.to_string()


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

    def balance_one(self):
        sources = [(r, l, l.empty_slots()) for r, l in self.routes() if l.empty_slots() > 0]
        sinks = [(r, l, l.empty_slots()) for r, l in self.routes() if l.empty_slots() < 0]

        
        sources = sorted(sources, key=lambda t: -t[2])
        sinks = sorted(sinks, key=lambda t: t[2])

        for r0, l0, slots0 in sources:
            for r1, l1, slots1 in sinks:
                slots = min(slots0, -slots1)
                transfer(l0, l1, slots)
                return True

        return False
    
    def balance_routes(self):
        print('edge: {:24} -> {:24}'.format(self.src.name, self.dst.name))
        
        for r, l in self.routes():
            print('\troute {:2} empty: {:5.1f}'.format(r.id_, l.empty_slots()))

        while self.balance_one(): pass

        for r, l in self.routes():
            print('\troute {:2} empty: {:5.1f}'.format(r.id_, l.empty_slots()))



