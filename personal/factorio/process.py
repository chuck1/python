import math
import itertools
import crayons

#from products import *
from ingredient import *

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
        
class Process:
    def __init__(self, name, inputs, t, power=None, has_site=False):
        self.name = name
        self.inputs = inputs
        self.t = t
        self.has_site = has_site
        
        if power is not None:
            self.inputs.append(ProductInput(self.electrical_energy, power * t))
    
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

    def items_per_cycle(self, product):
        try:
            i = next(i for i in self.inputs if i.product == product)
        except StopIteration:
            raise RuntimeError("{} not found in {}".format(product.name, self.name))
        return i.q

    def buildings(self, product, rate):
        i = self.items_per_cycle(product)
        c = rate / i
        return c * self.t

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
           
            p = i.product.process_default

            c1 = i1.q / -p.items_per_cycle(i.product)

            for i2 in p.excess_default(c1, track):
                inputs.append(i2)

        inputs = sorted(inputs, key=lambda i: id(i.product))

        for k, g in itertools.groupby(inputs, key=lambda i1: i1.product):
            g = list(g)
            
            s = sum([i.q for i in g])
            
            yield ProductInput(k, s)


    def all_inputs_default(self, c0, track=None):
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
            
            p = i.product.default_process()
            
            # use excess available

            rate = i1.q

            c1 = rate / -p.items_per_cycle(i.product)
           
            g = p.all_inputs_default(c1, track)

            for i2 in g:
                inputs.append(i2)

        inputs = sorted(inputs, key=lambda i: id(i.product))

        for k, g in itertools.groupby(inputs, key=lambda i1: i1.product):
            g = list(g)
            
            s = sum([i.q for i in g if i.q > 0])
            
            yield ProductInput(k, s)

    def count_outputs(self):
        return len(i for i in p.inputs if i.q < 0)

def excess_in(inputs, product):
    #inputs = [i for i in inputs if i.product == product]
    return sum(i.q for i in inputs if i.product == product)



