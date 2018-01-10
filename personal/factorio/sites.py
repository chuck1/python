import math
import itertools
import crayons
import numpy as np
import scipy.optimize

from products import *
from processes import *



tiers = []

Process.processes = [p for p in globals().values() if isinstance(p, Process)]

def tier_index(product):
    for i in range(len(tiers)):
        if product in tiers[i]:
            return i
    return None

def tiers_insert(product):
   
    #i = tier_index(product)
    #if i is not None: return i

    #print("insert" , product.name)
    
    i_max = -1

    for product_input in product.default_process().inputs:
        if product_input.q < 0:
            continue

        if product_input.product == electrical_energy: continue

        p = product_input.product
        i = tier_index(p)
        #print("index of", p.name, "is", i)

        if i is None:
            i = tiers_insert(product_input.product)

        if i > i_max: i_max = i

    i_max += 1

    while len(tiers) <= i_max:
        tiers.append([])
    
    tiers[i_max].append(product)
    
    assert tier_index(product) == i_max

    product.tier = i_max

    return i_max


for t in tiers:
    print([p.name for p in t])

def print_raw(p, x):
    print(p.name)
    for r in p.raw(x):
        print("\t{:24} {:8.2f}".format(r.product.name, r.q))

def print_all(p, x):
    print(p.name)
    inputs = list(p.all_inputs(x))
    inputs = sorted(inputs, key=lambda x: x.product.tier)
    for r in inputs:

        
        if r.product.rate is not None:
            print("\t{:24} {:12.4f} {:8.2f}".format(r.product.name, r.q, r.q / r.product.rate))
        else:
            print("\t{:24} {:12.4f}".format(r.product.name, r.q))

        #if r.product.rate is not None:
        #    b = r.q / r.product.rate
        #    print("\t\tproduction buildings: {:8.2f}".format(b))
        
        #if r.product.transport:
        #    print("\t\ttransport")
        #    for t in r.product.transport:
        #        x = r.q / t.rate
        #        print("\t\t\t{:24} {:8.2f}".format(t.name, x))



tiers_insert(satellite)
tiers_insert(stack_inserter)
tiers_insert(science_pack_1)
tiers_insert(science_pack_2)

#print_all(electronic_circuit, 1)
#print_all(production, 1)

#print_all2(petroleum, 1)



def train_rate():

    # train movement time. 
    # the time from one train entering a station to the next train entering the station, minus the amount of time
    # spent loading/unloading
    # in other words, the time between trains if you had a "wait for 0 seconds" condition on the stop
    # depends on how many train you have but if you saturate a track with trains, it is limited
    # by the time it takes the last train to accelerate and clear the signal and the waiting train to accelerate from rest,
    # then decelerate to the stop
    t = 60
    
    # amount of stuff on the train
    l = 2000 * 4
    
    # rate at which we can load/unload the train
    r = 12.41 * 12 * 4

    t_load = l / r

    R = l / (t + t_load)

    print("time to load/unload: ", t_load)
    print("train switching time:", t)
    print("total time:          ", t + t_load)
    print("overall rate:        ", l / (t + t_load))
    print("express belt equiv:  ", R / 40)
    

#train_rate()

if False:
    iron_plate.production_building_row_length()
    copper_plate.production_building_row_length()
    copper_cable.production_building_row_length()
    
    #iron_plate.production_building_row_length()
    advanced_circuit.production_building_row_length()
    #processing_unit.production_building_row_length()
    
    inserter.production_building_row_length()

    processing_unit.production_building_row_length()
    
    science_pack_1.production_building_row_length()
    science_pack_2.production_building_row_length()
    science_pack_3.production_building_row_length()

if False:
    #x = advanced_oil_processing.all_inputs(1)
    x = produce_plastic_bar.raw(1)
    print()
    for y in x:
        print("option")
        for i, p in y.final:
            if p is not None:
                print("\t{:32} {:8.2f} {:32}".format(i.product.name, i.q, p.name))
            else:
                print("\t{:32} {:8.2f} {:32}".format(i.product.name, i.q, ""))
    
        print("group")
        for i in y.group():
            print("\t{:32} {:8.2f}".format(i.product.name, i.q))


def fun(X, process, product, rate):

    ing = list(process.ingredients_grouped(X))
    
    i = next(i for i in ing if i.product == product)
    
    #print(i.product.name, i.q)
    #print(i.product.name, rate)

    c = rate / i.q
    
    #print('c',c)
    
    e = next(i for i in ing if i.product == electrical_energy)
    #print(e.product.name, e.q)
    #print(e.product.name, e.q * c)
    
    #ing = [i.mul(c) for i in ing]
    
    return e.q * c

def optimizer(process, product, rate, X):
    
    #X = np.ones(process.process_count())

    return scipy.optimize.minimize(fun, X, (process, product, rate))

if False:
    v = VirtualProcess(petroleum, [basic_oil_processing, advanced_oil_processing])

    ret = optimizer(v, petroleum, -1, [1, 100])
    print(ret)

    #for i in v.ingredients_grouped([1,1]):
    #    print("\t{:32} {:8.2f}".format(i.product.name, i.q))

    if True:
        print(fun([1,1], v, petroleum, -1))
        print(fun([1,2], v, petroleum, -1))
        print(fun([1,3], v, petroleum, -1))
        print(fun([1,10], v, petroleum, -1))
        print(fun([1,100], v, petroleum, -1))

def process_track_list(l):

    l = sorted(l, key=lambda t: id(t[0]))

    for k, g in itertools.groupby(l, key=lambda t: t[0]):
        g = list(g)
        
        #if any(i.q < 0 for p, i in g):
        #    raise RuntimeError()

        s = sum([i.q for p, i in g])
        yield k, s

def process_track(track):
    return dict((p, process_track_list(l)) for p, l in track.items())

def all_inputs_default(process, product, rate):
    track = {}

    #c = 1 / process.t
    
    c = rate / process.items_per_cycle(product)

    print("inputs")
    inputs = list(process.all_inputs_default(c, track))
    for i in inputs:
        if i.product.process_default.t is None:
            print("\t{:32} {:12.2f}".format(i.product.name, i.q))
        else:
            b = -i.product.process_default.buildings(i.product, i.q)
            print("\t{:32} {:12.2f} {:12.2f}".format(i.product.name, i.q, b))

    return dict((i.product, i) for i in inputs)

    track = process_track(track)

    print()
    for p, l in track.items():
        print(p.name)
        for process1, r in l:
            print("\t{:32} {:12.2f}".format(process1.name, r))

    return

    track = {}

    print()
    for i in process.excess_default(1 / process.t, track):
        print("\t{:32} {:12.2f}".format(i.product.name, i.q))


if False:
    all_inputs_default(production) 
    #all_inputs_default(produce_science_pack_3)
    #all_inputs_default(produce_satellite) 

def graph():
    print()

    from graphviz import Digraph
    
    g = Digraph()

    for process in Process.processes:
        if process.has_site:
            name = process.name.replace(' ', '_')
            g.node(name, process.name)

            for i in process.inputs:
                if i.q < 0:
                    continue
                
                process1 = i.product.default_process()

                if process1.has_site:
                    g.edge(process1.name.replace(' ', '_'), name)
                else:
                    print('need site for {}'.format(i.product.name))
            

    print()
    print(g.source)
    g.view()
    g.render('items.svg')

#graph()

#mine_iron_ore.print_()

rockets_per_minute = 10

rate = 100 * rockets_per_minute / 60

mine_iron_ore.print_()
#produce_rocket_part.print_()
all_inputs_default(produce_rocket_part, rocket_part, rate)

##########

mine_iron_ore.modules = [ProductivityModule3(3), SpeedModule3(3)]
# miners on circumference
#mine_iron_ore.modules.append(SpeedModule3(3 * 0.58))

mine_copper_ore.modules = [ProductivityModule3(3), SpeedModule3(3)]

produce_iron_plate.modules = [ProductivityModule3()]*2 + [SpeedModule3(3)]
produce_copper_plate.modules = [ProductivityModule3()]*2
produce_steel_plate.modules = [ProductivityModule3()]*2

produce_copper_cable.modules = [ProductivityModule3()]*4
produce_electronic_circuit.modules = [ProductivityModule3()]*4
produce_advanced_circuit.modules = [ProductivityModule3()]*4
produce_processing_unit.modules = [ProductivityModule3()]*4
produce_speed_module_1.modules = [ProductivityModule3()]*4
produce_low_density_structure.modules = [ProductivityModule3()]*4
produce_rocket_control_unit.modules = [ProductivityModule3()]*4

produce_rocket_part.modules = [ProductivityModule3()]*4

mine_iron_ore.print_()
#produce_rocket_part.print_()
inputs = all_inputs_default(produce_rocket_part, rocket_part, rate)

beacons = 3

def mine_calcs(deposit_size, i):

    #deposit_size = 20000000
    ore_per_tile = 45000

    tiles_per_deposit = deposit_size / ore_per_tile
    
    miners_per_tile = (9 - beacons) / (9*12)
    
    miners_per_deposit = tiles_per_deposit * miners_per_tile
    
    #i = inputs[iron_ore]
    
   
    area = tiles_per_deposit / 12
    
    radius = math.sqrt(area / math.pi)
    
    circ = 2 * radius * math.pi
    
    #print('radius       ', radius)
    #print('circumference', circ)
    
    circ_miners = circ * ((9 - beacons) / 9)
    
    #print('miners on circumference', circ_miners)
    
    #print('fraction on circumference', circ_miners / miners_per_deposit)
    
    usable_ore = deposit_size * (9 * 12 - 3 * beacons) / (9 * 12)
    
    period_s = usable_ore / i.q
    
    print('tiles_per_deposit ', tiles_per_deposit)
    print('miners_per_deposit', miners_per_deposit)
    print('miners            ', -i.buildings())
    print('mines             ', -i.buildings() / miners_per_deposit)
    print('seconds           ', period_s)
    print('minutes           ', period_s / 60)

    return period_s

period_iron = mine_calcs(20E6, inputs[iron_ore])
period_copper = mine_calcs(20E6, inputs[copper_ore])

period = 1 / (1 / period_iron + 1 / period_copper)

print()
print('period {:8.2f} minutes'.format(period / 60))



