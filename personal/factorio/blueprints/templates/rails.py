import enum

from fact.util import *

from blueprints.blueprint import *
import blueprints.templates

class TurnDirection(enum.Enum):
    EN = 0
    NW = 1

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

def bus_turn(rails_start, rails_end, direction):
    
    if direction == TurnDirection.EN:
        c0 = min(r.position[0] for r in rails_start)
    elif direction == TurnDirection.NW:
        c0 = min(r.position[1] for r in rails_start)

    print('bus turn')
    print('rails end  ', len(rails_end))
    print('rails start', len(rails_start))

    i_iter = iter(spread(len(rails_end), len(rails_start)))

    l = []

    p_n = [None]*len(rails_end)
    p_s = [None]*len(rails_end)

    turns = [[] for i in range(len(rails_end))]

    for r in rails_start:
        i = next(i_iter)


        if direction == TurnDirection.EN:
            c1 = r.position[0]
            rails = list(blueprints.templates.rails_x(c0, c1, r.position[1]))
        elif direction == TurnDirection.NW:
            c1 = r.position[1]
            rails = list(blueprints.templates.rails_y(r.position[0], c0, c1))

         
        g2 = blueprints.blueprint.Group(rails)

        l.append(g2)

        # turn to bus 2 west
        
        if rails:
            e3 = rails[0]
        else:
            e3 = Entity({'name':''}, r.position)

        turn = blueprints.templates.rails.turn_90(e3, direction)

        turns[i].append(turn)
        
        l.append(turn)

    for i in range(len(rails_end)):
        if direction == TurnDirection.EN:
            turns1 = sorted(turns[i], key=lambda turn: turn.connection_west.position[0])
        elif direction == TurnDirection.NW:
            turns1 = sorted(turns[i], key=lambda turn: turn.connection_west.position[1])

        p0 = turns1[0].connection_west.position
        p1 = turns1[-1].connection_west.position
        
        if direction == TurnDirection.EN:
            rails = list(blueprints.templates.rails_y(p0[0], p0[1], p1[1]))
        elif direction == TurnDirection.NW:
            rails = list(blueprints.templates.rails_x(p0[0], p1[0], p0[1]))
    
        l.append(blueprints.blueprint.Group(rails))

    return Group(l)

def bus_turn_NW(rails_start, rails_end):

    y0 = min(r.position[1] for r in rails_start)

    print('bus turn NW')
    print('rails end  ', len(rails_end))
    print('rails start', len(rails_start))

    i_iter = iter(spread(len(rails_end), len(rails_start)))

    l = []

    p_w = [None]*len(rails_end)
    p_e = [None]*len(rails_end)
    
    turns = [[] for i in range(len(rails_end))]

    for r in rails_start:
        i = next(i_iter)

        y1 = r.position[1]
        rails = list(blueprints.templates.rails_y(r.position[0], y0, y1))
         
        g2 = blueprints.blueprint.Group(rails)

        l.append(g2)

        # turn to bus 2 west
        
        if rails:
            e3 = rails[0]
        else:
            e3 = Entity({'name':''}, r.position)

        turn = blueprints.templates.rails.turn_90_NW(e3)
        
        turns[i].append(turn)

        if p_e[i] is None: p_e[i] = turn.connection_west.position
        p_w[i] = turn.connection_west.position

        l.append(turn)

    for i in range(len(rails_end)):
        

        turns1 = sorted(turns[i], key=lambda turn: turn.connection_west.position[0])

        p0 = turns1[0].connection_west.position
        p1 = turns1[-1].connection_west.position

        rails = list(blueprints.templates.rails_x(p0[0], p1[0], p0[1]))
        
        print('second bus rails', len(rails))

        l.append(blueprints.blueprint.Group(rails))
        
    return Group(l)









