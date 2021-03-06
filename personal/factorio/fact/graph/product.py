import copy
import itertools
import numpy as np
import crayons
from product import *
import matplotlib.pyplot as plt
import scipy.optimize

from constants import *

class RouteLegProduct:
    def __init__(self, leg, product, rate):
        self.leg = leg
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
    
    def fluid_wagons(self):
        # fluid wagons per second
        if not isinstance(self.product, Liquid): return 0

        return self.rate / Constants.fluid_wagon_capacity


