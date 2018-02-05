import copy
import itertools
import numpy as np
import crayons
from product import *
import matplotlib.pyplot as plt
import scipy.optimize

from constants import *
from fact.graph.edge import *
from fact.util import *
from fact.subfactory import *

import blueprints as bp
import blueprints.build_1
import blueprints.templates

class LegPair:
    def __init__(self, leg0, leg1):
        self.leg0 = leg0
        self.leg1 = leg1

    def trains_per_sec(self):
        return (self.leg0 or self.leg1).route.trains_per_second()

    def is_thru(self):
        l = sum(1 for ir in self.difference() if ir.rate > 0)
        u = sum(1 for ir in self.difference() if ir.rate < 0)

        if (l == 0) and (u == 0):
            raise RuntimeError()

        return (l > 0) and (u > 0)

    def is_orig(self):
        l = sum(1 for ir in self.difference() if ir.rate > 0)
        u = sum(1 for ir in self.difference() if ir.rate < 0)

        if (l == 0) and (u == 0):
            raise RuntimeError()

        return (l > 0) and (u == 0)

    def is_term(self):
        l = sum(1 for ir in self.difference() if ir.rate > 0)
        u = sum(1 for ir in self.difference() if ir.rate < 0)

        if (l == 0) and (u == 0):
            raise RuntimeError()

        return (l == 0) and (u > 0)

    def route_string(self):
        s = []
        if self.leg0 is not None:
            s.append('{:24}'.format(self.leg0.edge.src.name))
        
        if self.leg0 is not None:
            s.append('{:24}'.format(self.leg0.edge.dst.name))
        else:
            s.append('{:24}'.format(self.leg1.edge.src.name))

        if self.leg1 is not None:
            s.append('{:24}'.format(self.leg1.edge.dst.name))
        
        return ' -> '.join(s)

    def route(self):
        return (self.leg0 or self.leg1).route

    def difference(self):
        return leg_difference(self.leg0, self.leg1)

    def show(self):
        print('leg pair')
        if self.leg0 is not None:
            print('{:24} -> {:24}'.format(self.leg0.edge.src.name, self.leg0.edge.dst.name))
            self.leg0.show()
        if self.leg1 is not None:
            print('{:24} -> {:24}'.format(self.leg1.edge.src.name, self.leg1.edge.dst.name))
            self.leg1.show()

        print('items')
        for ir in self.difference():
            print('\t {}'.format(ir.item.name))

    def cargo_wagon_stops(self, ins_l_frac, ins_u_frac):
       
        ws_c_load = 0
        ws_c_unload = 0

        for ir in self.difference():
            if ir.rate > 0:
                c = ir.cargo_wagon_stops(self.route(), ins_l_frac)
                
                if ins_l_frac == 0:
                    print('leg cargo wagon stops {} {} but load frac {}'.format(ir.item.name, ir.rate, ins_l_frac))
                    raise RuntimeError()

                ws_c_load += c

            if ir.rate < 0:
                c = -ir.cargo_wagon_stops(self.route(), ins_u_frac)
                ws_c_unload += c

        c_0 = 0
        if ins_l_frac == 0:
            if ws_c_load != 0:
                print('failed', ws_c_load, ins_l_frac)
                raise RuntimeError()
                return float("inf")
        else:
            c_0 = ws_c_load / ins_l_frac

        c_1 = 0
        if ins_u_frac == 0:
            if ws_c_unload != 0:
                print('failed', ins_u, ins_u_frac)
                raise RuntimeError()
                return float("inf")
                return None
        else:
            c_1 = ws_c_unload / ins_u_frac
        
        return max(c_0, c_1)

    def fluid_wagon_stops(self):
        
        ws_f_load = 0
        ws_f_unload = 0

        for ir in self.difference():
            if ir.rate > 0:
                f = ir.fluid_wagon_stops(self.route())
                ws_f_load += f

            if ir.rate < 0:
                f = -ir.fluid_wagon_stops(self.route())
                ws_f_unload += f

        return ws_f_load + ws_f_unload


class Station:
    def __init__(self, factory, legs):
        self.factory = factory
        self.legs = legs
    
    def trains_per_sec(self):
        return sum(leg.trains_per_sec() for leg in self.legs)

    def wagon_stops(self, node, ins_l_frac):
        ins_u_frac = 1 - ins_l_frac

        #print('{} wagon stops {:8.2f} {:8.2f}'.format(self.__class__.__name__, ins_l_frac, ins_u_frac))

        ws_c = 0
        ws_f = 0

        for leg in self.legs:
            ws_c += leg.cargo_wagon_stops(ins_l_frac, ins_u_frac)
            ws_f += leg.fluid_wagon_stops()
        
        if math.isinf(ws_c):
            raise RuntimeError()

        return ws_c, ws_f

class StationThru(Station):
    def __init__(self, factory, legs):
        super(StationThru, self).__init__(factory, legs)

    def inserter_load_fraction(self, node):

        def func1(X):
            ins_l_frac = X[0]

            y_c, y_f = self.wagon_stops(node, ins_l_frac)
            return y_c
        
        bounds = [(1e-3, 1 - 1e-3)]
        res = scipy.optimize.minimize(func1, [1e-2], bounds=bounds, method='L-BFGS-B')
        x = res.x[0]

        #print('{} load frac {}'.format(self.__class__.__name__, x))

        return x

class StationTerm(Station):
    def __init__(self, factory, legs):
        super(StationTerm, self).__init__(factory, legs)

    def inserter_load_fraction(self, node):
        return 0

class StationOrig(Station):
    def __init__(self, factory, legs):
        super(StationOrig, self).__init__(factory, legs)

    def inserter_load_fraction(self, node):
        return 1

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
                    yield LegPair(l.prev(), l)
                    break
                elif l.edge.dst == self:
                    yield LegPair(l, l.next())
                    break

   
    def items(self):
        for lp in self.legs():
            for ir in lp.difference():
                yield ir

    def logistic_robots(self):
        c = 0

        # round trip distance
        distance = 50

        for ir in self.items():
            if isinstance(ir.item, Liquid): continue
            
            c += distance * abs(ir.rate) / Constants.logistic_robot_speed / Constants.logistic_robot_cargo_size
        
        return c

    def express_belts(self):
        c = 0

        for ir in self.items():
            if isinstance(ir.item, Liquid): continue
            
            c += abs(ir.rate) / Constants.express_belt_throughput
        
        return c

    def legs_term(self):
        for leg in self.legs():
            if leg.is_term(): yield leg

    def legs_orig(self):
        for leg in self.legs():
            if leg.is_orig(): yield leg

    def legs_thru(self):
        for leg in self.legs():
            if leg.is_thru(): yield leg

    def layout_options(self):
        # produce combinations of stations
        # assign legs to stations

        #return list(s for s in self.layout_options_2() if s is not None)

        legs_thru = list(self.legs_thru())

        if legs_thru:
            return [StationThru(self, list(self.legs()))]

        return [
                StationOrig(self, list(self.legs_orig())),
                StationTerm(self, list(self.legs_term())),
                ]
   
    def station_for_leg(self, leg):

        l = sum(1 for ir in leg.difference() if ir.rate > 0)
        u = sum(1 for ir in leg.difference() if ir.rate < 0)

        if (l == 0) and (u == 0):
            return None
            leg.show()
            raise RuntimeError()

        if l == 0:
            return StationTerm(self, [leg])

        if u == 0:
            return StationOrig(self, [leg])

        return StationThru(self, [leg])

    def layout_options_2(self):

        for leg in self.legs():
            yield self.station_for_leg(leg)

    def test_layout(self, stations):
        
        legs = list(self.legs())
        
        ws_c = 0
        ws_f = 0
        
        ret = []
        
        for station in stations:
            station.stations = stations
            
            def func(ins_l_frac):
                return station.wagon_stops(self, ins_l_frac)

            def func1(X):
                ins_l_frac = X[0]
                y_c, y_f = station.wagon_stops(self, ins_l_frac)
                return y_c

            #ins_l_frac = np.linspace(0.01, 0.99, 100)
            #ins_u_frac = 1 - ins_l_frac
            
            #plt.plot(ins_l_frac, y)
            
            if False: #isinstance(station, StationThru):
                x = np.linspace(0.01, 0.99, 20)
                f = np.vectorize(func)
                y_c, y_f = f(x)
                print(y_c)
                plt.plot(x, y_c, '-')
                plt.show()

            x = station.inserter_load_fraction(self)

            y_c, y_f = station.wagon_stops(self, x)
            
            
            #print(station, 'optimal ins_l_frac: {:7.3f} ins: {:8.1f}'.format(x, y))

            #ret.append(Station(station, y_c, y_f, x))
            station.ws_c = y_c
            station.ws_f = y_f

            ws_c += y_c
            ws_f += y_f

        #return stations, ws_c, ws_f, ret
        return ws_c, ws_f, ret

    def subfactory_test(self, w, h, bl, stations, B, ips):
        # WS_c - cargo wagon stops in factory
        # WS_f - fluid wagon stops in factory

        # ws_c - cargo wagon stops in subfactory
        # ws_f - fluid wagon stops in subfactory

        # B    - building in factory
        # b    - building in subfactory

        if bl.footprint == 0:
            return
        
        WS_c = np.array([s.ws_c for s in stations])
        WS_f = np.array([s.ws_f for s in stations])

        stops_c = np.zeros(np.shape(WS_c))
        
        for a in range(20):

            h_p = h - 6 * np.sum(stops_c)

            a_p = w * h_p
        
            b = a_p / bl.footprint

            stops_0 = np.array(stops_c)
        
            ws_c = WS_c / B * b
           
            stops_c = ws_c / Constants.train_configuration.wagons
            
            stops_c[stops_c < 0] = 0

            stops_c = (stops_c + stops_0) / 2

            if np.all(np.abs(stops_c - stops_0) < 1e-4):
                break
            
            #print('stops: {}'.format(' '.join('{:8.3f}'.format(x) for x in s)))
        
        print(self.name)
        print('WS_c        ', WS_c)
        print('ws_c        ', ws_c)
        print('WS_f        ', WS_f)
        print('B           ', B)
        print('b           ', b)
        print('stops_c     ', stops_c)

        stops_c = np.ceil(stops_c)
        #ws = stops_c * Constants.train_configuration.wagons
        b = B / WS_c[WS_c > 0] * ws_c[WS_c > 0]
    
        b = np.amin(b)

        ws_f = WS_f / B * b
        stops_f = np.ceil(ws_f / Constants.train_configuration.wagons)

        a_p = b * bl.footprint

        #print('b {} a_p {}'.format(b, a_p))
        
        height_stops = np.sum(stops_c) * 6

        w = correct_answer(*quadratic(1, -height_stops, -a_p))

        h_p = a_p / w
        count_y = math.ceil(h_p / bl.tile_y)
        h_p = count_y * bl.tile_y

        w = a_p / h_p
        count_x = math.floor(w / bl.tile_x)
        w = count_x * bl.tile_x

        a_p = w * h_p

        b = a_p / bl.footprint

        subfactories = math.ceil(B / b)
        
        w_h_ratio = 2 / 3
        
        w = math.ceil(math.sqrt(B / b * w_h_ratio))
        h = math.ceil(B / b / w)

        self.subfactory_grid_width = w
        self.subfactory_grid_height = h

        # fraction of production handled by each factory
        self.subfactory_frac = 1 / subfactories

        print('w            ', w)
        print('h_p          ', h_p)
        print('a_p          ', a_p)
        print('b            ', b)
        print('stops_c      ', stops_c)
        print('stops_f      ', stops_f)
        print('count x      ', count_x)
        print('count y      ', count_y)
        print('subfactories           ', math.ceil(B / b))
        print('subfactories w         ', w)
        print('subfactories h         ', h)
        print('subfactories grid width', self.subfactory_grid_width)

        for station, stops_c_1, stops_f_1 in zip(stations, stops_c, stops_f):
            station.stops_c = stops_c_1
            station.stops_f = stops_f_1

        return Subfactory(self, stations, stops_c, stops_f, count_x, count_y, b, bl)

    def subfactory_rails_upstream(self):
        c = 0

        for station in self.stations:
            if isinstance(station, (StationTerm, StationThru)):
                c += station.stops_c
                c += station.stops_f

        return c

    def subfactory_rails_downstream(self):
        c = 0

        for station in self.stations:
            if isinstance(station, (StationOrig, StationThru)):
                c += station.stops_c
                c += station.stops_f

        return c
    
    def subfactory_trains_per_sec_upstream(self):
        x = 0

        for station in self.stations:
            if isinstance(station, StationTerm):
                # times 2 because train arrive and depart on same line
                x += station.trains_per_sec() * 2

            if isinstance(station, StationThru):
                x += station.trains_per_sec()
        
        return x * self.subfactory_frac

    def subfactory_trains_per_sec_downstream(self):
        x = 0

        for station in self.stations:
            if isinstance(station, StationOrig):
                # times 2 because train arrive and depart on same line
                x += station.trains_per_sec() * 2

            if isinstance(station, StationThru):
                x += station.trains_per_sec()
        
        return x * self.subfactory_frac

    def bus_2_trains_per_sec_upstream(self):
        return self.subfactory_trains_per_sec_upstream() * self.subfactory_grid_width

    def bus_2_rails_upstream(self):
        #return self.subfactory_rails_upstream() * self.subfactory_grid_width
        # line capacity reduction factor
        f = 0.5
        return math.ceil(self.bus_2_trains_per_sec_upstream() / Constants.train_configuration.train_line_capacity() / f)

    def bus_2_trains_per_sec_downstream(self):
        return self.subfactory_trains_per_sec_downstream() * self.subfactory_grid_width

    def bus_2_rails_downstream(self):
        #return self.subfactory_rails_upstream() * self.subfactory_grid_width
        # line capacity reduction factor
        f = 0.5
        return math.ceil(self.bus_2_trains_per_sec_downstream() / Constants.train_configuration.train_line_capacity() / f)

    def bus_1_trains_per_sec_upstream(self):
        return self.bus_2_trains_per_sec_upstream() * self.subfactory_grid_width

    def bus_1_rails_upstream(self):
        #return self.bus_2_rails_upstream() * self.subfactory_grid_width
        # line capacity reduction factor
        f = 0.5
        return math.ceil(self.bus_1_trains_per_sec_upstream() / Constants.train_configuration.train_line_capacity() / f)

    def bus_1_trains_per_sec_downstream(self):
        return self.bus_2_trains_per_sec_downstream() * self.subfactory_grid_width

    def bus_1_rails_downstream(self):
        #return self.bus_2_rails_upstream() * self.subfactory_grid_width
        # line capacity reduction factor
        f = 0.5
        return math.ceil(self.bus_1_trains_per_sec_downstream() / Constants.train_configuration.train_line_capacity() / f)

    def factory_layout_2(self, subfactory):
        
        # total width of each subfactory will be 

        # add margin of 6 to subfactory height for additional beacons

        w = self.subfactory_grid_width
        h = self.subfactory_grid_height
        
        subfactory_waiting = TrainWaitingAreaEW(2)
        
        bus_2_width_up = Constants.train_turn_radius + 1 + 4 * (self.bus_2_rails_upstream() - 1)
        bus_1_width_up = Constants.train_turn_radius + 1 + 4 * (self.bus_1_rails_upstream() - 1)

        bus_2_width_down = Constants.train_turn_radius + 1 + 4 * (self.bus_2_rails_downstream() - 1)
        bus_1_width_down = Constants.train_turn_radius + 1 + 4 * (self.bus_1_rails_downstream() - 1)

        column_width = subfactory.width() + subfactory_waiting.width() * 2 + bus_2_width_up + bus_2_width_down

        height = subfactory.height() * h + bus_1_width_up + bus_1_width_down
        width = column_width * w

        print(crayons.green('upstream'))
        print('subfactory trains           ', self.subfactory_trains_per_sec_upstream())
        print('subfactory rails            ', self.subfactory_rails_upstream())
        print()
        print('bus 2 trains                ', self.bus_2_trains_per_sec_upstream())
        print('bus 2 rails                 ', self.bus_2_rails_upstream())
        print('bus 2 width                 ', bus_2_width_up)
        print()
        print('bus 1 trains                ', self.bus_1_trains_per_sec_upstream())
        print('bus 1 rails                 ', self.bus_1_rails_upstream())
        print('bus 1 width                 ', bus_1_width_up)
        print()
        print(crayons.green('downstream'))
        print('subfactory trains           ', self.subfactory_trains_per_sec_downstream())
        print('subfactory rails            ', self.subfactory_rails_downstream())
        print()
        print('bus 2 trains                ', self.bus_2_trains_per_sec_downstream())
        print('bus 2 rails                 ', self.bus_2_rails_downstream())
        print('bus 2 width                 ', bus_2_width_down)
        print()
        print('bus 1 trains                ', self.bus_1_trains_per_sec_downstream())
        print('bus 1 rails                 ', self.bus_1_rails_downstream())
        print('bus 1 width                 ', bus_1_width_down)
        print()
        print('subfactory width            ', subfactory.width())
        print('subfactory height           ', subfactory.height())
        print('col width                   ', column_width)
        print('height                      ', height)
        print('width                       ', width)

    def factory_layout(self):
        print(crayons.blue('factory: {}'.format(self.process.name), bold=True))
        print('modules:', [str(m) for m in self.process.modules])

        # options for factory layout:
        
        stations = self.layout_options()
        self.stations = stations

        res = self.test_layout(stations)
        
        ws_c, ws_f, ret = res
        
        print('item movement')
        for lp in self.legs():
            for ir in lp.difference():
                print('\t{:24} {:8.2f}'.format(ir.item.name, ir.rate))

        print('logisitic robots: {:8}'.format(math.ceil(self.logistic_robots())))
        print('express belts:    {:8}'.format(math.ceil(self.express_belts())))
        print('optimal:')
        print(stations)
        for station in stations:
            print('{} load frac: {:7.3f} ws_c: {:10.3f} ws_f: {:10.3f}'.format(station.__class__.__name__, station.inserter_load_fraction(self), station.ws_c, station.ws_f))

            for leg in station.legs:
                print('\tleg', leg.route_string())
                for ir in leg.difference():
                   print('\t\t{:24} {:8.2f}'.format(ir.item.name, ir.rate))



            if math.isinf(ws_c):
                raise RuntimeError()
        
        inserters_per_stop = 12 * Constants.train_configuration.wagons

        b0 = self.buildings()

        bl = self.process.footprint_per_building()

        if bl is None: return

        fp = bl.footprint

        width = Constants.train_configuration.wagons * 7

        area = b0 * fp

        if b0 > 0:
            #WS_c = [ws_c for station, ins_l_frac, ws_c, ws_f in ret if ws_c > 0]
            #WS_f = [ws_f for station, ins_l_frac, ws_c, ws_f in ret if ws_c > 0]
            #if WS_c:

            if sum(s.ws_c for s in stations) > 0:

                subfactory = self.subfactory_test(50, 50, bl, stations, b0, inserters_per_stop)
                
                self.factory_layout_2(subfactory)

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


