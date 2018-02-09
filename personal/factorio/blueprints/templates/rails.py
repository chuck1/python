import enum

from fact.util import *

from blueprints.blueprint import *
import blueprints.templates
from blueprints.entity import *
from blueprints.group import *

class TurnDirection(enum.Enum):
    EN = 0
    NW = 1
    ES = 1

def turn_90(rail, direction, d=0, s=[0, 0]):
    # rail_s - starting straight rail
    # d - number of extra diagonal rails
    # s - offset from rail_s

    # return tuple of 
    #  group containing curved rails and diagonal rails
    #  position to place straight rail at opposite end

    # TODO assert proper direction of rail_e

    l = []

    s = np.array(s)

    # diagonal rails
    for i in range(d + 1):
        if direction == TurnDirection.NW:
            x = -4 - 2 * i
            y = -8 - 2 * i
        elif direction == TurnDirection.EN:
            x = -8 - 2 * i
            y = -4 - 2 * i

        e = Entity({'name':'straight-rail'}, [x, y])
        e.shift(rail.position + s)
        
        l.append(e)
    
    if direction == TurnDirection.NW:
        s = s + [-12 + 2, -12]
    elif direction == TurnDirection.EN:
        s = s + [-12, -12 + 2]

    e = Entity({'name':''}, rail.position + s)
    l.append(e)

    g = Group(l)

    g.connection_west = e

    return g

def S_EW(rail_e, d, s=[0, 0]):
    # s - offset from rail_e
    # return tuple of
    #  Group containing curved and diagonal rails
    #  position to place straight rail at opposite end
    
    l = []
    
    # diagonal rails
    for i in range(d):
        x = -8 - 2 * i
        y = -4 - 2 * i
        e = Entity({'name':'straight-rail'}, [x, y])
        e.shift(rail_e.position + s)
        l.append(e)
    
    e = Entity({'name':''}, rail_e.position + s + [-14 - 2*d + 2, -6 - 2*d])
    l.append(e)

    g = Group(l)

    g.connection_west = e
    
    return g

def S_WE(rail_w, d, s=[0, 0]):
    # s - offset from rail_e
    # return tuple of
    #  Group containing curved and diagonal rails
    #  position to place straight rail at opposite end
    
    l = []
    
    # diagonal rails
    for i in range(d):
        x = 8 + 2 * i
        y = 4 + 2 * i
        e = Entity({'name':'straight-rail'}, [x, y])
        e.shift(rail_w.position + s)
        l.append(e)
    
    e = Entity({'name':''}, rail_w.position + s + [14 + 2*d - 2, 6 + 2*d])
    l.append(e)

    g = Group(l)

    g.connection_east = e
    
    return g

def waiting_area_EW(rail_e, d, n, s=[0, 0]):
    # d - number of diagonal rails
    # n - number of parallel lines

    assert(n > 0)

    s = np.array(s)

    l = []

    for i in range(n):
        e = S_EW(rail_e, d, s + [-4 * i, 0])
        l.append(e)

    e = Entity({'name':''}, e.connection_west.position)
    l.append(e)

    g = Group(l)
    
    g.connection_west = e

    return g

def waiting_area_WE(rail_w, d, n, s=[0, 0]):
    # d - number of diagonal rails
    # n - number of parallel lines

    assert(n > 0)

    s = np.array(s)

    l = []

    for i in range(n):
        e = S_WE(rail_w, d, s + [4 * i, 0])
        l.append(e)

    e = Entity({'name':''}, e.connection_east.position)
    l.append(e)

    g = Group(l)
    
    g.connection_east = e

    return g

def bus_turn(rails_start, rails_end, direction):

    if direction == TurnDirection.EN:
        D = 0
    elif direction == TurnDirection.NW:
        D = 1
    elif direction == TurnDirection.ES:
        D = 0

    c0 = min(r.position[D] for r in rails_start)

    print('bus turn')
    print('rails start', len(rails_start))
    for r in rails_start:
        print('\t{}'.format(r.position))
    print('rails end  ', len(rails_end))
    for r in rails_end:
        print('\t{}'.format(r.position))
    
    i_iter = iter(spread(len(rails_end), len(rails_start)))
    
    l = []

    p_n = [None]*len(rails_end)
    p_s = [None]*len(rails_end)

    turns = [[] for i in range(len(rails_end))]

    for r in rails_start:
        i = next(i_iter)


        if direction == TurnDirection.EN:
            #c1 = r.position[D]
            c1 = r.position[D]
            c0 = rails_end[i].position[D] + 12
            print('rails', c0, c1)

            rails = list(blueprints.templates.rails_x(c0, c1, r.position[1-D]))
        elif direction == TurnDirection.NW:
            #c1 = r.position[D]
            
            c1 = r.position[D]
            c0 = rails_end[i].position[D] + 12
            print('rails', c0, c1)
            rails = list(blueprints.templates.rails_y(r.position[1-D], c0, c1))
        elif direction == TurnDirection.ES:
            #c1 = r.position[D]
            c1 = r.position[D]
            c0 = rails_end[i].position[D] - 12
            print('rails', c0, c1)

            rails = list(blueprints.templates.rails_x(c0, c1, r.position[1-D]))

         
        g2 = blueprints.group.Group(rails)

        l.append(g2)

        # turn to bus 2 west
        
        if rails:
            if direction == TurnDirection.EN:
                e3 = rails[0]
            elif direction == TurnDirection.NW:
                e3 = rails[0]        
            elif direction == TurnDirection.ES:
                e3 = rails[-1]
        else:
            e3 = Entity({'name':''}, r.position)

        print('turn from', e3.position)

        turn = blueprints.templates.rails.turn_90(e3, direction)

        turns[i].append(turn)
        
        l.append(turn)

    for i, r in zip(range(len(rails_end)), rails_end):
        turns1 = sorted(turns[i], key=lambda turn: turn.connection_west.position[1-D])

        p0 = turns1[0].connection_west.position
        p1 = turns1[-1].connection_west.position
        
        if direction == TurnDirection.EN:
            rails = list(blueprints.templates.rails_y(r.position[0], r.position[1], p1[1]))
        elif direction == TurnDirection.NW:
            rails = list(blueprints.templates.rails_x(r.position[0], p1[0], r.position[1]))
        elif direction == TurnDirection.ES:
            rails = list(blueprints.templates.rails_y(r.position[0], p0[1], r.position[1]))
    
        l.append(blueprints.group.Group(rails))

    return Group(l)






