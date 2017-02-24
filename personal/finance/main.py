import numpy
import copy

class Loan(object):
    def __init__(self, pv, rate):
        self.pv = pv
        self.rate = rate
    def calc_pmt(self, nper):
        return numpy.pmt(self.rate, nper, self.pv)
        
    def calc_nper(self, pmt):
        return numpy.nper(self.rate, pmt, self.pv)

    def calc_fv(self, nper, pmt):
        return numpy.fv(self.rate, nper, pmt, self.pv)



l1 = Loan(-354000, 0.0425/12)
l2 = copy.copy(l1)
l3 = copy.copy(l1)
l4 = copy.copy(l1)

pmt1 = l1.calc_pmt(12*29)

print 'pmt', pmt1
print 'fv ', l1.calc_fv(12*17, pmt1)

nper = l1.calc_nper(pmt1 + 186)

print
print 'nper', nper/12
print 'fv  ', l2.calc_fv(12*17, pmt1 + 186)


pmt3 = l3.calc_pmt(12*17)

print
print 'pmt', pmt3, pmt3 - pmt1

l4.rate = .035/12
pmt4 = l4.calc_pmt(12*17)

print 'pmt', pmt4, pmt4 - pmt1


