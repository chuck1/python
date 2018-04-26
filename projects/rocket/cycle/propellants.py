from CoolProp.CoolProp import PropsSI

class Subcooled:
    def tank_density(self, p):
        return PropsSI("D", "P", p, "T", self.tank_temperature(p), self.s)

    def tank_temperature(self, p):
        return 293

class Saturated:
    def tank_density(self, p):
        return PropsSI("D", "P", p, "Q", 0, self.s)

    def tank_temperature(self, p):
        return PropsSI("T", "P", p, "Q", 0, self.s)

class Methane(Saturated):
    def __init__(self):
        self.s = "Methane"
        self.M = 16.04

class Ethanol(Subcooled):
    def __init__(self):
        self.s = "Ethanol"
        self.M = 46.07

class Oxygen(Saturated):
    def __init__(self):
        self.s = "O2"
        self.M = 16

class PropEthanolLOX:
    def __init__(self):
        self.f = Ethanol()
        self.o = Oxygen()

        # sea level
        self.v_e = 2786 # m / s
        
        # f / o
        self.molar_ratio = 1 / 3
        self.mass_ratio = self.molar_ratio * self.f.M / self.o.M

        self.h = 29.8e6 # J / kg

class PropMethalox:
    def __init__(self):
        self.f = Methane()
        self.o = Oxygen()

        # sea level
        self.v_e = 3034 # m / s
        
        # f / o
        self.molar_ratio = 1 / 2
        self.mass_ratio = self.molar_ratio * self.f.M / self.o.M

        self.h = 55.5e6 # J / kg


