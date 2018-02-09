import copy
import enum
import numpy as np

from blueprints.blueprint import *
from blueprints.entity import *
from blueprints.group import *

def layout_x(generator):
    l = []

    for b in generator:
        if l:
            sx = l[-1].x_max - b.x_min + 1
            b.shift([sx, 0])
        l.append(b)
    
    return Group(l)

def layout_y(generator):
    l = []

    for b in generator:
        if l:
            sy = l[-1].y_max - b.y_min + 1
            b.shift([0, sy])
        l.append(b)
    
    return Group(l)


class GroupTrainStop(Group):
    def __init__(self, entities):
        super(GroupTrainStop, self).__init__(entities)


class GroupTrainStopOrig(GroupTrainStop):
    pass

class GroupTrainStopTerm(GroupTrainStop):
    pass

class GroupTrainStopThru(GroupTrainStop):
    pass

def train_stop_class(station):
    if station.is_thru(): return GroupTrainStopThru
    if station.is_orig(): return GroupTrainStopOrig
    if station.is_term(): return GroupTrainStopTerm

def pipes_y(x, y0, y1):
    for y in range(y0, y1 + 1):
        yield Entity({'name': 'pipe'}, [x, y])

def rails_y(x, y0, y1):
    for y in np.arange(y0, y1, 2):
        yield Entity({'name': 'straight-rail'}, [x, y])

def rails_x(x0, x1, y):
    for x in np.arange(x0, x1, 2):
        yield Entity({'name': 'straight-rail'}, [x, y])

def fluid_train_stop(wagons):
    return Group([
        Group(tile(fluid_wagon_stop(), 1, wagons, x=0, y=1)),
        Group(rails_y(0.5, 0.5, 0.5 + floor_(wagons * 7, 2))),
        ])

def train_stop(station, wagons, frac_loading, loco_0, loco_1):
    #rails = list(rails_y(3.0, 1.0, 1.0 + floor_(wagons * 7, 2)))

    loco_0_fuel = loco_fuel()

    wagon_stops = Group(tile(wagon_stop(frac_loading), wagons, 1, x=1, y=0))
    
    def prints():
        for i in range(loco_0): yield loco_fuel()
        yield wagon_stops
        for i in range(loco_1): yield loco_fuel()
   
    e = Entity({'name':'placeholder'}, [1.0, 3.0])

    g = train_stop_class(station)([layout_x(prints()), e])
    
    g.rail_placeholder = e

    #g.rail_west = rails[0]
    #g.rail_east = rails[-1]
    
    return g

def fluid_wagon_stop():
    return Group([
        Entity({'name':'pump'}, [-1.5, 0]),
        Entity({'name':'tank'}, [-4.0, 1]),
        ])

def loco_fuel():
    l = []
    l.append(Entity({'name':''}, [0.5, 0.5]))
    l.append(Entity({'name':'requester-chest'}, [2.5, 0.5]))
    l.append(Entity({'name':'inserter'}, [2.5, 1.5]))
    l.append(Entity({'name':''}, [6.5, 5.5]))
    return Group(l)

def wagon_stop(frac_loading):

    def inserter_and_chest_positions():
        for i in range(6):
            yield [i + 0.5, 1.5], [i + 0.5, 0.5]
        for i in range(6):
            yield [i + 0.5, 4.5], [i + 0.5, 5.5]
    
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
        Entity({'name': 'assembling-machine-1'}, [0.5, 0.5]),
        ])
    g1 = Group(tile(g1, 2, 1))
   
    g2 = Group([
        Entity({'name': 'assembling-machine-1'}, [0.5, 6.5]),
        ])
    g2 = Group(tile(g2, 2, 1))
   
    inserters1 = Group([
        Entity({'name': 'inserter'}, [-0.5, 2.5]),
        Entity({'name': 'inserter'}, [0.5, 2.5]),
        Entity({'name': 'inserter'}, [-0.5, 4.5]),
        Entity({'name': 'inserter'}, [0.5, 4.5]),
        ])
    inserters2 = copy.deepcopy(inserters1)
    inserters2.shift([4, 0])

    chests1 = Group([
        Entity({'name': 'requester-chest'}, [-0.5, 3.5]),
        Entity({'name': 'passive-provider-chest'}, [0.5, 3.5]),
        ])
    chests2 = copy.deepcopy(chests1)
    chests1.shift([4, 0])

    g = Group([
        g1,
        g2,
        inserters1,
        inserters2,
        chests1,
        chests2,
        Group(tile(Entity({'name': 'beacon'}, [0.5, 9.5]), 2, 1)),
        Entity({'name': 'substation'}, [2, 4]),
        ])
    
    #g.shift([g.x_min(), g.y_min()])

    return g









