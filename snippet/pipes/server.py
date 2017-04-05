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

name_srv_w = "/tmp/pipes_example_srv_w"
name_cli_w = "/tmp/pipes_example_cli_w"

def cli_read():
    with open(name_srv_w, 'rb') as f:
        return f.read().decode('utf-8')

def cli_write(s):
    with open(name_cli_w, 'wb') as f:
        f.write(s.encode('utf-8'))

class Stop(Exception): pass

class Server(object):
    def __init__(self):
        #self.fifo_name_srv_w = "/tmp/python_spreadsheet_srv_w"
        #self.fifo_name_cli_w = "/tmp/python_spreadsheet_cli_w"
        self.fifo_name_srv_w = name_srv_w
        self.fifo_name_cli_w = name_cli_w

        try:
            os.remove(self.fifo_name_srv_w)
            print(self.fifo_name_srv_w, "removed")
            os.remove(self.fifo_name_cli_w)
            print(self.fifo_name_cli_w, "removed")
        except Exception as e:
            print(e)
            pass

        try:
            um = os.umask(000)
            print("umask was",um)
            #os.mkfifo(self.fifo_name_srv_w, 0777)
            os.mkfifo(self.fifo_name_srv_w, 0o777)
            print(self.fifo_name_srv_w, "created")
            #os.mkfifo(self.fifo_name_cli_w, 0777)
            os.mkfifo(self.fifo_name_cli_w, 0o777)
            print(self.fifo_name_cli_w, "created")
            os.umask(um)
        except OSError:
            pass

    def write(self, s):
        with open(self.fifo_name_srv_w, 'wb') as f:
            f.write(s)
    
    def read(self):
        with open(self.fifo_name_cli_w, 'rb') as f:
            return f.read()

    def blocking_read(self):
        s = self.read()

        if s == 'stop': raise Stop()

        print('recieved',s)

        self.write(s)

    def run(self):
        
        t = datetime.datetime.now() + datetime.timedelta(minutes=1)
        
        while True:
            try:
                print("waiting for data")
                self.blocking_read()
            except Stop:
                break
            except IOError:
                print("got ioerror")
                break

if __name__ == '__main__':
    
    #parser = argparse.ArgumentParser()
    #parser.add_argument('-b', action='store_true')
    
    #args = parser.parse_args()
    
    server = Server()
    
    server.run()

