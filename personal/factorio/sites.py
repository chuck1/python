import math
import itertools
import crayons

from products import *

def insert_process(l, product, process):
    for i, p in l:
        if i.product == product:
            yield i, process

            for i1 in process.inputs:
                if i1.q > 0:
                    yield i1, None

        else:
            yield i, p

def insert_process_raw(l, product, process):
    for i, p in l:
        if i.product == product:
            for i1 in process.inputs:
                if i1.q < 0:
                    yield i1, process
                else:
                    yield i1, None

        else:
            yield i, p

def all_inputs3(x, inputs):
    for i, process in inputs:
        yield i, process
    
        #for i1 in process.inputs:
        #    print(i1.product.name)
        
def all_inputs2(x, inputs):
    if False:
        print("all_inputs2")
        for i, process in inputs:
            print(i.product.name, process)
    
    for i, process in inputs:
        if process is None:
            for p in i.product.processes():
                yield from all_inputs2(x, list(insert_process(inputs, i.product, p)))
            break
    
    if all([process is not None for i, process in inputs]):
        #yield inputs
        yield all_inputs3(x, inputs)

        #for i, process in inputs:

def all_raw2(x, inputs):
    if True:
        print("all_raw2")
        for i, process in inputs:
            print(i.product.name, process)
    
    for i, process in inputs:
        if i.q < 0:
            continue

        if process is None:
            for p in i.product.processes():
                yield from all_raw2(x, list(insert_process_raw(inputs, i.product, p)))
            break
    
    if all([(process is not None) or (i.q < 0) for i, process in inputs]):
        yield inputs
        #yield all_raw3(x, inputs)

        #for i, process in inputs:
            

class Process:
    def __init__(self, name, inputs, t):
        self.name = name
        self.inputs = inputs
        self.t = t

    def all_inputs(self, x):
        return all_inputs2(x, [(i, None) for i in self.inputs if i.q > 0])


    def raw(self, x):
        return all_raw2(x, [(i, None) for i in self.inputs])

        """
        inputs = []

        for i in self.inputs:

            inputs.append(i)

            for r in i.product.all_inputs(1.0):
                inputs.append(r.mul(i.q))

        inputs = sorted(inputs, key=lambda i: id(i.product))
        
        for k, g in itertools.groupby(inputs, key=lambda i: i.product):
            s = sum([i.q for i in g]) * x
            #print(k.name, s)

            yield ProductInput(k, s)
        """

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
        "coal",
        [
            ProductInput(coal, -0.525),
            ],
        1,
        )

produce_plastic_bar = Process(
        "plastic bar",
        [
            ProductInput(coal, 1),
            ProductInput(petroleum, 20),
            ProductInput(plastic_bar, -2),
            ],
        1,
        )


rocket_fuel = Product("rocket_fuel", [],
        1 / 30,
        )

solar_panel = Product("solar_panel", [
    ProductInput(copper_plate, 5),
    ProductInput(electronic_circuit, 15),
    ProductInput(steel_plate, 5),
    ],
    1 / 10,
    )

satellite = Product("satellite", [
    ProductInput(accumulator, 100),
    ProductInput(low_density_structure, 100),
    ProductInput(processing_unit, 100),
    ProductInput(radar, 5),
    ProductInput(rocket_fuel, 50),
    ProductInput(solar_panel, 100),
    ],
    1 / 5,
    )

rocket_control_unit = Product("rocket_control_unit", [
    ProductInput(processing_unit, 1),
    ProductInput(speed_module_1, 1),
    ],
    1 / 30,
    )

rocket_part = Product("rocket_part", [
    ProductInput(low_density_structure, 10),
    ProductInput(rocket_control_unit, 10),
    ProductInput(rocket_fuel, 10),
    ],
    1 / 3,
    )

launch_satellite = Product("launch_satellite", [
    ProductInput(rocket_part, 100),
    ProductInput(satellite, 1),
    ],
    )
    
science_pack_1 = Product("science pack 1",
        [
            ProductInput(copper_plate, 1, 0.5),
            ProductInput(iron_gear_wheel, 1, 0.5),
            ],
        1 / 5,
        )

inserter = Product("inserter",
        [
            ProductInput(electronic_circuit, 1, 1),
            ProductInput(iron_gear_wheel, 1, 1),
            ProductInput(iron_plate, 1, 1),
            ],
        1 / 0.5,
        [express_belt],
        )

fast_inserter = Product("fast inserter",
        [
            ProductInput(electronic_circuit, 2, 1),
            ProductInput(inserter, 1, 1),
            ProductInput(iron_plate, 2, 1),
            ],
        1 / 0.5,
        [express_belt],
        )

stack_inserter = Product("stack inserter",
        [
            ProductInput(advanced_circuit, 1, 1),
            ProductInput(electronic_circuit, 15, 1),
            ProductInput(fast_inserter, 1, 1),
            ProductInput(iron_gear_wheel, 15, 1),
            ],
        1 / 0.5,
        [express_belt],
        )

transport_belt = Product("transport_belt",
        [
            ProductInput(iron_gear_wheel, 1, 1),
            ProductInput(iron_plate, 1, 1),
            ],
        1 / 0.5,
        [express_belt],
        )

science_pack_2 = Product("science pack 2",
        [
            ProductInput(inserter, 1, 0.5),
            ProductInput(transport_belt, 1, 0.5),
            ],
        1 / 6,
        )

firearm_magazine = Product(
        "firearm magazine",
        [
            ProductInput(iron_plate, 4, 1),
            ],
        1,
        )

piercing_rounds_magazine = Product(
        "piercing rounds magazine",
        [
            ProductInput(copper_plate, 5, 1),
            ProductInput(firearm_magazine, 1, 1),
            ProductInput(steel_plate, 1, 1),
            ],
        1 / 3,
        )

defender_capsule = Product(
        "defender capsule",
        [
            ProductInput(electronic_circuit, 2, 1),
            ProductInput(iron_gear_wheel, 3, 1),
            ProductInput(piercing_rounds_magazine, 1, 1),
            ],
        1 / 8,
        )

distractor_capsule = Product(
        "distractor capsule",
        [
            ProductInput(advanced_circuit, 3, 1),
            ProductInput(defender_capsule, 4, 1),
            ],
        1 / 15,
        )

destroyer_capsule = Product(
        "destroyer capsule",
        [
            ProductInput(distractor_capsule, 4, 1),
            ProductInput(speed_module_1, 1, 1),
            ],
        1 / 15,
        )

tiers = []

processes = [p for p in globals().values() if isinstance(p, Process)]

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
    for i, p in y:
        if p is not None:
            print("\t{:32} {:32}".format(i.product.name, p.name))
        else:
            print("\t{:32} {:32}".format(i.product.name, ""))



