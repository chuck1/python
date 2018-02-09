import math
import sys
import json
from pprint import pprint
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.ticker as plticker
import numpy as np
import enum
import copy
import progressbar

class EntityPosition:
    def __init__(self):
        pass
    def __get__(self, instance, owner):
        #print('get')
        #print(instance)
        #print(owner)
        #p = p0 + g.p
        #p0 = p - g.p
        
        #if instance.group is not None:
        #    return instance.__position + instance.group.position
        #else:
        return instance.__position

    def __set__(self, instance, value):
        #print('set')
        #print(instance)
        #print(value)
        #if instance.group is not None:
        #    instance.__position = value - instance.group.position
        #else:
        instance.__position = value

        instance.invalidate()
    def __delete__(self, instance):
        print('delete')
        print(instance)
        raise Exception()


