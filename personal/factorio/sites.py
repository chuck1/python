import math
import itertools

class Transport:
    def __init__(self, name, rate):
        self.name = name
        self.rate = rate

express_belt = Transport("express belt", 40)

class ProductInput:
    def __init__(self, product, q=None):
        self.product = product
        # qantity
        self.q = q

    def mul(self, x):
        return ProductInput(self.product, self.q * x)

class Product:
    def __init__(self, name, inputs, rate=None, transport=[]):
        self.name = name
        self.inputs = inputs
        # the rate at which one production building will produce this
        self.rate = rate
        # methods that can transport this
        self.transport = transport
    
    def production_building_row_length(self):

        inputs = list(self.inputs)

        inputs = [ProductInput(i.product, i.q * self.rate) for i in inputs if express_belt in i.product.transport]

        for i in inputs:
            print(i.product.name, i.q)
        
        x = [10 / i.q for i in inputs]
        
        # if number of inputs is odd
        if len(self.inputs) % 2 == 1:
            x_min = min(x)
            i = x.index(x_min)
            del x[i]
            x.append(x_min * 2)

        # buildings per row based on output on one belt side
        x.append(20 / self.rate)

        print(x)

        y = min(x)

        y = math.floor(y)

        print(y)

    def raw(self, x):

        inputs = list(self.inputs)

        while True:
            intermediates = [i for i in inputs if i.product.inputs]
            if not intermediates: break

            i = intermediates[0]

            inputs.remove(i)

            for r in i.product.raw(1.0):
                inputs.append(r.mul(i.q))

        inputs = sorted(inputs, key=lambda i: id(i.product))

        for k, g in itertools.groupby(inputs, key=lambda i: i.product):
            s = sum([i.q for i in g]) * x
            #print(k.name, s)

            yield ProductInput(k, s)

    def all_inputs(self, x):

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

coal = Product("coal", [])

petroleum = Product("petroleum", [],
        55 / 5)

iron_ore = Product("iron ore", [],
        0.525,
        [express_belt],
        )

copper_ore = Product("copper ore", [])

plastic_bar = Product("plastic bar",
        [
            ProductInput(coal, 1 / 2),
            ProductInput(petroleum, 20 / 2),
            ],
        2 / 1,
        [express_belt],
        )

sulfur = Product("sulfur", [])

copper_plate = Product("copper plate",
    [
        ProductInput(copper_ore, 1.0)
    ],
    0.57,
    [
        express_belt,
    ])

copper_cable = Product("copper cable", [
    ProductInput(copper_plate, 0.5)
    ],
    2 / 0.5,
    [express_belt],
    )

iron_plate = Product("iron plate",
    [
        ProductInput(iron_ore, 1.0),
    ],
    0.57,
    [
        express_belt,
    ])

steel_plate = Product("steel plate", [
    ProductInput(iron_plate, 5.0)
    ])

sulfuric_acid = Product("sulfuric acid", [
    ProductInput(iron_plate, 1/50),
    ProductInput(sulfur, 5/50),
    ])

electronic_circuit = Product("electronic circuit", [
    ProductInput(iron_plate, 1.0),
    ProductInput(copper_cable, 3.0),
    ],
    1 / 0.5,
    [express_belt],
    )

advanced_circuit = Product("advanced circuit", [
    ProductInput(copper_cable, 4.0),
    ProductInput(electronic_circuit, 2.0),
    ProductInput(plastic_bar, 2.0),
    ],
    1 / 6,
    [express_belt],
    )

processing_unit = Product("processing unit", [
    ProductInput(electronic_circuit, 20.0), 
    ProductInput(advanced_circuit, 2.0), 
    ProductInput(sulfuric_acid, 5.0),
    ],
    1 / 10,
    [express_belt],
    )

speed_module_1 = Product("speed module 1", [
    ProductInput(electronic_circuit, 5.0),
    ProductInput(advanced_circuit, 5.0),
    ])

speed_module_2 = Product("speed module 2", [
    ProductInput(advanced_circuit, 5.0),
    ProductInput(processing_unit, 5.0),
    ProductInput(speed_module_1, 4.0),
    ])

speed_module_3 = Product("speed module 3", [
    ProductInput(advanced_circuit, 5.0),
    ProductInput(processing_unit, 5.0),
    ProductInput(speed_module_2, 5.0),
    ])

battery = Product("battery", [
    ProductInput(iron_plate, 1),
    ProductInput(copper_plate, 1),
    ProductInput(sulfuric_acid, 20),
    ])

accumulator = Product("accumulator", [
    ProductInput(iron_plate, 2),
    ProductInput(battery, 5)
    ])
  
low_density_structure = Product("low_density_structure", [
    ProductInput(copper_plate, 5),
    ProductInput(plastic_bar, 5),
    ProductInput(steel_plate, 10),
    ])

iron_gear_wheel = Product("iron_gear_wheel", [
    ProductInput(iron_plate, 2),
    ])

radar = Product("radar", [
    ProductInput(electronic_circuit, 5),
    ProductInput(iron_gear_wheel, 5),
    ProductInput(iron_plate, 10),
    ])

rocket_fuel = Product("rocket_fuel", [])

solar_panel = Product("solar_panel", [
    ProductInput(copper_plate, 5),
    ProductInput(electronic_circuit, 15),
    ProductInput(steel_plate, 5),
    ])

satellite = Product("satellite", [
    ProductInput(accumulator, 100),
    ProductInput(low_density_structure, 100),
    ProductInput(processing_unit, 100),
    ProductInput(radar, 5),
    ProductInput(rocket_fuel, 50),
    ProductInput(solar_panel, 100),
    ])

rocket_control_unit = Product("rocket_control_unit", [
    ProductInput(processing_unit, 1),
    ProductInput(speed_module_1, 1),
    ])

rocket_part = Product("rocket_part", [
    ProductInput(low_density_structure, 10),
    ProductInput(rocket_control_unit, 10),
    ProductInput(rocket_fuel, 10),
    ])

launch_satellite = Product("launch_satellite", [
    ProductInput(rocket_part, 100),
    ProductInput(satellite, 1),
    ])
    

tiers = []

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
        print("\t{:24} {:8.2f}".format(r.product.name, r.q))

        b = None
        if r.product.rate is not None:
            b = r.q / r.product.rate
            print("\t\tproduction buildings: {:8.2f}".format(b))
        
        if r.product.transport:
            print("\t\ttransport")
            for t in r.product.transport:
                x = r.q / t.rate
                print("\t\t\t{:24} {:8.2f}".format(t.name, x))

                if b is not None:
                    print("\t\t\t\t{:8.2f} production buildings per transport".format(b / math.ceil(x)))


production = Product("production", [
    ProductInput(speed_module_3, 1 / 3 / 60),
    ProductInput(speed_module_3, 1 / 3 / 60),
    ProductInput(speed_module_3, 1 / 3 / 60),
    ProductInput(launch_satellite, 1 / 10/ 60),
    ])

tiers_insert(production)

#print_all(electronic_circuit, 1)
print_all(production, 1)



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


#iron_plate.production_building_row_length()
#advanced_circuit.production_building_row_length()
#processing_unit.production_building_row_length()




