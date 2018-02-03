from constants import *

import blueprints as bp
import blueprints.build_1
import blueprints.templates


class Subfactory:
    def __init__(self, factory, stations, stops_c, stops_f, count_x, count_y, buildings, bl):
        self.factory = factory

        self.stations = stations
        
        self.stops_c = stops_c
        self.stops_f = stops_f

        self.count_x = count_x
        self.count_y = count_y

        self.buildings = buildings
        self.bl = bl

    def blueprint(self):
        
        stop_blueprints = [bp.templates.train_stop(Constants.train_configuration.wagons, s.inserter_load_fraction(self.factory)) for s in self.stations]
        
        g = blueprints.build_1.subfactory(
                    blueprints.templates.assembling(), 
                    self.stops_c,
                    stop_blueprints,
                    self.count_y, 
                    self.count_x)

        b = blueprints.blueprint.Blueprint()
        b.entities.append(g)
        b.plot()
        
        #stops_x_1 = i_x / ips


    def width(self):
        return self.count_x * self.bl.tile_x

    def height(self):
        return self.count_y * self.bl.tile_y

