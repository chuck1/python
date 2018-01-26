import copy
import enum
import numpy as np

from .blueprint import *

def floor_(x, y):
    return (x // y) * y


def pipes_y(x, y0, y1):
    for y in range(y0, y1 + 1):
        yield Entity({'name': 'pipe'}, [x, y])

def rails_y(x, y0, y1):
    for y in np.arange(y0, y1, 2):
        yield Entity({'name': 'straight-rail'}, [x, y])

def fluid_train_stop(wagons):
    return Group([
        Group(tile(fluid_wagon_stop(), 1, wagons, x=0, y=1)),
        Group(rails_y(0.5, 0.5, 0.5 + floor_(wagons * 7, 2))),
        ])

def train_stop(wagons, frac_loading):
    return Group([
        Group(tile(wagon_stop(frac_loading), 1, wagons, x=0, y=1)),
        Group(rails_y(0.5, 0.5, 0.5 + floor_(wagons * 7, 2))),
        ])

def fluid_wagon_stop():
    return Group([
        Entity({'name':'pump'}, [-1.5, 0]),
        Entity({'name':'tank'}, [-4.0, 1]),
        ])

def wagon_stop(frac_loading):

    def inserter_and_chest_positions():
        for i in range(6):
            yield [-1, i], [-2, i]
        for i in range(6):
            yield [2, i], [3, i]
    
    p = inserter_and_chest_positions()

    l = int(round(12 * frac_loading))
    u = 12 - l

    def inserters_and_chests():
        for i in range(l):
            p0, p1 = next(p)
            yield Entity({'name':'inserter'}, p0)
            yield Entity({'name':'requester-chest'}, p1)
        for i in range(u):
            p0, p1 = next(p)
            yield Entity({'name':'inserter'}, p0)
            yield Entity({'name':'passive-provider-chest'}, p1)
        
    return Group([
        Group(inserters_and_chests()),
        ])

def assembling_pipe():
    b = Blueprint()
    
    g1 = Group([
        Entity({'name': 'assembling-machine-1'}, [2, 0]),
        ])
    g1 = Group(tile(g1, 1, 2))
   
    g2 = Group([
        Entity({'name': 'assembling-machine-1'}, [8, 0]),
        ])
    g2 = Group(tile(g2, 1, 2))
   
    inserters1 = Group([
        Entity({'name': 'inserter'}, [4, -1]),
        Entity({'name': 'inserter'}, [4, 0]),
        Entity({'name': 'inserter'}, [6, -1]),
        Entity({'name': 'inserter'}, [6, 0]),
        ])
    inserters2 = copy.deepcopy(inserters1)
    inserters2.shift([0, 4])

    chests1 = Group([
        Entity({'name': 'requester-chest'}, [5, -1]),
        Entity({'name': 'passive-provider-chest'}, [5, 0]),
        ])
    chests2 = copy.deepcopy(chests1)
    chests1.shift([0, 4])

    g = Group([
        g1,
        g2,
        inserters1,
        inserters2,
        chests1,
        chests2,
        Group(tile(Entity({'name': 'beacon'}, [12, 0]), 1, 2)),
        Group(pipes_y(0, -1, 4)),
        Group(pipes_y(10, -1, 4)),
        Entity({'name': 'substation'}, [5.5, 1.5]),
        ])
    
    b.entities.append(Group(tile(g, m, n)))
    
    return b


def assembling():
    g1 = Group([
        Entity({'name': 'assembling-machine-1'}, [0, 0]),
        ])
    g1 = Group(tile(g1, 1, 2))
   
    g2 = Group([
        Entity({'name': 'assembling-machine-1'}, [6, 0]),
        ])
    g2 = Group(tile(g2, 1, 2))
   
    inserters1 = Group([
        Entity({'name': 'inserter'}, [2, -1]),
        Entity({'name': 'inserter'}, [2, 0]),
        Entity({'name': 'inserter'}, [4, -1]),
        Entity({'name': 'inserter'}, [4, 0]),
        ])
    inserters2 = copy.deepcopy(inserters1)
    inserters2.shift([0, 4])

    chests1 = Group([
        Entity({'name': 'requester-chest'}, [3, -1]),
        Entity({'name': 'passive-provider-chest'}, [3, 0]),
        ])
    chests2 = copy.deepcopy(chests1)
    chests1.shift([0, 4])

    g = Group([
        g1,
        g2,
        inserters1,
        inserters2,
        chests1,
        chests2,
        Group(tile(Entity({'name': 'beacon'}, [9, 0]), 1, 2)),
        Entity({'name': 'substation'}, [3.5, 1.5]),
        ])
    
    g.shift([g.x_min(), g.y_min()])

    return g









