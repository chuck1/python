import math

class ProductInput:
    def __init__(self, product, q, lanes=None):
        self.product = product
        # qantity
        self.q = q
        # number of dedicated lanes for input
        self.lanes = lanes

    def mul(self, x):
        return ProductInput(self.product, self.q * x, self.lanes)

    def __str__(self):
        #if self.product.process_default.t is None:
        return "\t{:32} {:12.2f}".format(self.product.name, self.q)
        #else:
        #    b = -self.buildings()
        #    return "\t{:32} {:12.2f} {:12.2f}".format(self.product.name, self.q, b)
    
    def buildings(self):
        return self.product.process_default.buildings(self.product, self.q)

    def site_analysis(self):

        b = -self.buildings()

        b_row = self.product.production_building_row_length()
        
        rows = b / b_row

        belt_lanes = self.product.belt_lanes()

       
        # assuming assembly building or electric furance for now

        # width in tiles of row
        # assume inserters on both sides
        width = 3 + 2 + belt_lanes / 2
 
        width_total = rows * width
       
        cargo_wagon_slots = 40
        
        cargo_wagon_capacity = cargo_wagon_slots * self.product.stack_size
        
        wagons_per_second = self.q / cargo_wagon_capacity
        

        # need to run tests to get these values
        train_route_duration = 180


        #wagons_per_train = train_period * wagons_per_second
        wagons_per_train = 4
        train_period = wagons_per_train / wagons_per_second

        trains = train_route_duration / train_period

        print('rows                {:6}'.format(math.ceil(rows)))
        print('belt lanes          {:6}'.format(belt_lanes))
        print('width               {:6.1f}'.format(width))
        print('width_total (tiles) {:6.1f}'.format(width_total))
        print('width_total (chunk) {:6.1f}'.format(width_total / 32))
        print('cargo wagon capacity', cargo_wagon_capacity)
        print('wagons per second   ', wagons_per_second)
        print('wagon period (s)    ', 1 / wagons_per_second)
        print('wagons per train    ', wagons_per_train)
        print('wagons per train    ', math.ceil(wagons_per_train))

        
        print('trains              ', math.ceil(trains))

       












