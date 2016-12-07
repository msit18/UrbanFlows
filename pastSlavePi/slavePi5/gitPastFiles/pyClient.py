#!/usr/bin/env python

import socket

s = socket.socket()
host = '10.0.0.1'
port = 12397

s.connect((host,port))
print s.recv(1024)
s.close
