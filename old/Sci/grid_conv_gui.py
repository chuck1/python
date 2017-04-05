#!/usr/bin/env python
import os
import sys
import numpy as np

import pygtk

pygtk.require('2.0')
import gtk

modules_dir = os.environ["HOME"] + "/Programming/Python/Modules"
sys.path.append( modules_dir )

import Sci.gridconv as gc

class HelloWorld:

	# This is a callback function. The data arguments are ignored
	# in this example. More on callbacks below.
	def hello(self, widget, data=None):
		print "Hello World"
		n = np.zeros(3)
		y = np.zeros(3)
		
		s = None
		
		for i in range(3):	
			s = self.entry[i].get_text()
			if s:
				n[i] = float(s)
			else:
				print "empty string"
				return
		for i in range(3):
			s = self.entry[i].get_text()
			if s:
				y[i] = float(self.entry[i+3].get_text())
			else:
				print "empty string"
				return
	
		s = self.entry[6].get_text()
		if s:
			v = float(self.entry[6].get_text())
		else:
			print "empty string"
			return

		print v
		print n
		print y

		gc.grid_refinement(y,n,v,0)
	def delete_event(self, widget, event, data=None):
		# If you return FALSE in the "delete_event" signal handler,
		# GTK will emit the "destroy" signal. Returning TRUE means
		# you don't want the window to be destroyed.
		# This is useful for popping up 'are you sure you want to quit?'
		# type dialogs.
		print "delete event occurred"

		# Change FALSE to TRUE and the main window will not be destroyed
		# with a "delete_event".
		return False

	def destroy(self, widget, data=None):
		print "destroy signal occurred"
		gtk.main_quit()

	def __init__(self):
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.connect("delete_event", self.delete_event)
		self.window.connect("destroy", self.destroy)
		self.window.set_border_width(10)
		
		vbox = gtk.VBox(False,0)
		self.window.add(vbox)
		vbox.show()
		
		self.button = [None,None]

		self.button[0] = gtk.Button("Enter")
		self.button[0].connect("clicked", self.hello, None)
		vbox.pack_start(self.button[0], True, True, 0)
		self.button[0].show()
	
		self.button[1] = gtk.Button("Exit")
		self.button[1].connect_object("clicked", gtk.Widget.destroy, self.window)
		vbox.pack_start(self.button[1], True, True, 0)
		self.button[1].show()

		labels = ["n[0]","n[1]","n[2]","y[0]","y[1]","y[2]","v"];
		x = [pow(100,3),pow(150,3),pow(225,3),2.0,1.1,1.0,1.0]
		
		self.vbox = []
		self.entry = []
		for i in range(7):
			vb = gtk.VBox(False,0)
			vbox.pack_start(vb, True, True, 0)
			vb.show()
			
			l = gtk.Label(labels[i])
			vb.pack_start(l, True, True, 0)
			l.show()
			
			e = gtk.Entry(max=0)
			e.set_text("{0}".format(x[i]))
			vb.pack_start(e, True, True, 0)
			e.show()
			self.entry.append(e)
			
			self.vbox.append(vb)
		
		
		# and the window
		self.window.show()

	def main(self):
		# All PyGTK applications must have a gtk.main(). Control ends here
		# and waits for an event to occur (like a key press or mouse event).
		gtk.main()

# If the program is run directly or passed as an argument to the python
# interpreter then create a HelloWorld instance and show it
if __name__ == "__main__":
	hello = HelloWorld()
	
	hello.main()







