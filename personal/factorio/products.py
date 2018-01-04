import math
import itertools
import crayons

class Transport:
    def __init__(self, name, rate):
        self.name = name
        self.rate = rate

express_belt = Transport("express belt", 40)

class ProductInput:
    def __init__(self, product, q, lanes=None):
        self.product = product
        # qantity
        self.q = q
        # number of dedicated lanes for input
        self.lanes = lanes

    def mul(self, x):
        return ProductInput(self.product, self.q * x)

class Product:
    def __init__(self, name, inputs=None, rate=None, transport=[]):
        self.name = name
        self.inputs = inputs
        # the rate at which one production building will produce this
        self.rate = rate
        # methods that can transport this
        self.transport = transport

    def processes(self):
        #processes = [p for p in globals().values() if isinstance(p, Process)]

        #for p in processes:
        #    print(p.name)
        
        for p in processes:
            for i in p.inputs:
                if i.product == self:
                    if i.q < 0:
                        yield p
                        break

    def production_building_row_length(self):
        print()
        print(crayons.blue(self.name, bold=True))
        print("production building row length")
        print()

        inputs = list(self.inputs)

        # get inputs delivered on belts
        # multiply by production rate to get input rate
        inputs = [ProductInput(i.product, i.q * self.rate, i.lanes) for i in inputs if express_belt in i.product.transport]

        inputs.append(ProductInput(self, self.rate, 1))

        x = [(i.lanes * 18) / i.q for i in inputs]

        y = min(x)

        y = math.floor(y)
        
        #y = min(y, math.floor(18 / self.rate))
        y = min(y, 30)

        print("{:32} {:8} {:8} {:14}".format("item", "rate", "lanes", "max buildings"))
        for i, z in zip(inputs, x):
            print("{:32} {:8.2f} {:8} {:14.2f} {:14.2f}".format(i.product.name, i.q, i.lanes, z, i.q * y))
        
        
        print()


        print("max buildings: {:8d}".format(y))
        print("output rate:   {:8.2f}".format(y * self.rate))
        
        #y2 = math.floor(18 / self.rate)
        #if y2 < y:
        #    print("buildings for max 18 output rate:", y2)
        
        print()

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


water = Product(
        "water",
        [],
        1200,
        )

crude_oil = Product(
        "crude_oil",
        [],
        50,
        )

heavy_oil = Product(
        "heavy oil",
        )

light_oil = Product(
        "light oil",
        )

petroleum = Product(
        "petroleum", 
        [],
        55 / 5)


coal = Product(
        "coal", 
        [],
        0.525,
        [express_belt],
        )

iron_ore = Product(
        "iron ore", 
        [],
        0.525,
        [express_belt],
        )

copper_ore = Product("copper ore", [],
        0.525,
        )

plastic_bar = Product("plastic bar",
        [
            ProductInput(coal, 1 / 2, 2),
            ProductInput(petroleum, 20 / 2),
            ],
        2 / 1,
        [express_belt],
        )

sulfur = Product("sulfur", 
        [
            ProductInput(petroleum, 30 / 2),
            ProductInput(water, 30 / 2),
            ],
        2 / 1
        )

copper_plate = Product("copper plate",
    [
        ProductInput(copper_ore, 1, 1)
    ],
    0.57,
    [express_belt],
    )

copper_cable = Product("copper cable", [
    ProductInput(copper_plate, 0.5, 1)
    ],
    2 / 0.5,
    [express_belt],
    )

iron_plate = Product("iron plate",
    [
        ProductInput(iron_ore, 1, 1),
    ],
    0.57,
    [
        express_belt,
    ])

steel_plate = Product("steel plate", [
    ProductInput(iron_plate, 5.0)
    ],
    0.114
    )

sulfuric_acid = Product("sulfuric acid", [
    ProductInput(iron_plate, 1 / 50),
    ProductInput(sulfur, 5 / 50),
    ],
    50 / 1
    )

electronic_circuit = Product("electronic circuit", [
    ProductInput(iron_plate, 1.0),
    ProductInput(copper_cable, 3.0),
    ],
    1 / 0.5,
    [express_belt],
    )

advanced_circuit = Product("advanced circuit", [
    ProductInput(copper_cable, 4.0, 1),
    ProductInput(electronic_circuit, 2.0, 0.5),
    ProductInput(plastic_bar, 2.0, 0.5),
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
    ],
    1 / 15,
    )

speed_module_2 = Product("speed module 2", [
    ProductInput(advanced_circuit, 5.0),
    ProductInput(processing_unit, 5.0),
    ProductInput(speed_module_1, 4.0),
    ],
    1 / 30,
    )

speed_module_3 = Product("speed module 3", [
    ProductInput(advanced_circuit, 5.0),
    ProductInput(processing_unit, 5.0),
    ProductInput(speed_module_2, 5.0),
    ],
    1 / 60,
    )

battery = Product("battery", [
    ProductInput(iron_plate, 1),
    ProductInput(copper_plate, 1),
    ProductInput(sulfuric_acid, 20),
    ],
    1 / 5,
    )

accumulator = Product("accumulator", [
    ProductInput(iron_plate, 2),
    ProductInput(battery, 5)
    ],
    1 / 10,
    )
  
low_density_structure = Product("low_density_structure", [
    ProductInput(copper_plate, 5),
    ProductInput(plastic_bar, 5),
    ProductInput(steel_plate, 10),
    ],
    1 / 30,
    )

iron_gear_wheel = Product("iron_gear_wheel", [
    ProductInput(iron_plate, 2),
    ],
    1 / 0.5,
    [express_belt],
    )

radar = Product("radar", [
    ProductInput(electronic_circuit, 5),
    ProductInput(iron_gear_wheel, 5),
    ProductInput(iron_plate, 10),
    ],
    1 / 0.5,
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


