
class Compressor:
    def __init__(self,
            t_in,
            p_in,
            mdot_in,
            eta,
            ratio):
        self.t_in = t_in
        self.p_in = p_in
        self.mdot_in = mdot_in
        self.eta = eta
        self.ratio = ratio
        
class Turbine:
    def __init__(self,
            eta,
            ratio):
        self.eta = eta
        self.ratio = ratio
    
    def _delta_hdot(self):
        return cp * (self.t_out - self.t_in)
    
    
    delta_hdot = property(_delta_hdot)
    
    def work(self):
        return self.delta_hdot


if __name__ == '__main__':

    cp = 1000

    turb2 = Turbine(0.75, 3.2)
    
    print "P = {}".format(turb2.work())




