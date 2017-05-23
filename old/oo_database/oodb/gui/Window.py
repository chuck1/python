import sys
import numpy as np
from PyQt4 import QtGui, QtCore
import pylab as pl

class Window(QtGui.QWidget):
	def __init__(self):
		super(Window, self).__init__()

		self.setStyleSheet('font-size: 11pt; font-family: Courier;')

		