import math
import itertools
import crayons
import numpy as np
import scipy.optimize

from products import *

Process.electrical_energy = electrical_energy

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
        has_site=True,
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
        420,
        has_site=True,
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
        420,
        )

mine_stone = Process(
        "mine stone",
        [
            ProductInput(stone, -0.65),
            ],
        1,
        90,
        has_site=True,
        )

mine_iron_ore = Process(
        "mine iron ore",
        [
            ProductInput(iron_ore, -0.525),
            ],
        1,
        90,
        has_site=True,
        )

mine_copper_ore = Process(
        "mine copper ore",
        [
            ProductInput(copper_ore, -0.525),
            ],
        1,
        90,
        has_site=True,
        )

mine_coal = Process(
        "mine coal",
        [
            ProductInput(coal, -0.525),
            ],
        1,
        90,
        )

produce_plastic_bar = Process(
        "plastic bar",
        [
            ProductInput(coal, 1, 2),
            ProductInput(petroleum, 20),
            ProductInput(plastic_bar, -2, 1),
            ],
        1,
        has_site=True,
        )

produce_sulfur = Process(
        "sulfur", 
        [
            ProductInput(petroleum, 30),
            ProductInput(water, 30),
            ProductInput(sulfur, -2, 1),
            ],
        1,
        )

produce_iron_plate = Process(
        "iron plate",
        [
            ProductInput(iron_ore, 0.57, 1),
            ProductInput(iron_plate, -0.57, 1),
            ],
        1,
        180,
        has_site=True,
        )

produce_copper_plate = Process(
        "copper plate",
        [
            ProductInput(copper_ore, 0.57, 1),
            ProductInput(copper_plate, -0.57, 1),
            ],
        1,
        180,
        has_site=True,
        )

produce_copper_cable = Process(
        "copper cable", 
        [
            ProductInput(copper_plate, 1, 1),
            ProductInput(copper_cable, -2, 2),
            ],
        0.5,
        has_site=True,
        )

produce_steel_plate = Process("steel plate", 
        [
            ProductInput(iron_plate, 5, 2),
            ProductInput(steel_plate, -1, 1),
        ],
        8.772,
        180,
        has_site=True,
        )

produce_lubricant = Process(
        "lubricant",
        [
            ProductInput(heavy_oil, 10, 1),
            ProductInput(lubricant, -10),
            ],
        1,
        )

produce_sulfuric_acid = Process(
        "sulfuric acid",
        [
            ProductInput(iron_plate, 1, 1),
            ProductInput(sulfur, 5, 1),
            ProductInput(sulfuric_acid, -50),
            ],
        1,
        )

produce_electronic_circuit = Process("electronic circuit", 
        [
            ProductInput(iron_plate, 1, 1),
            ProductInput(copper_cable, 3, 2),
            ProductInput(electronic_circuit, -1, 1),
            ],
        0.5,
        has_site=True,
        )

produce_advanced_circuit = Process(
        "advanced circuit", 
        [
            ProductInput(copper_cable, 4, 1),
            ProductInput(electronic_circuit, 2, 0.5),
            ProductInput(plastic_bar, 2, 0.5),
            ProductInput(advanced_circuit, -1, 1),
            ],
        6,
        has_site=True,
        )

produce_processing_unit = Process("processing unit", 
        [
            ProductInput(electronic_circuit, 20, 2), 
            ProductInput(advanced_circuit, 2, 1), 
            ProductInput(sulfuric_acid, 5),
            ProductInput(processing_unit, -1, 1),
            ],
        10,
        )

produce_speed_module_1 = Process("speed module 1", 
        [
            ProductInput(electronic_circuit, 5.0),
            ProductInput(advanced_circuit, 5.0),
            ProductInput(speed_module_1, -1, 1),
            ],
        15,
        )

produce_speed_module_2 = Process("speed module 2", [
    ProductInput(advanced_circuit, 5.0),
    ProductInput(processing_unit, 5.0),
    ProductInput(speed_module_1, 4.0),
    ProductInput(speed_module_2, -1, 1),
    ],
    30,
    )

produce_speed_module_3 = Process("speed module 3", 
        [
            ProductInput(advanced_circuit, 5.0),
            ProductInput(processing_unit, 5.0),
            ProductInput(speed_module_2, 5.0),
            ProductInput(speed_module_3, -1, 1),
            ],
        60,
        )

produce_battery = Process("battery", 
        [
            ProductInput(iron_plate, 1, 1),
            ProductInput(copper_plate, 1, 1),
            ProductInput(sulfuric_acid, 20),
            ProductInput(battery, -1, 1)
            ],
        5,
        )

produce_accumulator = Process("accumulator", 
        [
            ProductInput(iron_plate, 2, 1),
            ProductInput(battery, 5, 2),
            ProductInput(accumulator, -1, 1),
            ],
        10,
        )
  
produce_low_density_structure = Process("low_density_structure", 
        [
            ProductInput(copper_plate, 5, 1),
            ProductInput(plastic_bar, 5, 1),
            ProductInput(steel_plate, 10, 1),
            ProductInput(low_density_structure, -1, 1),
            ],
        30,
        )

produce_iron_gear_wheel = Process(
        "iron_gear_wheel", 
        [
            ProductInput(iron_plate, 2, 2),
            ProductInput(iron_gear_wheel, -1, 1),
            ],
        0.5,
        has_site=True,
        )

produce_radar = Process("radar", 
        [
            ProductInput(electronic_circuit, 5),
            ProductInput(iron_gear_wheel, 5),
            ProductInput(iron_plate, 10),
            ProductInput(radar, -1, 1),
            ],
        0.5,
        )

heavy_oil_to_solid_fuel = Process(
        "heavy oil to solid fuel",
        [
            ProductInput(heavy_oil, 20),
            ProductInput(solid_fuel, -1, 1),
            ],
        3,
        )

light_oil_to_solid_fuel = Process(
        "light oil to solid fuel",
        [
            ProductInput(light_oil, 10),
            ProductInput(solid_fuel, -1, 1),
            ],
        3,
        )

produce_rocket_fuel = Process(
        "rocket_fuel",
        [
            ProductInput(solid_fuel, 10, 2),
            ProductInput(rocket_fuel, -1, 1),
            ],
        30,
        )

produce_solar_panel = Process("solar_panel", 
        [
            ProductInput(copper_plate, 5),
            ProductInput(electronic_circuit, 15),
            ProductInput(steel_plate, 5),
            ProductInput(solar_panel, -1, 1),
            ],
        10,
        )

produce_satellite = Process(
        "satellite", 
        [
            ProductInput(accumulator, 100),
            ProductInput(low_density_structure, 100),
            ProductInput(processing_unit, 100),
            ProductInput(radar, 5),
            ProductInput(rocket_fuel, 50),
            ProductInput(solar_panel, 100),
            ProductInput(satellite, -1, 1),
            ],
        5,
        )

produce_rocket_control_unit = Process(
        "rocket control unit", 
        [
            ProductInput(processing_unit, 1),
            ProductInput(speed_module_1, 1),
            ProductInput(rocket_control_unit, -1, 1),
            ],
        30,
        )

produce_rocket_part = Process("rocket_part", 
        [
            ProductInput(low_density_structure, 10),
            ProductInput(rocket_control_unit, 10),
            ProductInput(rocket_fuel, 10),
            ProductInput(rocket_part, -1),
            ],
        3,
        )

produce_satellite_launch = Process(
        "satellite_launch", 
        [
            ProductInput(rocket_part, 100),
            ProductInput(satellite, 1),
            ProductInput(satellite_launch, -1, 1),
            ],
        0,
        )

produce_inserter = Process("inserter",
        [
            ProductInput(electronic_circuit, 1, 1),
            ProductInput(iron_gear_wheel, 1, 1),
            ProductInput(iron_plate, 1, 1),
            ProductInput(inserter, -1, 1),
            ],
        0.5,
        has_site=True,
        )

produce_fast_inserter = Process("fast inserter",
        [
            ProductInput(electronic_circuit, 2, 1),
            ProductInput(inserter, 1, 1),
            ProductInput(iron_plate, 2, 1),
            ProductInput(fast_inserter, -1, 1),
            ],
        0.5,
        has_site=True,
        )

produce_stack_inserter = Process("stack inserter",
        [
            ProductInput(advanced_circuit, 1, 1),
            ProductInput(electronic_circuit, 15, 1),
            ProductInput(fast_inserter, 1, 1),
            ProductInput(iron_gear_wheel, 15, 1),
            ProductInput(stack_inserter, -1, 1),
            ],
        0.5,
        has_site=True,
        )

produce_transport_belt = Process(
        "transport_belt",
        [
            ProductInput(iron_gear_wheel, 1, 1),
            ProductInput(iron_plate, 1, 1),
            ProductInput(transport_belt, -1, 1),
            ],
        0.5,
        )

produce_fast_transport_belt = Process(
        "fast transport belt",
        [
            ProductInput(iron_gear_wheel, 5, 1),
            ProductInput(transport_belt, 1, 1),
            ProductInput(fast_transport_belt, -1, 1),
            ],
        0.5,
        )

produce_express_transport_belt = Process(
        "express transport belt",
        [
            ProductInput(fast_transport_belt, 1, 1),
            ProductInput(iron_gear_wheel, 10, 1),
            ProductInput(lubricant, 20),
            ProductInput(express_transport_belt, -1, 1),
            ],
        0.5,
        )

produce_electric_mining_drill = Process(
        "electric mining drill",
        [
            ProductInput(electronic_circuit, 3, 0.5),
            ProductInput(iron_gear_wheel, 5, 0.5),
            ProductInput(iron_plate, 10, 0.5),
            ProductInput(electric_mining_drill, -1, 1),
            ],
        2,
        )

produce_science_pack_1 = Process("science pack 1",
        [
            ProductInput(copper_plate, 1, 0.5),
            ProductInput(iron_gear_wheel, 1, 0.5),
            ProductInput(science_pack_1, -1, 1),
            ],
        5,
        has_site=True,
        )

produce_science_pack_2 = Process("science pack 2",
        [
            ProductInput(inserter, 1, 0.5),
            ProductInput(transport_belt, 1, 0.5),
            ProductInput(science_pack_2, -1, 1),
            ],
        6,
        has_site=True,
        )

produce_science_pack_3 = Process(
        "science pack 3",
        [
            ProductInput(advanced_circuit, 1, 0.5),
            ProductInput(electric_mining_drill, 1, 0.5),
            ProductInput(engine_unit, 1, 0.5),
            ProductInput(science_pack_3, -1, 1),
            ],
        12,
        has_site=True,
        )

produce_firearm_magazine = Process(
        "firearm magazine",
        [
            ProductInput(iron_plate, 4, 1),
            ProductInput(firearm_magazine, -1, 1),
            ],
        1,
        )

produce_piercing_rounds_magazine = Process(
        "piercing rounds magazine",
        [
            ProductInput(copper_plate, 5, 1),
            ProductInput(firearm_magazine, 1, 1),
            ProductInput(steel_plate, 1, 1),
            ProductInput(piercing_rounds_magazine, -1, 1),
            ],
        3,
        )

produce_defender_capsule = Process(
        "defender capsule",
        [
            ProductInput(electronic_circuit, 2, 1),
            ProductInput(iron_gear_wheel, 3, 1),
            ProductInput(piercing_rounds_magazine, 1, 1),
            ProductInput(defender_capsule, -1, 1),
            ],
        8,
        )

produce_distractor_capsule = Process(
        "distractor capsule",
        [
            ProductInput(advanced_circuit, 3, 1),
            ProductInput(defender_capsule, 4, 1),
            ProductInput(distractor_capsule, -1, 1),
            ],
        15,
        )

produce_destroyer_capsule = Process(
        "destroyer capsule",
        [
            ProductInput(distractor_capsule, 4, 1),
            ProductInput(speed_module_1, 1, 1),
            ProductInput(destroyer_capsule, -1, 1),
            ],
        15,
        )

solar_panel_power = Process(
        "solar panel power",
        [
            ProductInput(electrical_energy, -42),
            ],
        1,
        )

produce_engine_unit = Process(
        "engine unit",
        [
            ProductInput(iron_gear_wheel, 1, 0.5),
            ProductInput(pipe, 2, 0.5),
            ProductInput(steel_plate, 1, 0.5),
            ProductInput(engine_unit, -1, 1),
            ],
        10,
        )

produce_pipe = Process(
        "pipe",
        [
            ProductInput(iron_plate, 1, 1),
            ProductInput(pipe, -1, 1),
            ],
        0.5,
        )

produce_explosives = Process(
        "explosives",
        [
            ProductInput(coal, 1, 1),
            ProductInput(sulfur, 1, 1),
            ProductInput(water, 10, 1),
            ProductInput(explosives, -1, 1),
            ],
        5,
        )

produce_explosive_cannon_shell = Process(
        "explosive_cannon_shell",
        [
            ProductInput(explosives, 2, 1),
            ProductInput(plastic_bar, 2, 1),
            ProductInput(steel_plate, 2, 1),
            ProductInput(explosive_cannon_shell, -1, 1),
            ],
        8,
        )

produce_artillery_shell = Process(
        "artillery_shell",
        [
            ProductInput(explosive_cannon_shell, 4, 1),
            ProductInput(explosives, 8, 1),
            ProductInput(radar, 1, 1),
            ProductInput(artillery_shell, -1, 1),
            ],
        15,
        )

produce_rail = Process(
        "rail",
        [
            ProductInput(iron_stick, 1, 1),
            ProductInput(steel_plate, 1, 1),
            ProductInput(stone, 1, 1),
            ProductInput(rail, -2, 1),
            ],
        0.5,
        )

produce_iron_stick = Process(
        "iron stick",
        [
            ProductInput(iron_plate, 1, 1),
            ProductInput(iron_stick, -2, 1),
            ],
        0.5,
        )

produce_new_base_supplies = Process(
        "new base supplies",
        [
            ProductInput(stack_inserter, 48),
            ProductInput(express_transport_belt, 200),
            ProductInput(rail, 100),
            ProductInput(new_base_supplies, -1),
            ],
        0,
        )

production = Process("production", 
        [
            ProductInput(speed_module_3, 1 / 3),
            ProductInput(speed_module_3, 1 / 3),
            ProductInput(speed_module_3, 1 / 3),
            ProductInput(satellite_launch, 1 / 10),
            ProductInput(destroyer_capsule, 1 / 1),
            ProductInput(piercing_rounds_magazine, 1 / 1),
            ProductInput(science_pack_1, 10),
            ProductInput(science_pack_2, 10),
            ProductInput(science_pack_3, 10),
            ProductInput(new_base_supplies, 1 / 30),
            ProductInput(artillery_shell, 10),
            ],
        60,
        )


#x.process_default = produce_x
#x.process_default = produce_x
#x.process_default = produce_x
#x.process_default = produce_x
#x.process_default = produce_x
iron_stick.process_default = produce_iron_stick
rail.process_default = produce_rail
lubricant.process_default = produce_lubricant
fast_transport_belt.process_default = produce_fast_transport_belt
express_transport_belt.process_default = produce_express_transport_belt
stone.process_default = mine_stone
explosives.process_default = produce_explosives
explosive_cannon_shell.process_default = produce_explosive_cannon_shell
artillery_shell.process_default = produce_artillery_shell
new_base_supplies.process_default = produce_new_base_supplies
pipe.process_default = produce_pipe
engine_unit.process_default = produce_engine_unit
firearm_magazine.process_default = produce_firearm_magazine
piercing_rounds_magazine.process_default = produce_piercing_rounds_magazine
defender_capsule.process_default = produce_defender_capsule
distractor_capsule.process_default = produce_distractor_capsule
destroyer_capsule.process_default = produce_destroyer_capsule
rocket_control_unit.process_default = produce_rocket_control_unit
rocket_part.process_default = produce_rocket_part
satellite_launch.process_default = produce_satellite_launch
speed_module_1.process_default = produce_speed_module_1
speed_module_2.process_default = produce_speed_module_2
speed_module_3.process_default = produce_speed_module_3
electric_mining_drill.process_default = produce_electric_mining_drill
transport_belt.process_default = produce_transport_belt
science_pack_1.process_default = produce_science_pack_1
science_pack_2.process_default = produce_science_pack_2
science_pack_3.process_default = produce_science_pack_3
inserter.process_default = produce_inserter
fast_inserter.process_default = produce_fast_inserter
stack_inserter.process_default = produce_stack_inserter
solar_panel.process_default = produce_solar_panel
rocket_fuel.process_default = produce_rocket_fuel
iron_gear_wheel.process_default = produce_iron_gear_wheel
radar.process_default = produce_radar
advanced_circuit.process_default = produce_advanced_circuit
copper_cable.process_default = produce_copper_cable
electronic_circuit.process_default = produce_electronic_circuit
processing_unit.process_default = produce_processing_unit
steel_plate.process_default = produce_steel_plate
coal.process_default = mine_coal
plastic_bar.process_default = produce_plastic_bar
low_density_structure.process_default = produce_low_density_structure

electrical_energy.process_default = solar_panel_power

water.process_default = mine_water
crude_oil.process_default = mine_crude_oil

petroleum.process_default = advanced_oil_processing
sulfur.process_default = produce_sulfur
sulfuric_acid.process_default = produce_sulfuric_acid
battery.process_default = produce_battery

iron_ore.process_default = mine_iron_ore
iron_plate.process_default = produce_iron_plate

copper_ore.process_default = mine_copper_ore
copper_plate.process_default = produce_copper_plate

accumulator.process_default = produce_accumulator
satellite.process_default = produce_satellite

solid_fuel.process_default = light_oil_to_solid_fuel
light_oil.process_default = advanced_oil_processing
heavy_oil.process_default = advanced_oil_processing

