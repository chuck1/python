import math

class Radio(object):
    def power(self, d, E):
        #E = 1e-6

        # E = sqrt(30 * P) / d
        # E * d = sqrt(30 * P)
        # (E * d)**2 = 30 * P
        # P = (E * d)**2 / 30
        P = (E * d)**2 / 30.0

        return P

class Rocket(object):
    stages=list()
    def deltav(self):
        stages = list(self.stages)

        m_wet = sum([s.m_wet for s in stages])

        dv = 0

        while stages:
            s = stages.pop(0)

            m_dry = m_wet - s.m_wet + s.m_dry
            
            dv_temp = s.Isp * 9.81 * math.log(m_wet / m_dry)

            dv += dv_temp

            if 0:
                print "m_wet  ", m_wet
                print "m_dry  ", m_dry
                print "log    ", math.log(m_wet / m_dry)
                print "log    ", m_wet / m_dry
                print "Isp    ", s.Isp
            
            print "dv_temp", dv_temp

            m_wet -= s.m_wet

        return dv

class Stage(object):
    pass


def test1():
    r = Rocket()
    s1 = Stage()
    s2 = Stage()
    
    s1.Isp = 200.
    s1.m_wet = 80.0
    s1.m_dry = 3.0
    
    s2.Isp = 200.
    s2.m_wet = 30.0
    s2.m_dry = 2.0
    
    r.stages = [s1, s2]
    
    print r.deltav()
    
def test2():
    r = Rocket()
    s1 = Stage()
    
    s1.Isp = 200.
    s1.m_wet = 20.0
    s1.m_dry = 10.0
    
    r.stages = [s1]
    
    print r.deltav()
    



test1()


#radio = Radio()
#print radio.power(400e3, 5e-6)


