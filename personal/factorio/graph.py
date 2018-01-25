import os

from graphviz import Digraph
import matplotlib.pyplot as plt

#from sites import *
from graph2 import *
from products import *
from fact.processes import *
import modules

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

    def node(self, name, process, c, product):
        if name in self.nodes:
            return self.nodes[name]

        n = Node(self, name, process, c, product, np.random.rand(2))
        self.nodes[name] = n
        return n

    def edge(self, n0, n1, products):
        for e in self.edges:
            if e.src == n0 and e.dst == n1:
                return e

        e = Edge(n0, n1)
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
    
    def graphviz(self, label_edges=False):
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
            if label_edges:
                #l = '\l'.join(list(e.label_lines()) + ['{} wagons/sec'.format(cargo_wagons_per_second(e.products))])
                l = '\l'.join(list(e.label_lines()))
                g.edge(e.src.name.replace(' ','_'), e.dst.name.replace(' ','_'), label=l)
            else:
                g.edge(e.src.name.replace(' ','_'), e.dst.name.replace(' ','_'))

        #print(g.source)

        #g.render('layout.svg')
        g.view()

def connect_to(process, c, product0, i, rate):
    if i.q < 0: return
    if i.product == Process.electrical_energy: return

    process1 = i.product.default_process()

    c1 = -rate / process1.items_per_cycle(i.product)

    print('{:24} {:8.1f} items/sec produced by {:24} {:8.1f} cycles/sec'.format(process1.name, c1, i.product.name, rate))
    
    if process1 in factories:

        src = process1.name
        dst = process.name
        
        n0 = g2.node(src, process1, c1, i.product)
        n1 = g2.node(dst, process, c, product0)

        e = g2.edge(n0, n1, [((process, i.product), rate)])
        
        r = Route(n1, [])
        r.leg(e, [RouteLegProduct(i.product, rate)])
        Routes.add_route(r)

    else:
        print('no factory for {}'.format(i.product.name))
        for i1 in process1.inputs:
            #print('\t{}'.format(i1.product.name))
            
            #how much i1?
            r1 = c1 * process1.items_per_cycle(i1.product)
            
            connect_to(process, c, product0, i1, r1)
    

def remove_edges_to_older_ancestors():
    """
    A -> B -> C
    A -> C

    remove A -> C

    find route for B -> C
    """
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

                    # route associated with e
                    route_AC = list(Routes.find_route(n.process, e))[0]
                    leg_AC = route_AC.find_leg(e)
                    Routes.routes.remove(route_AC)

                    # route associated with e1
                    r = list(Routes.find_route(n.process, e1))[0]
                    r.show()
                    r.leg(e1, leg_AC.products)
                    
                    # get path from e.src to n
                    for e2 in e1.src.path(e.src):
                        r.leg(e2, leg_AC.products)

                        #print('adding products ', e.products, 'to', e2.src.name, '->', e2.dst.name)

                    r.show()

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

Constants.electric_mining_drill = electric_mining_drill
Constants.mine_uranium_ore = mine_uranium_ore
Constants.wagons_per_train = 10
Constants.inserters_per_wagon = 12

modules.apply_modules()

g2 = MyGraph()

#inputs = produce_rocket_control_unit.all_inputs_default(1000)
#inputs = produce_production_science_pack.all_inputs_default(10000/60/2)

#product = production_science_pack
#p = product.default_process()

#inputs = list(p.all_inputs_default(items_per_sec / p.items_per_cycle(product), ignore_power=True))


# INPUT
items_per_sec = 1000



c = -items_per_sec / research.items_per_cycle(space_science_pack)
inputs = list(research.all_inputs_default(c))

for i in inputs:
    print('{:22} {:8.2f}'.format(i.product.name, i.q))


for i0 in inputs:
    process = i0.product.default_process()
    
    if process not in factories:
        continue
    
    c = -process.cycles_per_second(i0)

    print('\t', process.name, 'c = {} i0.q = {}'.format(c, i0.q))

    for i in process.inputs:
        r = c * process.items_per_cycle(i.product)
        connect_to(process, c, i0.product, i, r)

#for i in research.inputs:
#    connect_to(research, i, None, None, 1000)


    

exclude = [
        research,
        ]

repeat = True
while repeat:
    repeat = False
    if remove_edges_to_older_ancestors(): repeat = True
    #if reroute_through_highest_rank_ancestor(): repeat = True



print()

#print(g.source)
#g.render('items.svg')


#g2.nodes[processing_unit.name].inputs()

for r in Routes.routes:
    r.show()

for e in g2.edges:
    e.balance_routes()
    #e.products()

#g2.graphviz()

print()

print('factories')
for n in sorted(g2.nodes.values(), key=lambda n: n.process.name):
    n.factory_layout()
#g2.nodes[advanced_circuit.name].factory_layout()




