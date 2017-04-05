import os
import socket
import sys
import urllib2

HOST = ''   # Symbolic name, meaning all available interfaces
PORT = 4001 # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print 'Socket bind complete'

#Start listening on socket
s.listen(10)
print 'Socket now listening'

#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])

    msg = conn.recv(1024)

    print 'msg',repr(msg)
    
    if "'" in msg:
        print "msg contains ' may contain malicious content"
        continue
    
    msg=msg.replace("=","%"+hex(ord('='))[2:].upper())

    print 'msg',repr(msg)
    
    data_s = "key={}&title=untitled&msg={}&event=notification".format(os.environ['SIMPLEPUSH_KEY'], msg)
    
    print 'data',repr(data_s)

    req = urllib2.Request(
            "https://api.simplepush.io/send",
            data = data_s)

    f = urllib2.urlopen(req)
    print f.read()

s.close()



