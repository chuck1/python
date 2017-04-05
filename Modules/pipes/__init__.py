#!/usr/bin/env python3

import os
import array
import xml.etree.ElementTree as et
import pickle
import re
import numpy as np
import struct
import signal
import datetime
import random
import sys
import argparse

#name_srv_w = "/tmp/pipes_example_srv_w"
#name_cli_w = "/tmp/pipes_example_cli_w"

class Stop(Exception): pass

class Node(object):
    
    def write(self, b):
        with open(self.pipe_w, 'wb') as f:
            f.write(b)
    
    def read(self):
        with open(self.pipe_r, 'rb') as f:
            return f.read()

class Client(Node):
    def __init__(self, name_srv_w, name_cli_w):
        self.pipe_w = name_cli_w
        self.pipe_r = name_srv_w

class Server(Node):
    def __init__(self, name_srv_w, name_cli_w):
        self.pipe_w = name_srv_w
        self.pipe_r = name_cli_w

        try:
            os.remove(name_srv_w)
            print(name_srv_w, "removed")
            os.remove(name_cli_w)
            print(name_cli_w, "removed")
        except Exception as e:
            print(e)
            pass

        try:
            um = os.umask(000)
            print("umask was",um)
            #os.mkfifo(name_srv_w, 0777)
            os.mkfifo(name_srv_w, 0o777)
            print(name_srv_w, "created")
            #os.mkfifo(name_cli_w, 0777)
            os.mkfifo(name_cli_w, 0o777)
            print(name_cli_w, "created")
            os.umask(um)
        except OSError:
            pass

    """
    overload this function
    s is the receieved message
    raise a Stop object to break the server loop
    """
    def do_read(self, s):
        pass

    def run(self):
        
        t = datetime.datetime.now() + datetime.timedelta(minutes=1)
        
        while True:
            try:
                self.do_read(self.read())
            except Stop:
                break
            except IOError:
                print("got ioerror")
                break


