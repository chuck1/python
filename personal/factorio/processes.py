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
        building=electric_mining_drill,
        )

produce_stone_brick = Process(
        "stone brick",
        [
            ProductInput(stone, 2, 1),
            ProductInput(stone_brick, -1, 1),
            ],
        3.5,
        has_site=True,
        )

mine_iron_ore = Process(
        "mine iron ore",
        [
            ProductInput(iron_ore, -1),
            ],
        1.905,
        90,
        has_site=True,
        building=electric_mining_drill,
        )

mine_copper_ore = Process(
        "mine copper ore",
        [
            ProductInput(copper_ore, -0.525),
            ],
        1,
        90,
        has_site=True,
        building=electric_mining_drill,
        )

mine_coal = Process(
        "mine coal",
        [
            ProductInput(coal, -0.525),
            ],
        1,
        90,
        has_site=True,
        building=electric_mining_drill,
        )

mine_uranium_ore = Process(
        "uranium_ore",
        [
            ProductInput(sulfuric_acid, 1),
            ProductInput(uranium_ore, -1),
            ],
        1.905,
        has_site=True,
        building=electric_mining_drill,
        )

uranium_processing = Process(
        "uranium processing",
        [
            ProductInput(uranium_ore, 10),
            ProductInput(uranium_235, -0.007),
            ProductInput(uranium_238, -0.993),
            ],
        10,
        )

uranium_enrichment = Process(
        "uranium enrichment",
        [
            ProductInput(uranium_238, 3),
            ProductInput(uranium_235, -1),
            ],
        50,
        )

produce_uranium_fuel_cell = Process(
        "uranium fuel cell",
        [
            ProductInput(iron_plate, 10),
            ProductInput(uranium_235, 1),
            ProductInput(uranium_238, 19),
            ProductInput(uranium_fuel_cell, -10),
            ],
        10,
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
        has_site=True,
        )

produce_iron_plate = Process(
        "iron plate",
        [
            ProductInput(iron_ore, 0.57, 2),
            ProductInput(iron_plate, -0.57, 2),
            ],
        1,
        180,
        has_site=True,
        )

produce_copper_plate = Process(
        "copper plate",
        [
            ProductInput(copper_ore, 0.57, 2),
            ProductInput(copper_plate, -0.57, 2),
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
        has_site=True,
        )

produce_sulfuric_acid = Process(
        "sulfuric acid",
        [
            ProductInput(iron_plate, 1, 1),
            ProductInput(sulfur, 5, 1),
            ProductInput(sulfuric_acid, -50),
            ],
        1,
        has_site=True,
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
        has_site=True,
        )

produce_speed_module_1 = Process("speed module 1", 
        [
            ProductInput(electronic_circuit, 5.0),
            ProductInput(advanced_circuit, 5.0),
            ProductInput(speed_module_1, -1, 1),
            ],
        15,
        has_site=True,
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
        has_site=True,
        )

produce_accumulator = Process("accumulator", 
        [
            ProductInput(iron_plate, 2, 1),
            ProductInput(battery, 5, 2),
            ProductInput(accumulator, -1, 1),
            ],
        10,
        has_site=True,
        )
  
produce_low_density_structure = Process("low_density_structure", 
        [
            ProductInput(copper_plate, 5, 1),
            ProductInput(plastic_bar, 5, 1),
            ProductInput(steel_plate, 10, 1),
            ProductInput(low_density_structure, -1, 1),
            ],
        30,
        has_site=True,
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
        building=chemical_plant
        )

produce_chemical_plant = Process(
        "chemical plant",
        [
            ProductInput(electronic_circuit, 5, 1),
            ProductInput(iron_gear_wheel, 5, 1),
            ProductInput(pipe, 5, 1),
            ProductInput(steel_plate, 5, 1),
            ProductInput(chemical_plant, -1, 1),
            ],
        5,
        210,
        )

produce_rocket_fuel = Process(
        "rocket_fuel",
        [
            ProductInput(solid_fuel, 10, 2),
            ProductInput(rocket_fuel, -1, 1),
            ],
        30,
        has_site=True,
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
        4000,
        )

produce_satellite_launch = Process(
        "satellite_launch", 
        [
            ProductInput(rocket_part, 100),
            ProductInput(satellite, 1),
            #ProductInput(satellite_launch, -1, 1),
            ProductInput(space_science_pack, -1000, 1),
            ],
        0,
        has_site=True,
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

produce_stack_filter_inserter = Process(
        "stack filter inserter",
        [
            ProductInput(electronic_circuit, 5, 1),
            ProductInput(stack_inserter, 1, 1),
            ProductInput(stack_filter_inserter, -1, 1),
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
        has_site=True,
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

produce_electric_furnace = Process(
        "electric furnace",
        [
            ProductInput(advanced_circuit, 5, 1),
            ProductInput(steel_plate, 10, 1),
            ProductInput(stone_brick, 10, 1),
            ProductInput(electric_furnace, -1, 1),
            ],
        5,
        has_site=True,
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
        has_site=True,
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

produce_military_science_pack = Process(
        "military science pack",
        [
            ProductInput(grenade, 1, 1),
            ProductInput(gun_turret, 1, 1),
            ProductInput(piercing_rounds_magazine, 1, 1),
            ProductInput(military_science_pack, -2, 1),
            ],
        10,
        has_site=True,
        )

produce_production_science_pack = Process(
        "production science pack",
        [
            ProductInput(electric_engine_unit, 1, 1),
            ProductInput(electric_furnace, 1, 1),
            ProductInput(production_science_pack, -2, 1),
            ],
        14,
        has_site=True,
        )

produce_high_tech_science_pack = Process(
        "high tech science pack",
        [
            ProductInput(battery, 1, 1),
            ProductInput(copper_cable, 30, 1),
            ProductInput(processing_unit, 3, 1),
            ProductInput(speed_module_1, 1, 1),
            ProductInput(high_tech_science_pack, -2, 1),
            ],
        14,
        has_site=True,
        )

produce_firearm_magazine = Process(
        "firearm magazine",
        [
            ProductInput(iron_plate, 4, 1),
            ProductInput(firearm_magazine, -1, 1),
            ],
        1,
        has_site=True,
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
        has_site=True,
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

solar_power = Process(
        "solar power",
        [
            ProductInput(electrical_energy, -42),
            ],
        1,
        )

#includes 300% neighbor bonus
nuclear_power = Process(
        "nuclear power",
        [
            ProductInput(uranium_fuel_cell, 1),
            ProductInput(heat_energy, -8000000 * 4),
            ],
        200,
        building=nuclear_reactor
        )

heat_exchanger_process = Process(
        "heat exchanger process",
        [
            ProductInput(heat_energy, 10000),
            ProductInput(steam_500, -10000 / 97),
            ],
        1,
        )

steam_turbine_process = Process(
        "steam turbine process",
        [
            ProductInput(steam_500, 60),
            ProductInput(electrical_energy, -60 * steam_500.energy),
            ],
        1,
        building=steam_turbine
        )



research = Process(
        "research",
        [
            ProductInput(science_pack_1, 1),
            ProductInput(science_pack_2, 1),
            ProductInput(science_pack_3, 1),
            ProductInput(military_science_pack, 1),
            ProductInput(production_science_pack, 1),
            ProductInput(high_tech_science_pack, 1),
            ProductInput(space_science_pack, 1),
            ],
        1,
        has_site=True,
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
        has_site=True,
        )

produce_electric_engine_unit = Process(
        "electric engine unit",
        [
            ProductInput(electronic_circuit, 2, 1),
            ProductInput(engine_unit, 1, 1),
            ProductInput(lubricant, 15),
            ProductInput(electric_engine_unit, -1, 1),
            ],
        10,
        has_site=True,
        )

produce_pipe = Process(
        "pipe",
        [
            ProductInput(iron_plate, 1, 1),
            ProductInput(pipe, -1, 1),
            ],
        0.5,
        has_site=True,
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

produce_gun_turret = Process(
        "gun turret",
        [
            ProductInput(copper_plate, 10, 1),
            ProductInput(iron_gear_wheel, 10, 1),
            ProductInput(iron_plate, 20, 1),
            ProductInput(gun_turret, -1, 1),
            ],
        8,
        has_site=True,
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

produce_grenade = Process(
        "grenade",
        [
            ProductInput(coal, 10, 1),
            ProductInput(iron_plate, 5, 1),
            ProductInput(grenade, -1, 1),
            ],
        8,
        has_site=True,
        )

produce_nuclear_reactor = Process(
        "nuclear reactor",
        [
           ProductInput(advanced_circuit, 500),
           ProductInput(concrete, 500),
           ProductInput(copper_plate, 500),
           ProductInput(steel_plate, 500),
           ProductInput(nuclear_reactor, -1),
           ],
        3,
        )

produce_concrete = Process(
        "concrete",
        [
           ProductInput(iron_ore, 1),
           ProductInput(stone_brick, 5),
           ProductInput(water, 100),
           ProductInput(concrete, -10),
           ],
        10,
        )

produce_heat_exchanger = Process(
        "heat exchanger",
        [
           ProductInput(copper_plate, 100),
           ProductInput(pipe, 10),
           ProductInput(steel_plate, 10),
           ProductInput(heat_exchanger, -1),
           ],
        3,
        )

produce_steam_turbine = Process(
        "steam turbine",
        [
           ProductInput(copper_plate, 50),
           ProductInput(iron_gear_wheel, 50),
           ProductInput(pipe, 20),
           ProductInput(steam_turbine, -1),
           ],
        3,
        )

produce_assembling_machine_1 = Process(
        "assembling machine 1",
        [
            ProductInput(electronic_circuit, 3),
            ProductInput(iron_gear_wheel, 5),
            ProductInput(iron_plate, 9),
            ProductInput(assembling_machine_1, -1),
            ],
        0.5,
        building=assembling_machine_3
        )

produce_assembling_machine_2 = Process(
        "assembling machine 2",
        [
            ProductInput(assembling_machine_1, 1),
            ProductInput(electronic_circuit, 3),
            ProductInput(iron_gear_wheel, 5),
            ProductInput(iron_plate, 9),
            ProductInput(assembling_machine_2, -1),
            ],
        0.5,
        building=assembling_machine_3
        )

produce_assembling_machine_3 = Process(
        "assembling machine 3",
        [
            ProductInput(assembling_machine_2, 2),
            ProductInput(speed_module_1, 4),
            ProductInput(assembling_machine_3, -1),
            ],
        0.5,
        building=assembling_machine_3
        )

produce_rail_signal = Process(
        "rail signal",
        [
            ProductInput(electronic_circuit, 1),
            ProductInput(iron_plate, 5),
            ProductInput(rail_signal, -1),
            ],
        0.5,
        building=assembling_machine_3
        )

produce_rail_chain_signal = Process(
        "rail chain signal",
        [
            ProductInput(electronic_circuit, 1),
            ProductInput(iron_plate, 5),
            ProductInput(rail_chain_signal, -1),
            ],
        0.5,
        building=assembling_machine_3
        )


produce_new_base_supplies = Process(
        "new base supplies",
        [
            ProductInput(stack_filter_inserter, 48),
            ProductInput(express_transport_belt, 200),
            ProductInput(rail, 100),
            ProductInput(rail_signal, 20),
            ProductInput(rail_chain_signal, 20),
            ProductInput(new_base_supplies, -1),
            ],
        0,
        )


production = Process("production", 
        [
            ProductInput(speed_module_3, 1 / 3),
            ProductInput(speed_module_3, 1 / 3),
            ProductInput(speed_module_3, 1 / 3),
            ProductInput(satellite_launch, 1),
            ProductInput(destroyer_capsule, 1 / 1),
            ProductInput(piercing_rounds_magazine, 1 / 1),
            ProductInput(science_pack_1, 10),
            ProductInput(science_pack_2, 10),
            ProductInput(science_pack_3, 10),
            ProductInput(military_science_pack, 10),
            ProductInput(production_science_pack, 10),
            ProductInput(high_tech_science_pack, 10),
            ProductInput(space_science_pack, 10),
            ProductInput(new_base_supplies, 1 / 30),
            ProductInput(artillery_shell, 10),
            ],
        60,
        )


#x.process_default = produce_x
#x.process_default = produce_x
#x.process_default = produce_x

rail_signal.process_default = produce_rail_signal
rail_chain_signal.process_default = produce_rail_chain_signal

assembling_machine_1.process_default = produce_assembling_machine_1
assembling_machine_2.process_default = produce_assembling_machine_2
assembling_machine_3.process_default = produce_assembling_machine_3
concrete.process_default = produce_concrete
nuclear_reactor.process_default = produce_nuclear_reactor
heat_exchanger.process_default = produce_heat_exchanger
steam_turbine.process_default = produce_steam_turbine
heat_energy.process_default = nuclear_power
steam_500.process_default = heat_exchanger_process
uranium_235.process_default = uranium_enrichment
uranium_238.process_default = uranium_processing
uranium_ore.process_default = mine_uranium_ore
uranium_fuel_cell.process_default = produce_uranium_fuel_cell
space_science_pack.process_default = produce_satellite_launch
high_tech_science_pack.process_default = produce_high_tech_science_pack
stone_brick.process_default = produce_stone_brick
production_science_pack.process_default = produce_production_science_pack
gun_turret.process_default = produce_gun_turret
grenade.process_default = produce_grenade
electric_furnace.process_default = produce_electric_furnace
electric_engine_unit.process_default = produce_electric_engine_unit
military_science_pack.process_default = produce_military_science_pack
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
stack_filter_inserter.process_default = produce_stack_filter_inserter

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

electrical_energy.process_default = steam_turbine_process

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

chemical_plant.process_default = produce_chemical_plant


