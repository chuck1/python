import copy
import itertools
import numpy as np
import crayons
from product import *
import matplotlib.pyplot as plt
import scipy.optimize

from constants import *
from fact.graph.edge import *

import blueprints as bp
import blueprints.build_1
import blueprints.templates

def pythag(a, b, c):
    d = math.sqrt(b**2 - 4 * a * c)
    return (-b + d) / 2 / a, (-b - d) / 2 / a

def cargo_wagons_per_second(products):
    w = 0
    for k, r in products:
        process, product = k
        if not isinstance(product, IntermediateProduct): continue
        w += r / product.stack_size / 40
    return w

class Subfactory:
    def __init__(self, stations, stops_c, stops_f, count_x, count_y):
        self.stations = stations
        
        self.stops_c = stops_c
        self.stops_f = stops_f

        self.count_x = count_x
        self.count_y = count_y

    def blueprint(self):

        stop_blueprints = [bp.templates.train_stop(Constants.train_configuration.wagons, s.load_inserter_fraction) for s in self.stations]

        g = blueprints.build_1.subfactory(
                    blueprints.templates.assembling(), 
                    self.stops_c,
                    stop_blueprints,
                    self.count_y, 
                    self.count_x)

        b = blueprints.blueprint.Blueprint()
        b.entities.append(g)
        b.plot()
        
        #stops_x_1 = i_x / ips


class RouteLegProduct:
    def __init__(self, product, rate):
        self.product = product
        self.rate = rate
    
    def to_string(self):
        return '{:22} {:8.1f}'.format(self.product.name, self.rate)

    def show(self):
        print('\t\t' + self.to_string())

    def slots(self):
        if isinstance(self.product, Liquid):
            return 0

        return self.rate / self.product.stack_size



def load_time(d):
    ins_rate = 27.7
    
    ins_per_wagon_load = 6
    ins_per_wagon_unload = 6
    
    items_load = sum(r for p, r in d if r > 0)
    items_unload = sum(r for p, r in d if r < 0)
    
    print(items_load)
    print(items_unload)
    
    
def correct_answer(x, y):
    if (x < 0) and (y > 0): return y
    if (x > 0) and (y < 0): return x
    raise RuntimeError()

class Station:
    def __init__(self, type_, w_c, w_f, load_inserter_fraction):
        self.type_ = type_
        self.w_c, self.w_f, self.load_inserter_fraction = w_c, w_f, load_inserter_fraction

class Node:
    def __init__(self, g, name, process, c, product, position):
        self.g = g
        self.name = name
        self.process = process
        self.cycles_per_second = c
        self.product = product
        self.position = position

    def buildings(self):
        return self.cycles_per_second * self.process.t

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
        legs_thru = list(self.legs_thru())

        if legs_thru:
            return ['thru']

        return ['term', 'orig']
    
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

    def leg_compatible(self, leg, station):
        if station == 'thru':
            return True

        return self.get_leg_type(leg) == station

    def fluid_wagon_stops_for_product(self, leg, p, r, ins_frac):
        
        if not isinstance(p, Liquid):
            return 0

        Constants.fluid_wagon_pump_rate = 1000
        Constants.pumps_per_wagon = 12
        Constants.fluid_wagon_capacity = 25000

        # TODO consider if we were only partially draining or filling the tank
        
        t = Constants.fluid_wagon_capacity / (Constants.fluid_wagon_pump_rate * Constants.pumps_per_wagon)

        utilization = t / (t + Constants.train_transition_time)

        wagon_stops = r / (Constants.fluid_wagon_pump_rate * Constants.pumps_per_wagon) / utilization

        return wagon_stops

    def cargo_wagon_stops_for_product(self, leg, p, r, ins_frac):
        if isinstance(p, Liquid):
            return 0
        
        slots = r / p.stack_size

        if leg.route.slots() == 0:
            leg.route.show()

        wagon_capacity = slots / leg.route.slots() * 40 * p.stack_size

        if ins_frac == 0:
            print('inserters for product {} {} ins_frac={}'.format(p.name, r, ins_frac))
            return float("inf")

        t = wagon_capacity / (12 * Constants.inserter_rate * ins_frac)

        utilization = t / (t + Constants.train_transition_time)

        i = r / Constants.inserter_rate / utilization

        wagon_stops = i / Constants.inserters_per_wagon

        return wagon_stops

    def cargo_wagon_stops_for_leg(self, leg, ins_l_frac, ins_u_frac):
        leg0, leg1 = leg
        
        cargo_wagon_stops_load = 0
        cargo_wagon_stops_unload = 0

        for p, r in leg_difference(leg0, leg1):
            #print('product', p.name, r, 'ins_l_frac', ins_l_frac, 'ins_u_frac', ins_u_frac)
            if r > 0:
                c = self.cargo_wagon_stops_for_product(leg0 or leg1, p, r, ins_l_frac)
                cargo_wagon_stops_load += c
            if r < 0:
                c = self.cargo_wagon_stops_for_product(leg0 or leg1, p, -r, ins_u_frac)
                cargo_wagon_stops_unload += c

        c_0 = 0
        if ins_l_frac == 0:
            if cargo_wagon_stops_load != 0:
                print('failed', ins_l, ins_l_frac)
                return float("inf")
        else:
            c_0 = cargo_wagon_stops_load / ins_l_frac

        c_1 = 0
        if ins_u_frac == 0:
            if cargo_wagon_stops_unload != 0:
                print('failed', ins_u, ins_u_frac)
                return float("inf")
                return None
        else:
            c_1 = cargo_wagon_stops_unload / ins_u_frac

        return max(c_0, c_1)
    
    def fluid_wagon_stops_for_leg(self, leg, ins_l_frac, ins_u_frac):
        leg0, leg1 = leg
        
        fluid_wagon_stops_load = 0
        fluid_wagon_stops_unload = 0

        for p, r in leg_difference(leg0, leg1):
            #print('product', p.name, r, 'ins_l_frac', ins_l_frac, 'ins_u_frac', ins_u_frac)
            if r > 0:
                f = self.fluid_wagon_stops_for_product(leg0 or leg1, p, r, ins_l_frac)
                fluid_wagon_stops_load += f
            if r < 0:
                f = self.fluid_wagon_stops_for_product(leg0 or leg1, p, -r, ins_u_frac)
                fluid_wagon_stops_unload += f

        return fluid_wagon_stops_load + fluid_wagon_stops_unload

    def test_layout_station(self, station, stations, ins_l_frac):
        ins_u_frac = 1 - ins_l_frac

        legs = list(self.legs())
    
        ws_c = 0
        ws_f = 0

        for leg in legs:
            if not self.leg_compatible(leg, station):
                continue

            ws_c += self.cargo_wagon_stops_for_leg(leg, ins_l_frac, ins_u_frac)
            ws_f += self.fluid_wagon_stops_for_leg(leg, ins_l_frac, ins_u_frac)

        return ws_c, ws_f

    def test_layout(self, stations):
        
        legs = list(self.legs())
        
        ws_c = 0
        ws_f = 0
        
        ret = []
        
        for station in stations:
            
            def func(ins_l_frac):
                return self.test_layout_station(station, stations, ins_l_frac)

            def func1(X):
                ins_l_frac = X[0]
                y_c, y_f = self.test_layout_station(station, stations, ins_l_frac)
                return y_c
            
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
            y_c, y_f = f(ins_l_frac)
            
            #plt.plot(ins_l_frac, y)
            
            y_c, y_f = func(x)
            #plt.plot(x,y,'o')
            
            #print(station, 'optimal ins_l_frac: {:7.3f} ins: {:8.1f}'.format(x, y))

            ret.append(Station(station, y_c, y_f, x))

            ws_c += y_c
            ws_f += y_f

        return stations, ws_c, ws_f, ret

    def subfactory_test(self, w, h, bl, stations, B, ips):
        
        if bl.footprint == 0:
            return
        
        WS_c = np.array([s.w_c for s in stations])
        WS_f = np.array([s.w_f for s in stations])

        stops = np.zeros(np.shape(WS_c))
        
        for a in range(20):

            h_p = h - 6 * np.sum(stops)

            a_p = w * h_p
        
            b = a_p / bl.footprint

            stops_0 = np.array(stops)
        
            ws_c = WS_c / B * b
           
            stops = ws_c / Constants.train_configuration.wagons
            
            stops[stops < 0] = 0

            stops = (stops + stops_0) / 2

            if np.all(np.abs(stops - stops_0) < 1e-4):
                break
            
            #print('stops: {}'.format(' '.join('{:8.3f}'.format(x) for x in s)))

        stops = np.ceil(stops)
        ws = stops * Constants.train_configuration.wagons
        b = B / WS_c * ws_c

        ws_f = WS_f / B * b
        stops_f = np.ceil(ws_f / Constants.train_configuration.wagons)
    
        b = np.amin(b)

        a_p = b * bl.footprint

        #print('b {} a_p {}'.format(b, a_p))
        
        height_stops = np.sum(stops) * 6

        w = correct_answer(*pythag(1, -height_stops, -a_p))

        h_p = a_p / w
        count_y = math.ceil(h_p / bl.tile_y)
        h_p = count_y * bl.tile_y

        w = a_p / h_p
        count_x = math.floor(w / bl.tile_x)
        w = count_x * bl.tile_x

        a_p = w * h_p

        b = a_p / bl.footprint

        print('cargo stops ', stops)
        print('fluid stops ', stops_f)
        print('w           ', w)
        print('h_p         ', h_p)
        print('a_p         ', a_p)
        print('b           ', b)
        print('count x     ', count_x)
        print('count y     ', count_y)
        print('subfactories', math.ceil(B / b))
       
        return Subfactory(stations, stops, stops_f, count_x, count_y)


    def factory_layout(self):
        print(crayons.blue('factory: {}'.format(self.process.name), bold=True))
        print('modules:', [str(m) for m in self.process.modules])

        # options for factory layout:
        
        stations = self.layout_options()

        res = self.test_layout(stations)
        
        stations, ws_c, ws_f, ret = res

        print('optimal:')
        print(stations)
        for station in ret:
            print('{} {:7.3f} ws_c {:10.3f} ws_f {:10.3f}'.format(station.type_, station.load_inserter_fraction, station.w_c, station.w_f))

            if math.isinf(ws_c):
                raise RuntimeError()

        inserters_per_stop = 12 * Constants.train_configuration.wagons

        b0 = self.buildings()

        bl = self.process.footprint_per_building()

        if bl is None: return

        fp = bl.footprint

        width = Constants.wagons_per_train * 7

        area = b0 * fp

        if b0 > 0:
            #WS_c = [ws_c for station, ins_l_frac, ws_c, ws_f in ret if ws_c > 0]
            #WS_f = [ws_f for station, ins_l_frac, ws_c, ws_f in ret if ws_c > 0]
            #if WS_c:
            subfactory = self.subfactory_test(100, 100, bl, ret, b0, inserters_per_stop)

            subfactory.blueprint()
        

        # another calculation of the number of stops of each type needed to serve a logisitic area of my chosing
        # need function ...

        def get_items_load(legs):
            return sum(r for l0, l1 in legs for p, r in leg_difference(l0, l1) if r > 0)
        
        def get_items_unload(legs):
            return sum(r for l0, l1 in legs for p, r in leg_difference(l0, l1) if r < 0)
        
        print('buildings:       {:8.1f}'.format(self.buildings()))
        print('area (sq tile):  {:8.1f}'.format(area))
        print('area (sq chunk): {:8.1f}'.format(area / 32 / 32))

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





