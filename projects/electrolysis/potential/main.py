import matplotlib.pyplot as plt
import copy
from fractions import gcd
import math
import numpy

R = 8.314
F = 9.649E4
T = 273.15 + 25

class Reaction(object):
    def __init__(self, r, p, E, n):
        self.r = r
        self.p = p
        self.E = E
        self.n = n

    def reverse(self):
        self.r, self.p = self.p, self.r
        self.E = -self.E

srp = {
        'Al' :Reaction([['Al3+',1], ['e-',3]],       [['Al',1]], -1.66, 3),
        'Zn' :Reaction([['Zn2+',1], ['e-',2]],       [['Zn',1]], -0.76, 2),
        'Cu' :Reaction([['Cu2+',1], ['e-',2]],       [['Cu',1]],  0.34, 2),
        'H2' :Reaction([['H+',2], ['e-',2]],         [['H2',1]],  0,    2),
        'H2O':Reaction([['O2',1], ['H+',4],['e-',4]],[['H2O',2]], 1.23, 4),
        'Cl-':Reaction([['Cl2',1],['e-',2]],         [['Cl-',2]], 1.36, 2),
        }

ph = numpy.linspace(0, 14, 100)
ph = 0

concentrations = {
        'H2O':  1.0,
        'H+':   numpy.power(10, -ph),
        'Zn2+':  1.0,
        'Zn':  1.0,
        'Cl-':  1.0,
        'O2':   1.0,
        'H2':   1.0,
        'Cl2':  1.0,
        }

def chem_mul(r, p, m):

    for a in r:
        a[1] *= m

    for a in p:
        a[1] *= m

def reaction_mul(reaction, m):

    for a in reaction.r:
        a[1] *= m

    for a in reaction.p:
        a[1] *= m

    reaction.n *= m

def list_gcd(r, p):
    l = r + p
    for a in l:
        for b in l:
            yield gcd(a[1], b[1])

def reduce(reactants, products):
    
    d = min(list_gcd(reactants, products))

    if d == 1: return

    #print "reduce by",d
    
    for a in reactants:
        a[1] /= d

    for b in products:
        b[1] /= d

def elim(reactants, products):

    #balance(reactants, products)

    for a in reactants:

        if a[0] == 'e-': continue

        if a in products:
            reactants.remove(a)
            products.remove(a)
            return True

    return False

def reaction_sum(r, o):
    
    r = copy.deepcopy(r)
    o = copy.deepcopy(o)

    mr = o.n / gcd(o.n, r.n)
    mo = r.n / gcd(o.n, r.n)
    
    chem_mul(r.r, r.p, mr)
    chem_mul(o.r, o.p, mo)

    reactants = list(r.r) + list(o.p)
    products =  list(r.p) + list(o.r)

    while elim(reactants, products): pass
   
    #reduce(reactants, products)
   
    #while True:
    #    while elim(reactants, products): pass
    #    balance(reactants, products)
    #    if elim(reactants, products): continue
    #    break

    return reactants, products

def chem_str(l):
    
    m = []
    for r in l:
        if r[1] == 1:
            m.append(r[0])
        else:
            m.append("{} {}".format(r[1],r[0]))

    return " + ".join(m)

def Nernst(Q, n):
    return R * T / n / F * numpy.log(Q)

class Cell(object):

    def __init__(self, half_reactions, cathode, anode):
        self.half_reactions = half_reactions
        self.cathode = cathode
        self.anode = anode

    def concentration(self, s):

        try:
            return concentrations[s]
        except: pass

        return None

    def potential_half(self, reaction):


        reactants = reaction.r
        products = reaction.p
        
        if 0:
    
            Qreactants = 1
            for r in reactants:
                if r[0] == 'e-': continue
                
                C = self.concentration(r[0])
                
                if C is None:
                    raise Exception("concentraiton of {} is unknown", r[0])
                
                #print "concentration of {}: {}".format(r[0], C)
    
                Qreactants *= C**r[1]
    
            Qproducts = 1
            for p in products:
                if p[0] == 'e-': continue
                
                C = self.concentration(p[0])
                
                if C is None:
                    raise Exception("concentraiton of {} is unknown", p[0])
                
                #print "concentration of {}: {}".format(p[0], C)
                
                Qproducts *= C**r[1]
    
            Q = Qproducts / Qreactants
    
            n = reaction.n
    
            nernst = Nernst(Q, n)
    

        E0 = reaction.E

        E = E0

        #print "n     ",n
        #print "Q     ",Q
        #print "nernst",nernst
        print "           {:32} -> {:32} E0={:8}".format(chem_str(reactants), chem_str(products), E0)

        return E0

    def potential(self, red, oxi):
        
        reaction_r = copy.deepcopy(srp[red])
        reaction_o = copy.deepcopy(srp[oxi])
        
        reactants, products = reaction_sum(srp[red], srp[oxi])
        
        n_r = srp[red].n
        n_o = srp[oxi].n
        
        n = n_r * n_o / gcd(n_o, n_r)
        
        reaction_mul(reaction_r, n / n_r)
        reaction_mul(reaction_o, n / n_o)
        
        print

        E_r = self.potential_half(reaction_r)
        reaction_o.reverse()
        E_o = self.potential_half(reaction_o)
 
        E = E_r + E_o

        print "           {:32} -> {:32} E0={:8}".format(chem_str(reactants), chem_str(products), E)
 
   
        return E
    
    
    def cell_potential(self):

        r0 = None
        o0 = None
        E0 = 0
    
        for r in self.half_reactions:
            for o in self.half_reactions:
                if r == o: continue
    
                E = self.potential(r, o)

                if E is None: continue
    
                if r0 is None:
                    r0 = r
                    o0 = o
                    E0 = E
                elif E < 0:
                    if E > E0:
                        r0 = r
                        o0 = o
                        E0 = E

        print "reduction: {:32} -> {:32} E0={:8}".format(chem_str(srp[r0].r), chem_str(srp[r0].p), srp[r0].E)
        print "oxidation: {:32} -> {:32} E0={:8}".format(chem_str(srp[o0].r), chem_str(srp[o0].p), -srp[o0].E)
    
        reactants, products = reaction_sum(srp[r0], srp[o0])
    
        print
        print "           {:32} -> {:32} E0={:8}".format(chem_str(reactants), chem_str(products), E0)
    
    def plot(self):

        for r in self.half_reactions:
            E = self.potential_half(srp[r])
            
            #print numpy.shape(ph), numpy.shape(E)
            
            if numpy.shape(E) == ():
                plt.plot(ph, numpy.ones(numpy.shape(ph)) * E)
            else:
                plt.plot(ph, E)

        plt.show()

##############################

#cell = Cell(['H2', 'H2O', 'Cl-'], 'Al', 'Zn')
cell = Cell(['H2', 'H2O', 'Zn', 'Cu'], 'Al', 'Zn')

cell.cell_potential()

#cell.plot()












