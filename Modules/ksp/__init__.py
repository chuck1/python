import math

class Orbit(object):
    def a(self):
        return (self.apoapsis + self.periapsis) / 2.0

class Body(object):
    pass

sun = Body()
sun.mu = 1.1723328E18

kerbin = Body()
kerbin.obt = Orbit()
kerbin.obt.body      = sun
kerbin.obt.apoapsis  = 13599840256
kerbin.obt.periapsis = 13599840256

duna = Body()
duna.obt = Orbit()
duna.obt.body      = sun
duna.obt.apoapsis  = 21783189163
duna.obt.periapsis = 19669121365

mun = Body()
mun.radius = 200000
mun.mu = 6.5138398E10
mun.obt = Orbit()
mun.obt.body      = kerbin
mun.obt.apoapsis  = 12000000
mun.obt.periapsis = 12000000

def circle_to_ellipse(body, r1, r2):
    tmp0 = math.sqrt(2.0 * r2 / (r1 + r2)) - 1.0
    return math.sqrt(body.mu / r1) * tmp0


class PlanetTransfer(object):
    def __init__(self, b1, b2):
        self.b1 = b1
        self.b2 = b2
        
    def calc(self):
        
        self.t = math.pi * math.sqrt(
                (self.b1.obt.a() + self.b2.obt.a())**3 / (8 * sun.mu))

        tmp0 = math.sqrt(sun.mu / self.b2.obt.a())

        self.phase = 180 / math.pi * (
                math.pi - tmp0 * self.t / self.b2.obt.a())

    def __str__(self):
        ret  = "t     {}\n".format(self.t)
        ret += "phase {}".format(self.phase)
        return ret






