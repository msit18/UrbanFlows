#!/usr/bin/env python

import mosquitto
import time

def on_connect(mosq, obj, msg):
	print "Connected"

def on_message(mosq, obj, msg):
	msg_time = time.time()
	snap_time = float(msg.payload)
	while time.time() < snap_time:
		pass
	now_time = time.time()

	print("msg={}, snap={}, now={}".format(msg_time, snap_time, now_time))

mq = mosquitto.Mosquitto()

#define callbacks
mq.on_message = on_message
mq.on_connect = on_connect

#connect
mq.connect("mercury")

#subscribe to topic
mq.subscribe("photo/trigger")

#keep connected to broker
while mq.loop() == 0:
	pass
