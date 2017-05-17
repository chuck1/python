import math

from orbit import *

G = 6.674e-11
TWO_PI = 2 * math.pi
HALF_PI = 0.5 * math.pi



class CelestialBody:
    def __init__(self, mass, radius, siderealRotation, orbit, atmPressure = 0, atmScaleHeight = 0):
        self.mass = mass
        self.radius = radius
        self.orbit = orbit
        self.atmScaleHeight = atmScaleHeight
        
        
        self.gravitationalParameter = G * self.mass
    
        self.sphereOfInfluence = self.orbit.semiMajorAxis * math.pow(self.mass / self.orbit.referenceBody.mass, 0.4) if self.orbit else None
        
        self.atmRadius = -math.log(1e-6) * self.atmScaleHeight + self.radius
  
    def circularOrbitVelocity(self, altitude):
        return math.sqrt(self.gravitationalParameter / (altitude + self.radius))

    def siderealTimeAt(self, longitude, time):

        result = ((time / self.siderealRotation) * TWO_PI + HALF_PI + longitude) % TWO_PI
        
        return (result + TWO_PI) if (result < 0) else result
  
    def name():
        for k, v in CelestialBodies.items():
            if v == this:
                return k
  
    def children():
        for k, v in CelestialBodies.items():
            if v.orbit.referenceBody == this:
                yield v



CelestialBodies = {}
CelestialBodies['Kerbol'] = Kerbol = CelestialBody(1.756567e+28, 2.616e+08, 432000, None)
CelestialBodies['Moho'] = Moho = CelestialBody(2.5263617e21, 250000, 1210000, Orbit(Kerbol, 5263138304, 0.2, 7.0, 70.0, 15.0, 3.14))
CelestialBodies['Eve'] = Eve = CelestialBody(1.2244127e23, 700000, 80500, Orbit(Kerbol, 9832684544, 0.01, 2.1, 15.0, 0, 3.14), 5, 7000)
CelestialBodies['Gilly'] = Gilly = CelestialBody(1.2420512e17, 13000, 28255, Orbit(Eve, 31500000, 0.55, 12.0, 80.0, 10.0, 0.9))
CelestialBodies['Kerbin'] = Kerbin = CelestialBody(5.2915793e22, 600000, 21600, Orbit(Kerbol, 13599840256, 0.0, 0, 0, 0, 3.14), 1, 5000)
CelestialBodies['Mun'] = Mun = CelestialBody(9.7600236e20, 200000, 138984.38, Orbit(Kerbin, 12000000, 0.0, 0, 0, 0, 1.7))
CelestialBodies['Minmus'] = Minmus = CelestialBody(2.6457897e19, 60000, 40400, Orbit(Kerbin, 47000000, 0.0, 6.0, 78.0, 38.0, 0.9))
CelestialBodies['Duna'] = Duna = CelestialBody(4.5154812e21, 320000, 65517.859, Orbit(Kerbol, 20726155264, 0.051, 0.06, 135.5, 0, 3.14), 0.2, 3000)
CelestialBodies['Ike'] = Ike = CelestialBody(2.7821949e20, 130000, 65517.862, Orbit(Duna, 3200000, 0.03, 0.2, 0, 0, 1.7))
CelestialBodies['Dres'] = Dres = CelestialBody(3.2191322e20, 138000, 34800, Orbit(Kerbol, 40839348203, 0.145, 5.0, 280.0, 90.0, 3.14))
CelestialBodies['Jool'] = Jool = CelestialBody(4.2332635e24, 6000000, 36000, Orbit(Kerbol, 68773560320, 0.05, 1.304, 52.0, 0, 0.1), 15, 10000)
CelestialBodies['Laythe'] = Laythe = CelestialBody(2.9397663e22, 500000, 52980.879, Orbit(Jool, 27184000, 0, 0, 0, 0, 3.14), 0.8, 4000)
CelestialBodies['Vall'] = Vall = CelestialBody(3.1088028e21, 300000, 105962.09, Orbit(Jool, 43152000, 0, 0, 0, 0, 0.9))
CelestialBodies['Tylo'] = Tylo = CelestialBody(4.2332635e22, 600000, 211926.36, Orbit(Jool, 68500000, 0, 0.025, 0, 0, 3.14))
CelestialBodies['Bop'] = Bop = CelestialBody(3.7261536e19, 65000, 544507.4, Orbit(Jool, 128500000, 0.235, 15.0, 10.0, 25.0, 0.9))
CelestialBodies['Pol'] = Pol = CelestialBody(1.0813636e19, 44000, 901902.62, Orbit(Jool, 179890000, 0.17085, 4.25, 2.0, 15.0, 0.9))
CelestialBodies['Eeloo'] = Eeloo = CelestialBody(1.1149358e21, 210000, 19460, Orbit(Kerbol, 90118820000, 0.26, 6.15, 50.0, 260.0, 3.14))














