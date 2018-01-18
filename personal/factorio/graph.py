import os

from sites import *
from graphviz import Digraph
import matplotlib.pyplot as plt

from graph2 import *

factories = [
        mine_iron_ore,
        mine_copper_ore,
        mine_crude_oil,
        mine_coal,
        mine_stone,
        produce_grenade,
        produce_gun_turret,
        produce_accumulator,
        produce_solar_panel,
        produce_piercing_rounds_magazine,
        produce_iron_plate,
        produce_copper_plate,
        produce_steel_plate,
        produce_copper_cable,
        produce_electronic_circuit,
        advanced_oil_processing,
        produce_iron_gear_wheel,
        produce_sulfur,
        produce_sulfuric_acid,
        produce_engine_unit,
        light_oil_to_solid_fuel,
        produce_electric_mining_drill,
        produce_plastic_bar,
        produce_advanced_circuit,
        produce_processing_unit,
        produce_rocket_control_unit,
        produce_low_density_structure,
        produce_rocket_fuel,
        produce_battery,
        produce_speed_module_1,
        produce_electric_engine_unit,
        produce_electric_furnace,
        produce_stone_brick,
        produce_science_pack_1,
        produce_science_pack_2,
        produce_science_pack_3,
        produce_military_science_pack,
        produce_production_science_pack,
        produce_high_tech_science_pack,
        produce_satellite_launch,
        research,
        ]

edges = []

#g.attr('graph', maxiter='99999999')
#g.attr('graph', damping='9999999')
#g.attr('graph', splines='true')

class MyGraph:
    def __init__(self):
        self.nodes = {}
        self.edges = []

    def node(self, name, process, product):
        if name in self.nodes:
            return self.nodes[name]

        n = Node(self, name, process, product, np.random.rand(2))
        self.nodes[name] = n
        return n

    def edge(self, n0, n1, products):
        for e in self.edges:
            if e.src == n0 and e.dst == n1:
                e.add_products(products)
                return e

        e = Edge(n0, n1, products)
        self.edges.append(e)
        return e

    def edge_pairs(self):
        for i in range(len(self.edges)):
            for j in range(i + 1, len(self.edges)):
                yield (self.edges[i], self.edges[j])

    def crossings(self):
        c = 0
        for i in range(len(self.edges)):
            for j in range(i + 1, len(self.edges)):
                if cross(self.edges[i], self.edges[j]) is not None:
                    c += 1
        return c

    def mean_length(self):
        return np.mean([e.length() for e in self.edges])
    
    

    def graphviz(self):
        g = Digraph()

        #g = Digraph(engine='neato')

        #g.attr('graph', overlap='scalexy')
        g.attr('graph', ranksep='2.0')
        g.attr('graph', rankdir='LR')
        g.attr('node', fontname='courier')
        g.attr('edge', fontname='courier')
    
        for n in self.nodes.values():
            scale = 10 / self.mean_length()
            p = n.position * scale
            pos_string = '{},{}!'.format(p[0], p[1])
            #print(pos_string)
            
            if n.product.image is not None:
                g.node(n.name.replace(' ','_'), "", pos=pos_string, image=n.product.image)
            else:
                g.node(n.name.replace(' ','_'), pos=pos_string)

        for e in self.edges:
            l = '\l'.join(list(e.label_lines()) + ['{} wagons/sec'.format(cargo_wagons_per_second(e.products))])

            g.edge(e.src.name.replace(' ','_'), e.dst.name.replace(' ','_'), label=l)

        #print(g.source)

        #g.render('layout.svg')
        g.view()

def connect_to(process, product0, i, i0, c, r):
    if i.q < 0: return
    if i.product == Process.electrical_energy: return

    process1 = i.product.default_process()

    #c = r / process.items_per_cycle(i.product)
    c1 = -r / process1.items_per_cycle(i.product)

    # items per second of i.product
    #r = c * process.items_per_cycle(i.product)

    #c1 = -process1.cycles_per_second(i)

    print('{:24} {:8.1f} items/sec produced by {:24} {:8.1f} cycles/sec'.format(process1.name, c1, i.product.name, r))
    
    if process1 in factories:

        src = process1.name
        dst = process.name
        
        g2.edge(g2.node(src, process1, i.product), g2.node(dst, process, product0), [((process, i.product), r)])

    else:
        print('no factory for {}'.format(i.product.name))
        for i1 in process1.inputs:
            #print('\t{}'.format(i1.product.name))

            #how much i1?
            r1 = c1 * process1.items_per_cycle(i1.product)

            connect_to(process, product0, i1, None, None, r1)
    
def try_move_neighbor_center(n):
    if len(list(n.neighbors())) < 2: return False

    c0 = n.g.crossings()

    nc = n.neighbor_center()
    
    #print(n.position, nc)
    
    p0 = n.position
    n.position = nc

    c1 = n.g.crossings()

    if c1 < c0:
        print('{} < {}'.format(c1, c0))
        return True
    else:
        n.position = p0
        return False

def try_move(n, e, k):
        c0 = n.g.crossings()

        p0 = n.position

        n.position = e.x(k)
        
        c1 = n.g.crossings()

        if c1 < c0:
            print('{} < {}'.format(c1, c0))
            return True
        else:
            n.position = p0
            return False

def remove_edges_to_older_ancestors():
    c = 0

    for n in g2.nodes.values():
        # each edge pointing at n
        edges = [e for e in g2.edges if e.dst == n]
        
        edges_to_remove = []
    
        for e in edges:
            for e1 in edges:
                if e == e1: continue
                if e in edges_to_remove: continue
                
                if e1.src.is_ancestor(e.src):
                    edges_to_remove.append(e)

                    # move products from removed route
                    #print('adding products ', e.products, 'to', e1.src.name, '->', e1.dst.name)
                    e1.add_products(e.products)
                
                    # get path from e.src to n
                    for e2 in e1.src.path(e.src):
                        e2.add_products(e.products)
                        #print('adding products ', e.products, 'to', e2.src.name, '->', e2.dst.name)

                    print('removing edge {} -> {}'.format(e.src.name, e.dst.name))
                    print('\tbecause {} is ancestor of {}'.format(e.src.name, e1.src.name))
    
        #print('removing {} edges'.format(len(edges_to_remove)))
    
        for e in edges_to_remove:
            if e in g2.edges:
                g2.edges.remove(e)
                c += 1
    
    return c > 0

def reroute_through_highest_rank_ancestor():
    c = 0

    print('ancestor rank')
    for n in g2.nodes.values():
        if n.process in exclude: continue

        ancestors = list(n.ancestors())
        
        if len(ancestors) < 2: continue
    
        ancestor_rank = [e.src.rank() for e in ancestors]
        print(n.name, ancestor_rank)
        
        ancestor_rank_max = max(ancestor_rank)
        
        lowest = next(a for a in ancestors if a.src.rank() == ancestor_rank_max)
    
        if len([r for r in ancestor_rank if r == ancestor_rank_max]) > 1: continue
        
        ancestors_remove = [a for a in ancestors if a.src.rank() < ancestor_rank_max]
        
        for a in ancestors_remove:
            g2.edges.remove(a)
            g2.edge(a.src, lowest.src, list(a.products))
            c += 1
    
            print('remove edge {} -> {}'.format(a.src.name, a.dst.name))
            print('add edge {} -> {}'.format(a.src.name, lowest.src.name))
        
    return c > 0

###################################################################33
###################################################################33
###################################################################33

g2 = MyGraph()


inputs = research.all_inputs_default(1000)

for i0 in inputs:
    process = i0.product.default_process()
    
    if process not in factories:
        continue
    
    #print(process.name, 'c =', process.cycles_per_second(i0))
    
    c = -process.cycles_per_second(i0)


    for i in process.inputs:
        r = c * process.items_per_cycle(i.product)
        connect_to(process, i0.product, i, i0, c, r)

#for i in research.inputs:
#    connect_to(research, i, None, None, 1000)




print('edges', len(g2.edges))

print(g2.crossings())

repeat = False
while repeat:
    repeat = False
    for n in g2.nodes.values():
        try_move_neighbor_center(n)


print('try move')

repeat = False
while repeat:
    repeat = False
    for e0, e1 in g2.edge_pairs():
        t = cross(e0, e1)
        if t is not None:
    
            k0, k1 = t
            
            if(try_move(e0.src, e0, (k0 + 1) / 2)): repeat = True
            if(try_move(e0.dst, e0, (k0 + 0) / 2)): repeat = True
            if(try_move(e1.src, e0, (k1 + 1) / 2)): repeat = True
            if(try_move(e1.dst, e0, (k1 + 0) / 2)): repeat = True
        
x = [np.linalg.norm(e.v()) for e in g2.edges]
x0 = np.mean(x)

# shorten long edges where one node has only one neighbor

for n in g2.nodes.values():
    neighbors = list(n.neighbors())
    if len(neighbors) == 1:
        for e, n1 in neighbors:
            d = e.length()
            if d > x0:
                if n == e.src:
                    n.position = e.x(1 - x0 / d)
                else:
                    n.position = e.x(x0 / d)

if False:
    n, bins, patches = plt.hist(x, 50, normed=1, facecolor='green', alpha=0.75)
    plt.show()

exclude = [
        research,
        ]

repeat = True
while repeat:
    repeat = False
    if remove_edges_to_older_ancestors(): repeat = True
    #if reroute_through_highest_rank_ancestor(): repeat = True

g2.graphviz()

print()

#print(g.source)
#g.render('items.svg')






