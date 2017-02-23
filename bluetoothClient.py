#Written by Michelle Sit. 
#Based off of the l2capclient.py from pybluez (Albert Huang, MIT)

#Client => Server. Client sends cmds to the Server.

import bluetooth, sys

class BluetoothClient():
	def run(self):
		print("connected.  Enter password:")
		while True:
			data = input()
			if(str(data) == "Thanks"): break
			sock.send(data)

			while True:
				data = sock.recv(1024)
				if (str(data) == "EOL"):
					print "END OF LINE"
					break
				else:
					print "Received: ", data

		sock.close()

if __name__ == '__main__':
	blC = BluetoothClient()

	if sys.version < '3':
		input = raw_input

	sock=bluetooth.BluetoothSocket(bluetooth.L2CAP)
	bluetooth.set_l2cap_mtu( sock, 65535 )

	if len(sys.argv) < 2:
		print("usage: l2capclient.py <addr>")
		sys.exit(2)

	bt_addr=sys.argv[1]
	port = 0x1001

	print("trying to connect to %s on PSM 0x%X" % (bt_addr, port))

	sock.connect((bt_addr, port))
	blC.run()