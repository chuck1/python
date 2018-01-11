import math
import itertools
import crayons

from process import *

class Transport:
    def __init__(self, name, rate):
        self.name = name
        self.rate = rate

express_belt = Transport("express belt", 40)

class Product:
    def __init__(self, name, transport=[]):
        self.name = name
        self.transport = transport

    def processes(self):
        #processes = [p for p in globals().values() if isinstance(p, Process)]

        #for p in processes:
        #    print(p.name)
        
        for p in Process.processes:
            for i in p.inputs:
                if i.product == self:
                    if i.q < 0:
                        yield p
                        break

    def belt_lanes(self):
        p = self.process_default
        inputs = list(p.inputs)
        inputs = [i.mul(1 / p.t) for i in inputs if express_belt in i.product.transport]
        lanes = sum(i.lanes for i in inputs)
        return lanes

    def production_building_row_length(self):
        print()
        print(crayons.blue(self.name, bold=True))
        print("production building row length")
        print()
        
        p = self.process_default
        inputs = list(p.inputs)

        # get inputs delivered on belts
        # multiply by production rate to get input rate
        inputs = [ProductInput(i.product, i.q / p.t, i.lanes) for i in inputs if express_belt in i.product.transport]

        #inputs.append(ProductInput(self, self.rate, 1))
        
        for i in inputs:
            if i.lanes is None:
                print(i.product.name, "lanes is none")

        x = [(i.lanes * 18) / abs(i.q) for i in inputs]

        y = min(x)

        y = math.floor(y)
        
        #y = min(y, math.floor(18 / self.rate))
        y = min(y, 30)

        print("{:32} {:8} {:8} {:14}".format("item", "rate", "lanes", "max buildings"))
        for i, z in zip(inputs, x):
            print("{:32} {:8.2f} {:8} {:14.2f} {:14.2f}".format(i.product.name, i.q, i.lanes, z, i.q * y))
        
        
        print()
        
        i = next(i for i in inputs if i.product == self)

        print("max buildings: {:8d}".format(y))
        print("output rate:   {:8.2f}".format(y * i.q))
        
        #y2 = math.floor(18 / self.rate)
        #if y2 < y:
        #    print("buildings for max 18 output rate:", y2)
        
        print()

        return y

    def raw(self, x):

        inputs = list(self.inputs)

        while True:
            intermediates = [i for i in inputs if i.product.inputs]
            if not intermediates: break

            i = intermediates[0]

            inputs.remove(i)

            for r in i.product.raw(1.0):
                inputs.append(r.mul(i.q))

        inputs = sorted(inputs, key=lambda i: id(i.product))

        for k, g in itertools.groupby(inputs, key=lambda i: i.product):
            s = sum([i.q for i in g]) * x

            yield ProductInput(k, s)

    def all_inputs(self, x):

        inputs = []

        for i in self.inputs:

            inputs.append(i)

            for r in i.product.all_inputs(1.0):
                inputs.append(r.mul(i.q))

        inputs = sorted(inputs, key=lambda i: id(i.product))
        
        for k, g in itertools.groupby(inputs, key=lambda i: i.product):
            s = sum([i.q for i in g]) * x

            yield ProductInput(k, s)

    def default_process(self):
        if not hasattr(self, "process_default"):
            raise RuntimeError("{} does not have a default process".format(self.name))
        return self.process_default

class IntermediateProduct(Product):
    def __init__(self, name, stack_size):
        super(IntermediateProduct, self).__init__(name, [express_belt])
        self.stack_size = stack_size


