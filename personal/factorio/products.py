import math
import itertools
import crayons

from process import *
from product import *


concrete = Product(
        "concrete",
        )

electrical_energy = Product(
        "electrical energy",
        )

nuclear_reactor = Product(
        "nuclear reactor",
        )

heat_exchanger = Product(
        "heat exchanger",
        )

heat_energy = Product(
        "heat energy",
        )

steam_500 = Product(
        "steam 500 C",
        )
steam_500.energy = 97 # kJ

water = Product(
        "water",
        )

crude_oil = Product(
        "crude_oil",
        )

heavy_oil = Product(
        "heavy oil",
        )

light_oil = Product(
        "light oil",
        )

petroleum = Product(
        "petroleum", 
        )

coal = Product(
        "coal", 
        [express_belt],
        )

iron_ore = Product(
        "iron ore", 
        [express_belt],
        )

copper_ore = Product(
        "copper ore", 
        [express_belt],
        )

plastic_bar = Product(
        "plastic bar",
        [express_belt],
        )

sulfur = Product(
        "sulfur", 
        [express_belt],
        )

copper_plate = Product("copper plate",
    [express_belt],
    )

copper_cable = IntermediateProduct(
        "copper cable", 
        200,
        )

iron_plate = IntermediateProduct(
        "iron plate",
        100,
        )

steel_plate = Product("steel plate", 
        [express_belt],
        )

sulfuric_acid = Product("sulfuric acid", 
    )

lubricant = Product(
        "lubricant",
        )

electronic_circuit = Product("electronic circuit",
        [express_belt],
        )

advanced_circuit = Product("advanced circuit", 
        [express_belt],
        )

processing_unit = Product("processing unit",
    [express_belt],
    )

speed_module_1 = Product("speed module 1",
    )

speed_module_2 = Product("speed module 2",
    )

speed_module_3 = Product("speed module 3",
    )

battery = Product("battery",
    )

accumulator = Product("accumulator",
    )
  
low_density_structure = Product("low_density_structure",
    )

iron_gear_wheel = Product("iron_gear_wheel",
    [express_belt],
    )

radar = Product("radar",
    )

rocket_fuel = Product("rocket_fuel",
        )

solar_panel = Product("solar_panel",
    )

satellite = Product("satellite",
    )

satellite_launch = Product(
        "satellite launch",
        )

rocket_control_unit = Product("rocket_control_unit",
        )

rocket_part = Product("rocket_part",
        )

inserter = Product("inserter",
        [express_belt],
        )

fast_inserter = Product("fast inserter",
        [express_belt],
        )

stack_inserter = Product("stack inserter",
        [express_belt],
        )

transport_belt = Product(
        "transport_belt",
        [express_belt],
        )

fast_transport_belt = Product(
        "fast transport_belt",
        [express_belt],
        )

express_transport_belt = Product(
        "express_transport_belt",
        [express_belt],
        )

science_pack_1 = Product("science pack 1",
        [express_belt],
        )

science_pack_2 = Product(
        "science pack 2",
        [express_belt],
        )

science_pack_3 = Product(
        "science pack 3",
        [express_belt],
        )

military_science_pack = Product(
        "military science pack",
        [express_belt],
        )

production_science_pack = Product(
        "production science pack",
        [express_belt],
        )

high_tech_science_pack = Product(
        "high tech science pack",
        [express_belt],
        )

space_science_pack = Product(
        "space science pack",
        [express_belt],
        )

firearm_magazine = Product(
        "firearm magazine",
        [express_belt],
        )

grenade = Product(
        "grenade",
        [express_belt],
        )

gun_turret = Product(
        "gun turret",
        [express_belt],
        )

electric_engine_unit = Product(
        "electric engine unit",
        [express_belt],
        )

electric_furnace = Product(
        "electric furnace",
        [express_belt],
        )

stone_brick = Product(
        "stone brick",
        [express_belt],
        )

piercing_rounds_magazine = Product(
        "piercing rounds magazine",
        [express_belt],
        )

defender_capsule = Product(
        "defender capsule",
        )

distractor_capsule = Product(
        "distractor capsule",
        )

destroyer_capsule = Product(
        "destroyer capsule",
        )

electric_mining_drill = Product(
        "electric_mining_drill",
        [express_belt],
        )

engine_unit = Product(
        "engine unit",
        [express_belt],
        )

pipe = Product(
        "pipe",
        [express_belt],
        )

new_base_supplies = Product(
        "new base supplies",
        )

solid_fuel = Product(
        "solid fuel",
        [express_belt],
        )

explosives = Product(
        "explosives",
        [express_belt],
        )

explosive_cannon_shell = Product(
        "explosive_cannon_shell",
        [express_belt],
        )

artillery_shell = Product(
        "artillery_shell",
        [express_belt],
        )

stone = Product(
        "stone",
        [express_belt],
        )

rail = Product(
        "rail",
        [express_belt],
        )

iron_stick = Product(
        "iron stick",
        [express_belt],
        )

uranium_ore = Product(
        "uranium ore",
        [express_belt],
        )

uranium_235 = Product(
        "uranium 235",
        [express_belt],
        )

uranium_238 = Product(
        "uranium 238",
        [express_belt],
        )

uranium_fuel_cell = Product(
        "uranium fuel cell",
        [express_belt],
        )

chemical_plant = Product(
        "chemical plant",
        [express_belt],
        )

steam_turbine = Product(
        "steam turbine",
        )

stack_filter_inserter = Product(
        "stack filter inserter",
        )

assembling_machine_1 = Product(
        "assembling machine 1",
        )

assembling_machine_2 = Product(
        "assembling machine 2",
        )

assembling_machine_3 = Product(
        "assembling machine 3",
        )

rail_signal = Product(
        "rail signal",
        )

rail_chain_signal = Product(
        "rail chain signal",
        )



