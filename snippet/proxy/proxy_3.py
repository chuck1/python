#!/usr/bin/python
# This is a simple port-forward / proxy, written using only the default python
# library. If you want to make a suggestion or fix something you can contact-me
# at voorloop_at_gmail.com
# Distributed over IDC(I Don't Care) license
import socket
import select
import time
import sys

# Changing the buffer_size and delay, you can improve the speed and bandwidth.
# But when buffer get to high or delay go too down, you can broke things
buffer_size = 4096
delay = 0.0001

class Forward:
    def __init__(self):
        self.forward = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self, host, port):
        try:
            self.forward.connect((host, port))
            return self.forward
        except Exception, e:
            print e
            return False

class TheServer:
    input_list = []
    channel = {}

    def __init__(self, host, port, whost, wport):
        # no accept server
        #self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #self.server.bind((host, port))
        #self.server.listen(200)

        self.host = host
        self.port = port

        print "connect to p2"
        self.forward = Forward().start(whost, wport)
        self.input_list.append(self.forward)

    def main_loop(self):
        #self.input_list.append(self.server)
        while 1:
            time.sleep(delay)
            ss = select.select
            inputready, outputready, exceptready = ss(self.input_list, [], [])
            for self.s in inputready:
    
                self.data = self.s.recv(buffer_size)

                if self.s == self.forward:
                    if len(self.data) == 4:
                        self.on_wclose()
                    else:
                        self.on_wrecv()
                else:
                    if len(self.data) == 0:
                        self.on_close()
                    else:
                        self.on_recv()

    def on_wclose(self):
        data = self.data

        print "on_wclose", repr(data)
        i = int(data)
       
        if i in self.channel:

            s = self.channel[i]

            self.input_list.remove(s)
        
            s.close()
        
            del self.channel[i]
            del self.channel[s]
        
    def on_close(self):

        i = self.channel[self.s]

        data = "{:4}".format(i)

        self.forward.send(data)

        print self.s.getpeername(), "has disconnected"

        #remove objects from input_list
        self.input_list.remove(self.s)
        
        # close the connection with client
        self.channel[i].close()  # equivalent to do self.s.close()
        
        # delete both objects from channel dict
        del self.channel[i]
        del self.channel[self.s]

    def on_recv(self):
        data = self.data
        # here we can parse and/or modify the data before send forward
        i = self.channel[self.s]

        print "recv"
        print "    i =", i
        print "    data of length ", len(data)

        
        assert isinstance(i, int)

        data = "{:4}".format(i) + data

        print "    forwarding {} bytes".format(len(data))

        self.forward.send(data)

    def on_wrecv(self):
        data = self.data

        i = int(data[:4])

        data = data[4:]

        print "wrecv"
        print "    i =", i
        print "    data of length ", len(data)
        
        try:
            s = self.channel[i]
        except:
            print "    create forward", i
            s = Forward().start(self.host, self.port)
            self.input_list.append(s)
            self.channel[i] = s
            self.channel[s] = i

        print "    returning {} bytes".format(len(data))

        s.send(data)

if __name__ == '__main__':
        server = TheServer('192.168.56.2', 8000, '192.168.56.2', 8002)
        try:
            server.main_loop()
        except KeyboardInterrupt:
            print "Ctrl C - Stopping server"
            sys.exit(1)



