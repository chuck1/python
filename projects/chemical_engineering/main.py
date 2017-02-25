
import scipy.optimize

molar_masses = {
        'H':   1.0,
        'O':  16.0,
        'Na': 23.0,
        'S':  32.0,
        'Cl': 35.453,
        }

class Chemical(object):
    def __init__(self, formula, cost=0):
        self.formula = formula
        self.cost = cost
    def molar_mass(self):
        mass = 0
        for k,v in self.formula.items():
            mass += molar_masses[k] * v
        return mass


class Reaction(object):
    def __init__(self, chemicals):
        self.chemicals = chemicals
    def cost(self):
        cost = 0
        for c in self.chemicals:
            if c[1] > 0:
                cost += c[1] * c[0].molar_mass() * c[0].cost
        return cost

def convert_solution_cost(concentration, volume, cost):
    """
    output cost per gram

    volume in ml
    concentration by weight

    cost     | vol soln  | mass soln
             |           | 
    vol soln | mass soln | mass chemical

    """
    c = cost / volume * 1.0 / concentration
    return c

############################################

sodium_metabisulfite = Chemical({'Na':2, 'S':2, 'O':5})
sodium_chloride = Chemical({'Na':1, 'Cl':1})
hydrogen_chloride = Chemical({'H':1, 'Cl':1})
sulfur_dioxide = Chemical({'S':1, 'O':2})
water = Chemical({'H':2, 'O':1})

sulfur = Chemical(
        {'S':1},
        3.0 / 454.0
        )

oxygen = Chemical({'O':2})

hydrogen_peroxide = Chemical(
        {'H':2, 'O':2},
        convert_solution_cost(0.03, 473.0, 1.09)
        )

sulfuric_acid = Chemical(
        {'H':2, 'S':1, 'O':4}
        )

############################################

r1 = Reaction([
        [sodium_metabisulfite,1],
        [hydrogen_chloride,2],
        [sodium_chloride,-2],
        [water,-1],
        [sulfur_dioxide,-2]
        ])

r2 = Reaction([
        [oxygen,1],
        [sulfur,1],
        [sulfur_dioxide,-1]
        ])

r3 = Reaction([
        [hydrogen_peroxide,1],
        [sulfur_dioxide,1],
        [sulfuric_acid,-1],
        ])

############################################

print r3.cost() / sulfuric_acid.molar_mass()



