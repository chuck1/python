#!/usr/bin/python
# This is a simple port-forward / proxy, written using only the default python
# library. If you want to make a suggestion or fix something you can contact-me
# at voorloop_at_gmail.com
# Distributed over IDC(I Don't Care) license
import socket
import select
import time
import sys

"""
sockets

server  socket that accepts clients

wserver socket that accepts the web server
"""

# Changing the buffer_size and delay, you can improve the speed and bandwidth.
# But when buffer get to high or delay go too down, you can broke things
buffer_size = 1024*16
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
	
    def __init__(self, host, port, wport):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host, port))
        self.server.listen(200)

        self.wserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.wserver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.wserver.bind((host, wport))
        self.wserver.listen(200)

	# index for the client
	self.fcount = 1
	
    def wloop(self):
        """
        wait for the web server host to connect to wserver
        """
        print "wait for wserver"

        self.input_list.append(self.wserver)
        while 1:
            time.sleep(delay)
            ss = select.select
            inputready, outputready, exceptready = ss(self.input_list, [], [])
            for self.s in inputready:
                assert self.s == self.wserver
                self.on_waccept()
                return

    def main_loop(self):

        self.wloop()

        print "wserver connected", self.forward_addr

        self.input_list.append(self.server)
        while 1:
            time.sleep(delay)
            ss = select.select
            inputready, outputready, exceptready = ss(self.input_list, [], [])
            for self.s in inputready:
                if self.s == self.server:
                    self.on_accept()
                    break

                #self.data = self.s.recv(buffer_size)
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

    def on_waccept(self):
        self.forward, self.forward_addr = self.wserver.accept()

        self.input_list.append(self.forward)

        self.input_list.remove(self.wserver)
        self.wserver.close()

    def on_accept(self):
        # original program connected to the forward_to addr and port
        #forward = Forward().start(forward_to[0], forward_to[1])
        # this program will use the self.forward socket that connected to the wserver socket
		
	i = self.fcount
	self.fcount += 1
		
        clientsock, clientaddr = self.server.accept()
        
        assert self.forward

        print clientaddr, "has connected. i =", i
        
        self.input_list.append(clientsock)
        #self.input_list.append(i)
        self.channel[clientsock] = i
        self.channel[i] = clientsock

    def on_close(self):
        
        print self.s.getpeername(), "has disconnected"
    
        i = self.channel[self.s]
        data = "{:4}".format(i)
        self.forward.send(data)
        
        #remove objects from input_list
        self.input_list.remove(self.s)
        
        # close the connection with remote server
	self.s.close()
        
        # delete both objects from channel dict
        del self.channel[i]
        del self.channel[self.s]


    def on_wclose(self):

        data = self.data

        i = int(data)

        print "wclose i =", i

        if i in self.channel:

            s = self.channel[i]

            self.input_list.remove(s)

            s.close()

            del self.channel[i]
            del self.channel[s]

    def on_recv(self):
        data = self.data
       	i = self.channel[self.s]

        assert isinstance(i, int)

        print "recv"
        print "    i =", i
        print "    data of length",len(data)

        data = "{:4}".format(i) + data

        print "    forwarding {} bytes".format(len(data))

        self.forward.send(data)

    def on_wrecv(self):
        data = self.data
        
        try:
            i = int(data[:4])
        except:
            print repr(data)
            sys.exit(1)

        data = data[4:]

        print "wrecv"
        print "    i =", i
        print "    data of length",len(data)

        self.channel[i].send(data)
    
if __name__ == '__main__':
        server = TheServer('', 8001, 8002)
        try:
            server.main_loop()
        except KeyboardInterrupt:
            print "Ctrl C - Stopping server"
            sys.exit(1)



