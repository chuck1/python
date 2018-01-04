import math
import itertools
import crayons

from products import *
from product import *

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

class Process:
    def __init__(self, name, inputs, t):
        self.name = name
        self.inputs = inputs
        self.t = t

    def all_inputs(self, x):
        return all_inputs2(x, [(i, None) for i in self.inputs if i.q > 0])

    def raw(self, x):
        return all_raw2(x, Raw([(i, None) for i in self.inputs]))

        """
        inputs = []

        for i in self.inputs:

            inputs.append(i)

            for r in i.product.all_inputs(1.0):
                inputs.append(r.mul(i.q))

        inputs = sorted(inputs, key=lambda i: id(i.product))
        
        for k, g in itertools.groupby(inputs, key=lambda i: i.product):
            s = sum([i.q for i in g]) * x
            #print(k.name, s)

            yield ProductInput(k, s)
        """


