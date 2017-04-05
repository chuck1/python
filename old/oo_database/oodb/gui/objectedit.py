import sys
import numpy as np
from PyQt4 import QtGui, QtCore
import pylab as pl

import oodb
import oodb.gui


class Table(QtGui.QTableWidget):
    def __init__(self, parent):
        super(Table, self).__init__(parent)

        self.itemChanged.connect(self.handleItemChanged)

    def refresh(self):
        
        d = self.parent().obj.__dict__
        
        self.setRowCount(len(d))
        self.setColumnCount(2)

        r = 0
        for k,v in d.items():
            # key
            i = oodb.gui.TableWidgetItem(k)
            i.setEditable(False)
            
            self.setItem(r,0,i)

            # value
            i = oodb.gui.TableWidgetItemRaw(k, v, self.parent().obj)

            if k == 'id':
                i.setEditable(False)

            i.setToolTip(str(type(v)))

            self.setItem(r,1,i)
            
            r += 1

    def handleItemChanged(self, item):
        item.handleChanged()


class Window(oodb.gui.Window):
    def __init__(self, obj):
        super(Window, self).__init__()
        
        print(self,obj)
        
        self.obj = obj

        self.createLayout()
        self.show()
        
    def createLayout(self):

        self.layout = QtGui.QVBoxLayout()

        self.setLayout(self.layout)

        self.table = Table(self)
        self.table.refresh()
        
        self.layout.addWidget(self.table)

        
