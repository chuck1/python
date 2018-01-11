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
        train_period = 30
        train_route_duration = 90


        wagons_per_train = train_period * wagons_per_second

        trains = train_route_duration / train_period

        print('rows                ', rows)
        print('rows                ', math.ceil(rows))
        print('belt lanes          ', belt_lanes)
        print('width               ', width)
        print('width_total (tiles) ', width_total)
        print('width_total (chunk) ', width_total / 32)
        print('cargo wagon capacity', cargo_wagon_capacity)
        print('wagons per second   ', wagons_per_second)
        print('wagon period (s)    ', 1 / wagons_per_second)
        print('wagons per train    ', wagons_per_train)
        print('wagons per train    ', math.ceil(wagons_per_train))
        print('trains              ', trains)

       












