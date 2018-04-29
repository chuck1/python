import math

class TrainConfiguration:
    def __init__(self, loco_1, wagons, loco_2, speed, t_acc):
        self.loco_1, self.wagons, self.loco_2, self.speed = loco_1, wagons, loco_2, speed
        
        self.acc = speed / t_acc

        self.train_gap = 10
        
    def time_rest_to_distance(self, d):
        # d = 0.5 * a * t**2
        return math.sqrt(2 * d / self.acc)

    def cars(self):
        return self.loco_1 + self.wagons + self.loco_2
    
    def length(self):
        return self.cars() * 7 - 1

    def train_line_capacity(self):
        # trains per second per line
        return self.speed / (self.train_gap + self.length())

class TrainWaitingAreaEW:
    def __init__(self, n):
        self.n = n

    def width(self):
        w = math.sqrt(2) / 2 * (Constants.train_turn_radius * 2 + Constants.train_configuration.length())
        w = math.ceil(w)
        w += w % 2
        return w

class Constants:
    inserter_rate = 27.7

    train_transition_time = 20
    locomotives_per_train = 4
    train_configuration = TrainConfiguration(2, 8, 2, 80.3, 21)
    inserters_per_wagon = 12
    cargo_wagon_slots = 40
    train_turn_radius = 7
    
    fluid_wagon_capacity = 25000
    fluid_wagon_pump_rate = 1000
    pumps_per_wagon = 12

    logistic_robot_speed = 3 * (1 + 2.4 + 0.65 * 5)
    logistic_robot_cargo_size = 4

    express_belt_throughput = 40


    

