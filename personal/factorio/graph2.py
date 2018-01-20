import copy
import itertools
import numpy as np
import crayons
from product import *
import matplotlib.pyplot as plt
import scipy.optimize

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
    
    def to_string(self):
        return '{:22} {:8.1f}'.format(self.product.name, self.rate)

    def show(self):
        print('\t\t' + self.to_string())

    def slots(self):
        if isinstance(self.product, IntermediateProduct):
            return self.rate / self.product.stack_size
        else:
            return 0

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

def load_time(d):
    ins_rate = 27.7
    
    ins_per_wagon_load = 6
    ins_per_wagon_unload = 6
    
    items_load = sum(r for p, r in d if r > 0)
    items_unload = sum(r for p, r in d if r < 0)
    
    print(items_load)
    print(items_unload)
    
    

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

    def edges_out(self):
        for e in self.g.edges:
            if e.src == self:
                yield e
    
    def legs(self):
        for r in Routes.routes:
            for l in r.legs:
                if l.edge.src == self:
                    yield l.prev(), l
                    break
                elif l.edge.dst == self:
                    yield l, l.next()
                    break
 
    def legs_term(self):
        for l0, l1 in self.legs():
            if l1 is None:
                yield l0, l1

    def legs_orig(self):
        for l0, l1 in self.legs():
            if l0 is None:
                yield l0, l1

    def legs_thru(self):
        for l0, l1 in self.legs():
            if l0 is None: continue
            if l1 is None: continue
            yield l0, l1

    def layout_options(self):
        legs_term = list(self.legs_term())
        legs_orig = list(self.legs_orig())
        legs_thru = list(self.legs_thru())

        comb = itertools.combinations_with_replacement(['term', 'orig', 'thru'], 2)
        for c in comb:
            if legs_term:
                if not any(x in c for x in ['term', 'thru']):
                    continue
            if legs_orig:
                if not any(x in c for x in ['orig', 'thru']):
                    continue
            if legs_thru:
                if 'thru' not in c:
                    continue
            yield c
    
    def get_leg_type(self, leg):
        legs_term = list(self.legs_term())
        legs_orig = list(self.legs_orig())
        legs_thru = list(self.legs_thru())
        if leg in legs_term:
            return 'term'
        elif leg in legs_orig:
            return 'orig'
        elif leg in legs_thru:
            return 'thru'
        raise RuntimeError()

    def leg_fraction(self, leg, c, comb):
        """
        fraction of items from leg that will go through single station with layout c
        """

        def compatible(t, s):
            if s == 'thru': return True
            return t == s

        t = self.get_leg_type(leg)

        if not compatible(t, c): return 0

        count = sum(1 for c1 in comb if compatible(t, c1))
        
        return 1 / count
        
    def test_layout_station(self, station, stations, ins_l_frac):
        ins = 0
        ins_u_frac = 1 - ins_l_frac

        # fraction of load and unload inserters
        ins_rate = 27.7
        transition_time = 20
        #ins_l_frac = 0.5
        
        legs = list(self.legs())

        for leg in legs:
            f = self.leg_fraction(leg, station, stations)
            leg0, leg1 = leg
            
            l0 = sum(r for p, r in leg_difference(leg0, leg1) if r > 0) * f
            u0 = sum(r for p, r in leg_difference(leg0, leg1) if r < 0) * f
            
            for each product:
                wagon_capacity_l = slots_l / l0.route.slots() * 40 * p.stack_size
            
            load_time = wagon_capacity_l / (12 * ins_rate * ins_l_frac)
            unload_time = wagon_capacity_u / (12 * ins_rate * ins_u_frac)

            ins_l_utilization = load_time / (load_time + transition_time)
            ins_u_utilization = unload_time / (unload_time + transition_time)

            ins_l = l0 / ins_rate
            ins_u = -u0 / ins_rate
            
            ins0 = 0
            if ins_l_frac == 0:
                if ins_l != 0:
                    print('failed', ins_l, ins_l_frac)
                    return float("inf")
            else:
                ins0 = ins_l / ins_l_frac

            ins1 = 0
            if ins_u_frac == 0:
                if ins_u != 0:
                    print('failed', ins_u, ins_u_frac)
                    return float("inf")
                    return None
            else:
                ins1 = ins_u / ins_u_frac

            ins += max(ins0, ins1)

        return ins

    def test_layout(self, stations):
        
        legs = list(self.legs())
        
        ins = 0

        ret = []

        for station in stations:
            
            def func(ins_l_frac):
                return self.test_layout_station(station, stations, ins_l_frac)

            def func1(X):
                ins_l_frac = X[0]
                return self.test_layout_station(station, stations, ins_l_frac)
            
            if station == 'thru':
                bounds = [(1e-5, 1 - 1e-5)]
                res = scipy.optimize.minimize(func1, [0], bounds=bounds, method='L-BFGS-B')
                x = res.x[0]
            elif station == 'term':
                x = 0
            elif station == 'orig':
                x = 1

            ins_l_frac = np.linspace(0.01, 0.99, 100)
            ins_u_frac = 1 - ins_l_frac
            
            f = np.vectorize(func)
            y = f(ins_l_frac)
            
            #plt.plot(ins_l_frac, y)
            
            y = func(x)
            #plt.plot(x,y,'o')
            
            #print(station, 'optimal ins_l_frac: {:7.3f} ins: {:8.1f}'.format(x, y))

            ret.append((station, x, y))

            ins += y

        return stations, ins, ret

    def factory_layout(self):
        print(crayons.blue('factory: {}'.format(self.process.name), bold=True))

        # options for factory layout:
        
        options = list(self.layout_options())

        res = [self.test_layout(c) for c in options]
        
        stations, ins, ret = min(res, key=lambda t: t[1])

        print(stations)
        for station, ins_l_frac, ins in ret:
            print('{} {:7.3f} {:8.1f}'.format(station, ins_l_frac, ins))

        def get_items_load(legs):
            return sum(r for l0, l1 in legs for p, r in leg_difference(l0, l1) if r > 0)
        
        def get_items_unload(legs):
            return sum(r for l0, l1 in legs for p, r in leg_difference(l0, l1) if r < 0)

        return

        legs_term = list(self.legs_term())
        legs_orig = list(self.legs_orig())
        legs_thru = list(self.legs_thru())

        legs = list(self.legs())

        items_load = get_items_load(legs)
        items_unload = get_items_unload(legs)
        
        print('total:')
        print('\titems load   {:8.1f}'.format(get_items_load(legs)))
        print('\titems unload {:8.1f}'.format(get_items_unload(legs)))
        print('term:')
        print('\titems load   {:8.1f}'.format(get_items_load(legs_term)))
        print('\titems unload {:8.1f}'.format(get_items_unload(legs_term)))
        print('orig:')
        print('\titems load   {:8.1f}'.format(get_items_load(legs_orig)))
        print('\titems unload {:8.1f}'.format(get_items_unload(legs_orig)))
        print('thru:')
        print('\titems load   {:8.1f}'.format(get_items_load(legs_thru)))
        print('\titems unload {:8.1f}'.format(get_items_unload(legs_thru)))
        
        print('legs')
        for l0, l1 in legs:
            print('\ttrain item delta')
            d = list(leg_difference(l0, l1))
            for p, r in d:
                print('\t\t{:22} {:8.1f}'.format(p.name, r))
            print()

    def items_out(self):
        for l in self.legs_out():
            pass

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

    

