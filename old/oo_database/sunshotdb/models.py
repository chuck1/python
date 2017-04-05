import math
import inspect
import logging

import oodb

import sunshotdb

import Sci.Fluids

class FluidSettings:
    def __init__(self, string):
        if string == 'co2':
            self.qpp        = 1e6
            self.temp_in    = 773.15
            self.temp_out   = 923.15
        if string == 'ms1':
            self.qpp        = 4e6
            self.temp_in    = 573.15
            self.temp_out   = 873.15
            

class Design(oodb.Object):
    def __init__(self, i):
        super(Design, self).__init__(i)
        logging.info('Design.__init__')

    def resolve(self, db=None):
        logging.info('Design.resolve')
        try:
            fluid_str = self.get('fluid_str')
            self.fluid = Sci.Fluids.Fluid(fluid_str)
            self.fs = FluidSettings(fluid_str)
        except Exception as err:
            self.print_dict()
            logging.info('__dict__:')
            for k,v in self.__dict__.items():
                logging.info("{} {}".format(k,v))
            raise err
                
    def display(self):
        for k,v in self.__dict__.items():
            logging.info("{} {}".format(k,v))

    def Re(self):
        
        T = self.temp_avg()
        
        rho = self.fluid.get('density', T)
        mu = self.fluid.get('dynamic_viscosity', T)
        
        return rho * self.D_h() * self.v() / mu

    def temp_avg(self):
        return (self.fs.temp_in + self.fs.temp_out) / 2.0

    def v(self):
        rho = self.fluid.get('density', self.temp_avg())
        return self.mdot() / rho / (self.A_cs() * self.get('NT'))

    # total mass flow rate for device
    def mdot(self):
        dh = self.fluid.enthalpy_change(self.fs.temp_in, self.fs.temp_out)
        return self.fs.qpp * self.A_heated() / dh

    # 
    def A_heated(self):
        return self.get('width') * self.get('length')
    def test(self):
        print(self.get('width'))
        print(self.get('length'))
        print(self.get('Re'))

class Rectangular(Design):
    def __init__(self, i):
        super(Rectangular, self).__init__(i)

    ## the full width of the heated area
    # hidden by full design objects; this should be in Geo
    def width(self):
        return self.get('width_channel') + self.get('width_wall')
    
    def length(self):
        return self.get('length_channel')

    def D_h(self):
        
        P = 2.0 * (self.get('width_channel') + self.get('height_channel'))
        return 4 * self.A_cs() / P

    def NT(self):
        return (self.get('width') - self.get('width_channel')) / (self.get('width_channel') + self.get('width_wall')) + 1

    def A_cs(self):
        return self.get('width_channel') * self.get('height_channel')

    def test(self):
        super(Rectangular, self).test()
        self.get('width_channel')
        self.get('length_channel')
        self.get('width_wall')

class Circular(Design):
    def __init__(self, i):
        super(Circular, self).__init__(i)
    
    def D_h(self):
        return self.get('D')

    def NT(self):
        return (self.get('D') - self.get('width_channel')) / (self.get('width_channel') + self.get('width_wall')) + 1

    def A_cs(self):
        return math.pi * self.get('D')**2 / 4.0
    
    def test(self):
        self.get('D')
        self.get('width_wall')

class PinFin(Design):
    def __init__(self, i):
        Design.__init__(self, i)

    def length(self):
        return self.get('SL') * self.get('NL')
    def width(self):
        #if self.has('ST'):
        #    self.PT = self.get('ST') / self.get('D')
        #else:
        #    if self.has('PT'):
        #        self.ST = self.get('PT') * self.get('D')
        return self.get('ST') * self.get('NT') + 2.0 * self.get('SE')

    def NT(self):
        return self.get('width') / self.get('ST')
    def NL(self):
        return self.get('length') / self.get('SL')

    def foo(self):

        if not hasattr(self,'data'):
            print('doesnt have data')
            self.data = {}
        
    def ST(self):
        return self.get('PT') * self.get('D')
    def SL(self):
        if self.has('PL'):
            return self.get('PL') * self.get('D')
        else:
            PL = math.sqrt(3.0) / 2.0 * self.get('PT')
            return PL * self.get('D')
        

    def D_h(self):
        return self.get('D')

    def gap(self):
        return self.get('D') - self.get('ST')

    def A_cs(self):
        return math.pi * self.gap()**2 / 4.0

    def test(self):
        self.get('D')

        if self.has('ST'):
            self.data['PT'] = self.get('ST') / self.get('D')

        self.get('PT')

### Geo

class Geo(oodb.Object):
    def __init__(self, i, design_id):
        super(Geo, self).__init__(i)
        self.id = i
        self.design_id = design_id

    def resolve(self, db=None):
        db = db if db else oodb.DB
        #print(self.design_id)
        self.design = db.get_object(self.design_id)
    def test(self):
        pass

### Simulation

class Simulation(oodb.Object):
    def __init__(self, i, geo_id):
        super(Simulation, self).__init__(i)
        self.geo_id = geo_id

    def length(self):
        return self.geo.design.get('length')

    def receiver_efficiency(self):
        emis = 0.95

        T = self.get('temperature_heated_awa')
        
        radi = 5.67e-8 * 0.95 * (pow(T, 4) - pow(298.0, 4))
        
        conv = 15.0 * (T - 298.0)
        
        qpp = self.geo.design.fs.qpp
        
        return qpp * emis / (qpp + radi + conv)

    def resolve(self, db=None):
        logging.info("Simulation.resolve")
        db = db if db else oodb.DB
        self.geo = db.get_object(self.geo_id)

    def Re(self):
        return self.geo.design.Re()

    def pressure_drop(self):
        return self.get('pressure_inlet') - self.get('pressure_outlet')
    def test(self):

        #if self.has('temp_heated_awa'):
        #    self.data['temperature_heated_awa'] = self.get('temp_heated_awa')
        
        print(self.get('temperature_heated_awa'))
        print(self.get('receiver_efficiency'))

## Experiment

class HeatLossCurve(oodb.Object):
    def __init__(self, i, design_id):
        self.design_id = design_id
    def resolve(self, db=None):
        db = db if db else oodb.DB
        self.design = db.get_object(self.design_id)
    def Re(self):
        return self.design.Re()
    def test(self):
        pass

class Experiment(oodb.Object):
    def __init__(self, i, design_id):
        self.design_id = design_id
        self.heat_loss_curve = None
        self.heat_loss_curve_id = None
    def resolve(self, db=None):
        db = db if db else oodb.DB
        self.design = db.get_object(self.design_id)
        if self.heat_loss_curve_id:
            self.heat_loss_curve = db.get_object(self.heat_loss_curve_id)
    def length(self):
        return self.design.get('length')
    def pressure_drop(self):
        return self.get('pressure_inlet') - self.get('pressure_outlet')
    #def Re(self):
    #    return self.design.Re()
    def test(self):
        pass


