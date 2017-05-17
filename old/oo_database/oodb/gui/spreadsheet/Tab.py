import sys
import numpy as np
from PyQt4 import QtGui, QtCore
import pylab as pl

import logging
import argparse

import oodb

from oodb.gui.spreadsheet.Table import Table

class TabLayout(QtGui.QVBoxLayout):
        def __init__(self, parent):
                super(TabLayout, self).__init__(parent)

class Tab(QtGui.QWidget):
        def __init__(self, parent, s0, s1):
                super(Tab, self).__init__(parent)

                self.s0 = s0
                self.s1 = s1

                self.w = [[300,100,100],[600],[600]]
                self.h = [60,60,600]

                #self.db = oodb.Database()

                #self.widget = QtGui.QWidget(self)

                self.layout = TabLayout(self)

                self.setLayout(self.layout)

                self.createGeneratorTextBox()
                self.createTable()

        def resizeEvent(self, e):
                w = e.size().width()
                h = e.size().height()
                logging.info("{} {} {}".format(self, w, h))
        
                #self.tb2.resize(w, self.h[1])
                
                #self.tab.resize(w, h - sum(self.h[:2]))
                
        def createGeneratorTextBox(self):

                # grid
                grid = QtGui.QGridLayout(self)
                self.layout.addLayout(grid)

                # LineEdit filters
                lab = QtGui.QLabel("filters")
                grid.addWidget(lab, 0, 0)
                
                self.le_filters = QtGui.QLineEdit(self)
                grid.addWidget(self.le_filters, 0, 1)
                self.le_filters.resize(300, 60)
                self.le_filters.show()
                
                # LineEdit objtype
                lab = QtGui.QLabel("type")
                grid.addWidget(lab, 1, 0)
                
                self.le_objtype = QtGui.QLineEdit(self)
                grid.addWidget(self.le_objtype, 1, 1)
                self.le_objtype.resize(300, 60)
                self.le_objtype.show()
                
                # LineEdit tests
                lab = QtGui.QLabel("tests")
                grid.addWidget(lab, 2, 0)
                
                self.le_tests = QtGui.QLineEdit(self)
                grid.addWidget(self.le_tests, 2, 1)
                self.le_tests.resize(300, 60)
                self.le_tests.show()
                
                # second


                
                self.text_fields = QtGui.QTextEdit(self.s1, self)
                
                #self.putInSlot(self.tb2, 0, 1)
                self.layout.addWidget(self.text_fields, 1)
                
                self.text_fields.show()
                
        def get_objtype(self):
            text = self.le_objtype.text()
            if text:
                e = eval(text)
                return e
            else:
                return None

        def get_filters(self):
            text = self.le_filters.text()
            if text:
                e = eval(text)
                return e
            else:
                return {}

        def get_tests(self):
            text = self.le_tests.text()
            if text:
                e = eval(text)
                return e
            else:
                return []
        
        

        def createTable(self):
                
                self.table = Table(self)

                self.table.refresh()

                #self.putInSlot(self.tab, 0, 2)
                self.layout.addWidget(self.table, 5)
                
                self.table.show()


        def plot(self):
                self.table.plot()

