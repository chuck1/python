import itertools

class ProductInput:
    def __init__(self, product, q=None):
        self.product = product
        # qantity
        self.q = q

    def mul(self, x):
        return ProductInput(self.product, self.q * x)

class Product:
    def __init__(self, name, inputs):
        self.name = name
        self.inputs = inputs

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


iron_ore = Product("iron ore", [])

copper_ore = Product("copper ore", [])

plastic_bar = Product("plastic bar", [])

sulfur = Product("sulfur", [])

copper_plate = Product("copper plate", [
    ProductInput(copper_ore, 1.0)
    ])

copper_cable = Product("copper cable", [
    ProductInput(copper_plate, 0.5)
    ])

iron_plate = Product("iron plate", [
    ProductInput(iron_ore, 1.0)
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
    ])

advanced_circuit = Product("advanced circuit", [
    ProductInput(copper_cable, 4.0),
    ProductInput(electronic_circuit, 2.0),
    ProductInput(plastic_bar, 2.0),
    ])

processing_unit = Product("processing unit", [
    ProductInput(electronic_circuit, 20.0), 
    ProductInput(advanced_circuit, 2.0), 
    ProductInput(sulfuric_acid, 5.0),
    ])

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

launch_satellite = Product("rocket_part", [
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

    return i_max

tiers_insert(processing_unit)

for t in tiers:
    print([p.name for p in t])

def print_raw(p, x):
    print(p.name)
    for r in p.raw(x):
        print("\t{:16} {:8.2f}".format(r.product.name, r.q))


production = Product("production", [
    ProductInput(speed_module_3, 1 / 3 / 60),
    ProductInput(speed_module_3, 1 / 3 / 60),
    ProductInput(speed_module_3, 1 / 3 / 60),
    ProductInput(launch_satellite, 1 / 10/ 60),
    ])

print_raw(production, 1)






