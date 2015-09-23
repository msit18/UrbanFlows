#!/usr/bin/env python

import sys
import pika

credentails = pika.PlainCredentials(username='pi', password='raspberry')

connection = pika.BlockingConnection(pika.ConnectionParameters(host='10.0.0.1', credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='direct_logs', type='direct')

severity = sys.argv[1] if len(sys.argv) > 1 else 'info'

message = ' '.join(sys.argv[1:]) or "Hello World"
channel.basic_publish(exchange='direct_logs', routing_key=severity, body=message)
print " [x] Sent %r:%r" % (severity, message)
connection.close()
