import enum

from fact.util import *

from blueprints.blueprint import *
import blueprints.templates
from blueprints.entity import *
from blueprints.group import *

class TurnDirection(enum.Enum):
    WN = 0
    NW = 1
    ES = 2
    SE = 3
    EW = 4
    WE = 5

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
        elif direction == TurnDirection.WN:
            x = -8 - 2 * i
            y = -4 - 2 * i
        elif direction == TurnDirection.SE:
            x = 4 + 2 * i
            y = 8 + 2 * i
        elif direction == TurnDirection.ES:
            x = 8 + 2 * i
            y = 4 + 2 * i
        
        e = Entity({'name':'straight-rail'}, [x, y])
        e.shift(rail.position + s)
        
        l.append(e)
    
    if direction == TurnDirection.NW:
        s = s + [-12 + 2, -12]
    elif direction == TurnDirection.WN:
        s = s + [-12, -12 + 2]
    if direction == TurnDirection.SE:
        s = s + [12 - 2, 12]
    elif direction == TurnDirection.ES:
        s = s + [12, 12 - 2]

    e = Entity({'name':''}, rail.position + s)
    l.append(e)

    g = Group(l)

    g.connection = e

    return g

def S_turn(rail, d, direction, s=[0, 0]):
    # s - offset from rail_e
    # return tuple of
    #  Group containing curved and diagonal rails
    #  position to place straight rail at opposite end
    s = np.array(s)
    l = []
    
    # diagonal rails
    for i in range(d):
        if direction == TurnDirection.EW:
            x = -8 - 2 * i
            y = -4 - 2 * i
        if direction == TurnDirection.WE:
            x = 8 + 2 * i
            y = 4 + 2 * i

        e = Entity({'name':'straight-rail'}, [x, y])
        e.shift(rail.position + s)
        l.append(e)
    
    if direction == TurnDirection.EW:
        o = [-(14 + 2*d - 2), -(6 + 2*d)]
    elif direction == TurnDirection.WE:
        o = [14 + 2*d - 2, 6 + 2*d]

    e = Entity({'name':''}, rail.position + s + o)
    l.append(e)

    g = Group(l)

    g.connection = e
    
    return g

def waiting_area_EW(rail_e, d, n, s=[0, 0]):
    # d - number of diagonal rails
    # n - number of parallel lines

    assert(n > 0)

    s = np.array(s)

    l = []

    for i in range(n):
        e = S_turn(rail_e, d, TurnDirection.EW, s + [-4 * i, 0])
        l.append(e)

    e = Entity({'name':''}, e.connection.position)
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
        e = S_turn(rail_w, d, TurnDirection.WE, s + [4 * i, 0])
        l.append(e)

    e = Entity({'name':''}, e.connection.position)
    l.append(e)

    g = Group(l)
    
    g.connection_east = e

    return g

def bus_turn(rails_start, rails_end, direction):

    if direction == TurnDirection.WN:
        D = 0
    elif direction == TurnDirection.NW:
        D = 1
    elif direction == TurnDirection.ES:
        D = 0
    elif direction == TurnDirection.SE:
        D = 1

    c0 = min(p[D] for p in rails_start)

    print('bus turn', direction.name)
    print('rails start', len(rails_start))
    for p in rails_start:
        print('\t{}'.format(p))
    print('rails end  ', len(rails_end))
    for p in rails_end:
        print('\t{}'.format(p))
    
    i_iter = iter(spread(len(rails_end), len(rails_start)))
    
    l = []

    p_n = [None]*len(rails_end)
    p_s = [None]*len(rails_end)

    turns = [[] for i in range(len(rails_end))]

    for r in rails_start:
        i = next(i_iter)

        p1 = np.array(rails_end[i])
        p1[1-D] = r[1-D]
        
        if direction == TurnDirection.WN:
            p1[D] += 12
        elif direction == TurnDirection.NW:
            p1[D] += 12
        elif direction == TurnDirection.ES:
            p1[D] -= 12
        elif direction == TurnDirection.SE:
            p1[D] -= 12
        
        rails = list(blueprints.templates.rails_point_to_point(r, p1))
    
        print('first bus rails {} to {}'.format(str(r), str(p1)))

        """
        if direction == TurnDirection.WN:
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
        """
         
        g2 = blueprints.group.Group(rails)

        l.append(g2)

        # turn to bus 2 west
        
        if rails:
            if direction == TurnDirection.WN:
                e3 = rails[0]
            elif direction == TurnDirection.NW:
                e3 = rails[0]        
            elif direction == TurnDirection.ES:
                e3 = rails[-1]
            elif direction == TurnDirection.SE:
                e3 = rails[-1]
        else:
            e3 = Entity({'name':''}, r)

        print('turn from', e3.position)

        turn = blueprints.templates.rails.turn_90(e3, direction)

        turns[i].append(turn)
        
        l.append(turn)

    for i, r in zip(range(len(rails_end)), rails_end):
        turns1 = sorted(turns[i], key=lambda turn: turn.connection.position[1-D])

        p0 = turns1[0].connection.position
        p1 = turns1[-1].connection.position
        
        print('second bus rails {} to {}'.format(str(p0), str(p1)))

        rails = blueprints.templates.rails_point_to_point(p0, p1)

        l.append(blueprints.group.Group(rails))

    return Group(l)






