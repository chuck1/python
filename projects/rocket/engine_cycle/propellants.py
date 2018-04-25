
class Ethanol:
    def __init__(self):
        self.s = "Ethanol"
        self.M = 46.07

class Oxygen:
    def __init__(self):
        self.s = "O2"
        self.M = 16

class PropEthanolLOX:
    def __init__(self):
        self.f = Ethanol()
        self.o = Oxygen()
        
        # f / o
        self.molar_ratio = 1 / 3
        self.mass_ratio = self.molar_ratio * self.f.M / self.o.M

        self.h = 29.8e6 # J / kg


