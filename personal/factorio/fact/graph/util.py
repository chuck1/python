from constants import *
from product import *

class ItemRate:
    def __init__(self, item, rate):
        self.item = item
        self.rate = rate

    def cargo_wagon_stops(self, route, ins_frac):
        if isinstance(self.item, Liquid):
            return 0
        
        # slots per second
        slots = abs(self.rate) / self.item.stack_size
        
        if route.slots() == 0:
            route.show()
            raise RuntimeError()
        
        wagon_capacity = slots / route.slots() * 40 * self.item.stack_size

        if ins_frac == 0:
            print('inserters for product {} {} ins_frac={}'.format(self.item.name, self.rate, ins_frac))
            return float("inf")
        
        # load/unload time
        t = wagon_capacity / (12 * Constants.inserter_rate * ins_frac)
        
        # inserter utilization
        utilization = t / (t + Constants.train_transition_time)
        
        # inserters
        i = self.rate / Constants.inserter_rate / utilization

        wagon_stops = i / Constants.inserters_per_wagon
        
        if math.isinf(wagon_stops):
            raise RuntimeError()

        #print("{:24} rate: {:8.2f} frac: {:8.2f} wagon cap: {:8.2f} stops: {:8.2f}".format(self.item.name, self.rate, ins_frac, wagon_capacity, wagon_stops))

        return wagon_stops

    def fluid_wagon_stops(self, route):
        
        if not isinstance(self.item, Liquid):
            return 0

        #Constants.fluid_wagon_pump_rate = 1000
        #Constants.pumps_per_wagon = 12
        #Constants.fluid_wagon_capacity = 25000

        # TODO consider if we were only partially draining or filling the tank
        
        t = Constants.fluid_wagon_capacity / (Constants.fluid_wagon_pump_rate * Constants.pumps_per_wagon)

        utilization = t / (t + Constants.train_transition_time)

        wagon_stops = self.rate / (Constants.fluid_wagon_pump_rate * Constants.pumps_per_wagon) / utilization

        return wagon_stops



