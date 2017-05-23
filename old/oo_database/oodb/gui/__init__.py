import sys
from PyQt4 import Qt, QtGui, QtCore
import logging

#import oodb.gui.spreadsheet
#import oodb.gui.objectedit

from oodb.gui.Window import Window

import unit

def convert(s):
        try:
                return int(s)
        except:
                pass

        try:
                return float(s)
        except:
                pass

        try:
                e = eval(s)
                logging.info(e)
                return e
        except Exception as e:
                logging.info(e)
                logging.info(sys.exc_info())
                pass
        

        logging.info('str:',s)
        
        return s

class TableWidgetItem(QtGui.QTableWidgetItem):
	def __init__(self, value, editable = True):
		super(TableWidgetItem, self).__init__(str(value))

		self.value = value
		
		self.setEditable(editable)
		
	def setEditable(self, x):
		if x:
			f = self.flags()
			f |= 2
			self.setFlags(f)
		else:
			f = self.flags()
			f ^= 2
			self.setFlags(f)

	def handleChanged(self):
		pass

class TableWidgetItemRaw(TableWidgetItem):
    def __init__(self, field_name, value, obj):
        super(TableWidgetItemRaw, self).__init__(str(value))

        self.field_name = field_name
        self.value      = value
        self.obj        = obj

        self.first_change = True

    def handleChanged(self):
        if self.first_change:
                self.first_change = False
                return
        
        logging.info("{} {}".format(self,'handleChanged'))
        setattr(
            self.obj,
            self.field_name,
            convert(self.text()))

















        
