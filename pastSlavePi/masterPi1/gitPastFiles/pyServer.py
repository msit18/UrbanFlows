#!/usr/bin/env python

import socket

s = socket.socket()
port = 12397
s.bind(('', port))

s.listen(5)
while True:
	c,addr = s.accept()
	print "Got connection from", addr
	sock = s.getsockname()
	print "Sock name is ", sock
#	c.send("Thank you for connecting")
	c.send("run preview")
	stuff = c.recv(1024)
	print stuff
	c.close()
