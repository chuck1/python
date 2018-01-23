import math
import itertools
import contextlib
import crayons

#from products import *
from ingredient import *
from product import *
from constants import *

@contextlib.contextmanager
def stack_context(stack, product):

    if product in stack:
        b = True
    else:
        b = False
    
    stack.append(product)

    yield b
    
    stack.pop()


def insert_process(l, product, process):
    for i, p in l:
        if i.product == product:
            yield i, process

            for i1 in process.inputs:
                if i1.q > 0:
                    yield i1, None

        else:
            yield i, p


def all_inputs3(x, inputs):
    for i, process in inputs:
        yield i, process
    
        #for i1 in process.inputs:
        #    print(i1.product.name)
        
def all_inputs2(x, inputs):
    if True:
        print("all_inputs2")
        for i, process in inputs:
            print("\t{:32} {}".format(i.product.name, str(process)))
    
    for i, process in inputs:
        if process is None:
            for p in i.product.processes():
                yield from all_inputs2(x, list(insert_process(inputs, i.product, p)))
            break
    
    if all([process is not None for i, process in inputs]):
        #yield inputs
        yield all_inputs3(x, inputs)

        #for i, process in inputs:

class Raw:
    def __init__(self, inputs, final=[]):
        self.inputs = inputs
        self.final = final
    
    def copy(self):
        return Raw(list(self.inputs), list(self.final))

    def insert_process(self, product, process):

        i2 = next(i for i in process.inputs if i.product == product)
        
        t = next((i, p) for i, p in self.inputs if i.product == product)

        self.inputs.remove(t)
        
        self.final.append(t)

        i, p = t

        process_rate = i.q / -i2.q
        #print("process rate:", process_rate)

        for i1 in process.inputs:
            if i1.q < 0:
                self.final.append((ProductInput(i1.product, process_rate * i1.q), process))
            else:
                self.inputs.append((ProductInput(i1.product, process_rate * i1.q), None))

    def group(self):
        for k, g in itertools.groupby(self.final, key=lambda t: t[0].product):
            s = sum([i.q for i, p in g])
            yield ProductInput(k, s)

def all_raw2(x, raw):
    if False:
        print("all_raw2")
        for i, process in raw.inputs:
            print("\t{:32} {}".format(i.product.name, str(process)))
    
    for i, process in raw.inputs:
        if i.q < 0:
            continue

        if process is None:
            for p in i.product.processes():
                raw1 = raw.copy()
                raw1.insert_process(i.product, p)
                yield from all_raw2(x, raw1)
            break
    
    if all([(process is not None) or (i.q < 0) for i, process in raw.inputs]):
        yield raw
        #yield all_raw3(x, inputs)

        #for i, process in inputs:

class VirtualProcess:
    def __init__(self, product, processes):
        self.product = product
        self.processes = processes

    def ingredients(self, X):
        # X - process cycles per process cycle
        # returns items per process cycle

        if len(X) != self.process_count():
            raise RuntimeError("length of X must equal the process count")

        for p in self.processes:

            X1 = X[:(p.process_count() + 1)]
            X = X[(p.process_count() + 1):]
            
            x = X1[0]
            
            #print(p)
            #print(X1[1:])
            for i in p.ingredients(X1[1:]):
                yield i.mul(x)
    
    def ingredients_grouped(self, X):
        
        l = list(self.ingredients(X))
        
        l = sorted(l, key=lambda i: id(i.product))

        for k, g in itertools.groupby(l, key=lambda i: i.product):
            s = sum([i.q for i in g])
            yield ProductInput(k, s)

    def process_count(self):
        c = len(self.processes)
        for p in self.processes:
            c += p.process_count()
        return c

class SpeedModule3:
    def __init__(self, s = 1):
        self.s = s
        self.speed = 0.5 * s
        self.power = 0.7 * s
        self.productivity = 0 * s
    
    def __str__(self):
        return 'Speed Module 3 ({})'.format(self.s)

class ProductivityModule3:
    def __init__(self, s = 1):
        self.s = s
        self.speed = -0.15 * s
        self.power = 0.80 * s
        self.productivity = 0.10 * s

    def __str__(self):
        return 'Productivity Module 3 ({})'.format(self.s)

class Process:
    def __init__(self, name, inputs, t, power=None, has_site=False, building=None):
        self.name = name
        self._inputs = inputs
        self.t = t
        self.has_site = has_site
        self.building = building
        
        self.power = power
        #if power is not None:
        #    self.inputs.append(ProductInput(self.electrical_energy, power * t))
        
        self.modules = []

    @property
    def speed_modifier(self):
        x = 1
        for m in self.modules:
            x += m.speed
        return x

    @property
    def power_modifier(self):
        x = 1
        for m in self.modules:
            x += m.power
        return x

    @property
    def productivity_modifier(self):
        x = 1
        for m in self.modules:
            x += m.productivity
        return x

    @property
    def power_input(self):
        if self.power is not None:
            p = self.power * self.t * self.power_modifier
            return ProductInput(self.electrical_energy, p)

    def get_base_speed(self):
        if self.building is None:
            return 1
        return self.building.base_speed

    @property
    def inputs(self):
        s = self.speed_modifier
        p = self.productivity_modifier

        for i in self._inputs:
            m = self.get_base_speed() * s

            if i.q < 0:
                m *= p
            
            yield i.mul(m)

        if self.power is not None:
            yield self.power_input

    def print_(self):
        print(self.name)
        
        for i in self.inputs:
            print("{:32} {:10.3f}".format(i.product.name, i.q / self.t))

        #i = self.power_input
        #print("{:32} {:10.3f}".format(i.product.name, i.q / self.t))

    def process_count(self):
        return 0

    def ingredients(self, X):
        # returns items per process cycle
        if X:
            raise RuntimeError()

        for i in self.inputs:
            yield i

    def all_inputs(self, x):
        return all_inputs2(x, [(i, None) for i in self.inputs if i.q > 0])

    def raw(self, x):
        return all_raw2(x, Raw([(i, None) for i in self.inputs]))

    def ingredient(self, product):
        try:
            i = next(i for i in self.inputs if i.product == product)
        except StopIteration:
            raise RuntimeError("{} not found in {}".format(product.name, self.name))
        return i

    def items_per_cycle(self, product):
        try:
            i = next(i for i in self.inputs if i.product == product)
        except StopIteration:
            raise RuntimeError("{} not found in {}".format(product.name, self.name))
        return i.q

    def cycles_per_second(self, i):
        r = self.items_per_cycle(i.product)
        c = i.q / r
        print('Process {} Product {} rate {} items per cycle {} cycles per second {}'.format(
            self.name,
            i.product.name,
            i.q,
            r,
            c,
            ))

        return c

    def buildings(self, product, rate):
        i = self.items_per_cycle(product)
        c = rate / i
        b = c * self.t
        print('Process {} Product {} rate {} items per cycle {} cycles per second {} buildings {}'.format(
            self.name,
            product.name, 
            rate,
            i,
            c,
            b))

        return b

    def excess_default(self, c0, track=None):
        # c0 - cycles per second
        # returns list of input items in items per second
        
        inputs = []

        for i in self.inputs:
            i1 = i.mul(c0)

            if track is not None:
                if not i1.product in track:
                    track[i1.product] = []
                track[i1.product].append((self, i1))
            
            inputs.append(i1)
 
            if i.q < 0:
                continue

            if i.product == self.electrical_energy:
                continue
           
            p = i.product.process_default

            c1 = i1.q / -p.items_per_cycle(i.product)

            for i2 in p.excess_default(c1, track):
                inputs.append(i2)

        inputs = sorted(inputs, key=lambda i: id(i.product))

        for k, g in itertools.groupby(inputs, key=lambda i1: i1.product):
            g = list(g)
            
            s = sum([i.q for i in g])
            
            yield ProductInput(k, s)


    def all_inputs_default(self, c0, track=None, stack=[], ignore_power=False):
        # c0 - cycles per second
        # returns list of input items in items per second
            
        inputs = []
            
        for i in self.inputs:
            if ignore_power:
                if Process.electrical_energy is None:
                    raise RuntimeError()
                if i.product == Process.electrical_energy:
                    continue

            with stack_context(stack, i.product) as b:
                i1 = i.mul(c0)

                #print('all inputs default i {} {} c {}'.format(i.product.name, i.q, c0))
    
                if track is not None:
                    if not i1.product in track:
                        track[i1.product] = []
                    track[i1.product].append((self, i1))
                
                inputs.append(i1)
    
                if i.q < 0:
                    continue

                if b: 
                    continue
               
                #if i.product == self.electrical_energy:
                #    continue
    
                p = i.product.default_process()
                
                # use excess available
    
                rate = i1.q
    
                c1 = rate / -p.items_per_cycle(i.product)
               
                g = p.all_inputs_default(c1, track, stack, ignore_power)
                
                for i2 in g:
                    inputs.append(i2)
    
        inputs = sorted(inputs, key=lambda i: id(i.product))
    
        for k, g in itertools.groupby(inputs, key=lambda i1: i1.product):
            g = list(g)
                
            s = sum([i.q for i in g if i.q > 0])
                
            yield ProductInput(k, s)

    def count_outputs(self):
        return len(i for i in p.inputs if i.q < 0)

    def footprint_per_building(self):
        
        if self.building == Constants.electric_mining_drill:
            if self == Constants.mine_uranium_ore:
                pass
            else:
                return BuildingLayout(7, 3, 2 / 3)

        liquid_output = sum(1 for i in self._inputs if isinstance(i.product, Liquid) and i.q < 0)
        liquid_input = sum(1 for i in self._inputs if isinstance(i.product, Liquid) and i.q > 0)
        item_output_gt_zero = sum(1 for i in self._inputs if (not isinstance(i.product, Liquid)) and i.q < 0) > 0
        item_input_gt_zero = sum(1 for i in self._inputs if (not isinstance(i.product, Liquid)) and i.q > 0) > 0

        k = (liquid_output, liquid_input, item_output_gt_zero, item_input_gt_zero)

        d = {
                (1, 0, False, False): None,
                (1, 0, False, True): BuildingLayout(3, 14, 2),
                (0, 0, True, True): BuildingLayout(3, 12, 2),
                (0, 1, True, True): BuildingLayout(3, 14, 2),
                (0, 1, True, False): BuildingLayout(3, 14, 2),
                (0, 2, True, True): BuildingLayout(3, 15, 2),
                (0, 2, True, False): BuildingLayout(3, 15, 2),
                (3, 2, False, False): BuildingLayout(6, 22, 2), # oil refinery
                }
        
        return d[k]

class BuildingLayout:
    def __init__(self, tile_x, tile_y, buildings_per_tile):
        self.tile_x, self.tile_y, self.buildings_per_tile = tile_x, tile_y, buildings_per_tile
        self.footprint = self.tile_x * self.tile_y / self.buildings_per_tile

def excess_in(inputs, product):
    #inputs = [i for i in inputs if i.product == product]
    return sum(i.q for i in inputs if i.product == product)



