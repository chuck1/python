import math
import itertools
import crayons

from process import *
from product import *


concrete = Product(
        "concrete",
        100,
        )

electrical_energy = Other(
        "electrical energy",
        )

nuclear_reactor = Product(
        "nuclear reactor",
        10,
        module_slots=0,
        )

heat_exchanger = Product(
        "heat exchanger",
        50,
        )

heat_energy = Other(
        "heat energy",
        )

steam_500 = Liquid(
        "steam 500 C",
        )

steam_500.energy = 97 # kJ

water = Liquid(
        "water",
        )

crude_oil = Liquid(
        "crude_oil",
        )

heavy_oil = Liquid(
        "heavy oil",
        )

light_oil = Liquid(
        "light oil",
        )

petroleum = Liquid(
        "petroleum", 
        )

coal = IntermediateProduct(
        "coal", 
        50,
        )

iron_ore = IntermediateProduct(
        "iron ore", 
        50,
        )

copper_ore = IntermediateProduct(
        "copper ore", 
        50,
        )

plastic_bar = IntermediateProduct(
        "plastic bar",
        100,
        )

sulfur = IntermediateProduct(
        "sulfur", 
        50,
        )

copper_plate = IntermediateProduct(
        "copper plate",
        100,
        )

copper_cable = IntermediateProduct(
        "copper cable", 
        200,
        )

iron_plate = IntermediateProduct(
        "iron plate",
        100,
        )

steel_plate = IntermediateProduct(
        "steel plate", 
        100,
        )

sulfuric_acid = Liquid(
        "sulfuric acid", 
        )

lubricant = Liquid(
        "lubricant",
        )

electronic_circuit = IntermediateProduct(
        "electronic circuit",
        200,
        )

advanced_circuit = IntermediateProduct(
        "advanced circuit", 
        200,
        )

processing_unit = IntermediateProduct(
        "processing unit",
        100,
        )

speed_module_1 = Product(
        "speed module",
        50,
        )

speed_module_2 = Product(
        "speed module 2",
        50,
        )

speed_module_3 = Product(
        "speed module 3",
        50,
        )

battery = IntermediateProduct(
        "battery",
        200,
        )

accumulator = Product(
        "accumulator",
        50,
        )
  
low_density_structure = IntermediateProduct(
        "low_density_structure",
        10,
        )

iron_gear_wheel = IntermediateProduct(
        "iron_gear_wheel",
        100,
        )

radar = Product(
        "radar",
        50,
        )

rocket_fuel = IntermediateProduct("rocket_fuel",
        10,
        )

solar_panel = Product("solar_panel",
        50,
        )

satellite = Product(
        "satellite",
        1,
        )

satellite_launch = Other(
        "satellite launch",
        )

rocket_control_unit = IntermediateProduct(
        "rocket_control_unit",
        10,
        )

rocket_part = IntermediateProduct("rocket_part",
        5,
        )

inserter = Product("inserter",
        50,
        )

fast_inserter = Product("fast inserter",
        50,
        )

stack_inserter = Product("stack inserter",
        50,
        )

transport_belt = Product(
        "transport_belt",
        100,
        )

fast_transport_belt = Product(
        "fast transport_belt",
        100,
        )

express_transport_belt = Product(
        "express_transport_belt",
        100,
        )

science_pack_1 = IntermediateProduct("science pack 1",
        200,
        )

science_pack_2 = IntermediateProduct(
        "science pack 2",
        200,
        )

science_pack_3 = IntermediateProduct(
        "science pack 3",
        200,
        )

military_science_pack = IntermediateProduct(
        "military science pack",
        200,
        )

production_science_pack = IntermediateProduct(
        "production science pack",
        200,
        )

high_tech_science_pack = IntermediateProduct(
        "high tech science pack",
        200,
        )

space_science_pack = Product(
        "space science pack",
        2000,
        )

firearm_magazine = Product(
        "firearm magazine",
        200,
        )

grenade = Product(
        "grenade",
        100,
        )

gun_turret = Product(
        "gun turret",
        50,
        )

electric_engine_unit = IntermediateProduct(
        "electric engine unit",
        50,
        )

electric_furnace = Product(
        "electric furnace",
        50,
        module_slots=2,
        )

stone_brick = IntermediateProduct(
        "stone brick",
        100,
        )

piercing_rounds_magazine = Product(
        "piercing rounds magazine",
        200,
        )

defender_capsule = Product(
        "defender capsule",
        100,
        )

distractor_capsule = Product(
        "distractor capsule",
        100,
        )

destroyer_capsule = Product(
        "destroyer capsule",
        100,
        )

electric_mining_drill = Product(
        "electric_mining_drill",
        50,
        module_slots=3,
        )

engine_unit = IntermediateProduct(
        "engine unit",
        50,
        )

pipe = Product(
        "pipe",
        100,
        )

new_base_supplies = Other(
        "new base supplies",
        )

solid_fuel = IntermediateProduct(
        "solid fuel",
        50,
        )

explosives = IntermediateProduct(
        "explosives",
        50,
        )

explosive_cannon_shell = Product(
        "explosive_cannon_shell",
        200,
        )

artillery_shell = Product(
        "artillery_shell",
        1,
        )

stone = IntermediateProduct(
        "stone",
        50,
        )

rail = Product(
        "rail",
        100,
        )

iron_stick = IntermediateProduct(
        "iron stick",
        100,
        )

uranium_ore = IntermediateProduct(
        "uranium ore",
        50,
        )

uranium_235 = Product(
        "uranium 235",
        100,
        )

uranium_238 = Product(
        "uranium 238",
        100,
        )

uranium_fuel_cell = Product(
        "uranium fuel cell",
        50,
        )

chemical_plant = Product(
        "chemical plant",
        10,
        module_slots=3,
        )

steam_turbine = Product(
        "steam turbine",
        10,
        module_slots=0,
        )

stack_filter_inserter = Product(
        "stack filter inserter",
        50,
        )

assembling_machine_1 = Product(
        "assembling machine 1",
        50,
        )

assembling_machine_2 = Product(
        "assembling machine 2",
        50,
        )

assembling_machine_3 = Product(
        "assembling machine 3",
        50,
        module_slots=4,
        base_speed=1.25,
        )

rail_signal = Product(
        "rail signal",
        50,
        )

rail_chain_signal = Product(
        "rail chain signal",
        50,
        )

rocket_silo = Product(
        "rocket silo",
        1,
        module_slots=4,
        )

oil_refinery = Product(
        "oil refinery",
        10,
        module_slots=3,
        )

lab = Product(
        "lab",
        10,
        module_slots=2,
        )

pumpjack = Product(
        "pumpjack",
        20,
        module_slots=2,
        )


