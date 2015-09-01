#!/usr/bin/env python

import socket
import os

s = socket.socket()
host = '10.0.0.1'
port = 12397

s.connect((host,port))
cmd = s.recv(1024)
print "Receiving: ", cmd
#if cmd == "run preview":
#	print "cmd correct"
#	os.system("python preview.py")
partner = s.getpeername()
print "Connected with ", partner
s.send("hi friend")
s.close()

#write code that triggers flash.py on the MasterPi 
