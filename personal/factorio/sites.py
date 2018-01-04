import math
import itertools
import crayons

from products import *

mine_water = Process(
        "mine_water",
        [
            ProductInput(water, -1200),
            ],
        1,
        )

mine_crude_oil = Process(
        "mine_crude_oil",
        [
            ProductInput(crude_oil, -50),
            ],
        1,
        )

advanced_oil_processing = Process(
        "advanced_oil_processing",
        [
            ProductInput(crude_oil, 100),
            ProductInput(water, 50),
            ProductInput(heavy_oil, -10),
            ProductInput(light_oil, -45),
            ProductInput(petroleum, -55),
            ],
        5,
        )

basic_oil_processing = Process(
        "basic oil processing",
        [
            ProductInput(crude_oil, 100),
            ProductInput(heavy_oil, -30),
            ProductInput(light_oil, -30),
            ProductInput(petroleum, -40),
            ],
        5,
        )

mine_coal = Process(
        "mine coal",
        [
            ProductInput(coal, -0.525),
            ],
        1,
        )

produce_plastic_bar = Process(
        "produce plastic bar",
        [
            ProductInput(coal, 1),
            ProductInput(petroleum, 20),
            ProductInput(plastic_bar, -2),
            ],
        1,
        )

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

    for product_input in product.inputs:
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


new_base_supplies = Product(
        "new base supplier",
        [
            ProductInput(stack_inserter, 48),
            ],
        )

production = Product("production", [
    ProductInput(speed_module_3, 1 / 3 / 60),
    ProductInput(speed_module_3, 1 / 3 / 60),
    ProductInput(speed_module_3, 1 / 3 / 60),
    ProductInput(launch_satellite, 1 / 10 / 60),
    ProductInput(destroyer_capsule, 1 / 1 / 60),
    ProductInput(piercing_rounds_magazine, 1 / 1 / 60),
    ProductInput(science_pack_1, 10 / 60),
    ProductInput(science_pack_2, 10 / 60),
    ProductInput(new_base_supplies, 1 / 30 / 60),
    ])



tiers_insert(production)

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
    
    science_pack_1.production_building_row_length()
    science_pack_2.production_building_row_length()
    
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



