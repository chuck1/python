#!/usr/bin/env python
import os
import sys
import numpy as np

import pygtk

pygtk.require('2.0')
import gtk

def efficiency(T, q_abs, T_infr = 298.15, T_infc = 298.15, h_nat = 15.0, emiss = 0.95):
        sigma = 5.67 * pow(10,-8)

        q_rad = emiss * sigma * (pow(T,4) - pow(T_infr,4))
        q_conv = h_nat * (T - T_infc)

        # thermal
        eff_ther = q_abs / (q_abs + q_rad + q_conv)

        # receiver
        eff_recv = eff_ther * emiss

        return eff_ther, eff_recv, q_rad, q_conv

class HelloWorld:
        # This is a callback function. The data arguments are ignored
        # in this example. More on callbacks below.
        def hello(self, widget, data=None):
                n = [0]
                #for i in range(1):
                #	s = self.entry[i].get_text()
                #	if s:
                #		n[i] = float(s)
                #	else:
                #		print "empty string"
                #		return

                # get entries
                T = float(self.entry["T"].get_text())
                q = float(self.entry["q"].get_text())
                Tinfr = float(self.entry["Tinf r"].get_text())
                Tinfc = float(self.entry["Tinf c"].get_text())
                h = float(self.entry["h"].get_text())
                em = float(self.entry["em"].get_text())


                eff_ther, eff_recv, q_rad, q_con = efficiency(T, q, Tinfr, Tinfc, h, em)

                self.entry["eff th"].set_text("{0}".format(eff_ther))
                self.entry["eff re"].set_text("{0}".format(eff_recv))
                self.entry["q rad"].set_text("{0}".format(q_rad))
                self.entry["q con"].set_text("{0}".format(q_con))


        def delete_event(self, widget, event, data=None):
                # If you return FALSE in the "delete_event" signal handler,
                # GTK will emit the "destroy" signal. Returning TRUE means
                # you don't want the window to be destroyed.
                # This is useful for popping up 'are you sure you want to quit?'
                # type dialogs.
                print("delete event occurred")

                # Change FALSE to TRUE and the main window will not be destroyed
                # with a "delete_event".
                return False

        def destroy(self, widget, data=None):
                print("destroy signal occurred")
                gtk.main_quit()
        def label_text(self, vbox, nickname, label, value):
                vb = gtk.VBox(False,0)
                vbox.pack_start(vb, True, True, 0)
                vb.show()

                l = gtk.Label(label)
                vb.pack_start(l, True, True, 0)
                l.show()

                e = gtk.Entry(max=0)
                e.set_text("{0}".format(value))
                vb.pack_start(e, True, True, 0)
                e.show()

                self.entry[nickname] = e

                self.vbox.append(vb)

        
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


                self.vbox = []
                self.entry = {}

                self.label_text(vbox, "T", "temperature (K)", 0)
                self.label_text(vbox, "q", "flux (w/m2)", 0)

                self.label_text(vbox, "Tinf r", "T inf rad (K)", 298.15)
                self.label_text(vbox, "Tinf c", "T inf conv (K)", 298.15)
                self.label_text(vbox, "h", "h_nat (W/m2 K)", 15.0)
                self.label_text(vbox, "em", "emiss", 0.95)

                self.label_text(vbox, "eff th", "efficiency thermal", 0)
                self.label_text(vbox, "eff re", "efficiency receiver", 0)
                self.label_text(vbox, "q rad", "q rad", 0)
                self.label_text(vbox, "q con", "q conv", 0)
                for i in range(0):
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







