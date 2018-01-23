
from processes import *

def output_intermediate(process):
    for i in process.inputs:
        if i.q < 0:
            if not isinstance(i.product, IntermediateProduct):
                return False
    return True


def apply_modules():
    for p in globals().values():
        if not isinstance(p, Process): continue
        
        if p.building is None:
            #raise RuntimeError('Process {} does not have a building'.format(p.name))
            print('Process {} does not have a building'.format(p.name))
            continue
        
        if p.building.module_slots is None:
            raise RuntimeError('Building {} does not have module_slots defined'.format(p.building.name))

        if p.building.module_slots == 0:
            continue
        
        if output_intermediate(p):
            p.modules = [ProductivityModule3(p.building.module_slots), SpeedModule3(3)]
        else:
            p.modules = [SpeedModule3(p.building.module_slots + 3)]



