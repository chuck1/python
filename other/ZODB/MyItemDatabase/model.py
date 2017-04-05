
import persistent

class Model(persistent.Persistent):
    def _serialize(self):
        print type(self).__name__
    
        root = etree.Element(type(self).__name__)

        for s in dir(self):
            if s[0] == "_":
                continue
            else:
                print "  {}".format(s)
                child = etree.SubElement(root, s)
                child.text = getattr(self, s)

        print(etree.tostring(root, pretty_print=True))

class Item(Model):
    def __init__(self):
        self.itemNumber = None

    def __eq__(self, other):
        return True

class RefrigerationItem(Item):
    def __eq__(self, other):
        return super(RefrigerationItem, self).__eq__(other)

class ExpansionValve(RefrigerationItem):
    def __eq__(self, other):
        return super(ExpansionValve, self).__eq__(other)

class ElectronicExpansionValve(ExpansionValve):
    def __eq__(self, other):
        print "ElectronicExpansionValve.__eq__"

        if not isinstance(other, ElectronicExpansionValve): return False

        if not(self.pipeConnectionInlet == other.pipeConnectionInlet): return False
        if not(self.pipeConnectionOutlet == other.pipeConnectionOutlet): return False

        return super(ElectronicExpansionValve, self).__eq__(other)

class ElectronicExpansionValveSporlan(ElectronicExpansionValve):
    def __eq__(self, other):
        print "ElectronicExpansionValveSporlan.__eq__"

        if not isinstance(other, ElectronicExpansionValveSporlan): return False
        
        return super(ElectronicExpansionValveSporlan, self).__eq__(other)



