
class TrainConfiguration:
    def __init__(self, loco_1, wagons, loco_2, speed, t_acc):
        self.loco_1, self.wagons, self.loco_2, self.speed = loco_1, wagons, loco_2, speed
        
        self.acc = speed / t_acc
        
    def time_rest_to_distance(self, d):
        # d = 0.5 * a * t**2
        return math.sqrt(2 * d / self.acc)

    def cars(self):
        return self.loco_1 + self.wagons + self.loco_2
    
    def length(self):
        return self.cars() * 7 - 1

class Constants:
    inserter_rate = 27.7

    train_transition_time = 20
    locomotives_per_train = 4
    train_gap = 10
    train_configuration = TrainConfiguration(2, 8, 2, 80.3, 21)

    @classmethod
    def train_line_capacity(self):
        # trains per second
        c = self.train_configuration
        return c.speed / (self.train_gap + c.length())

    

