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
    
    


