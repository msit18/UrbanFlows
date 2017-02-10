#Written by Michelle Sit. 
#Based off of the l2capserver.py from pybluez (Albert Huang, MIT)

import bluetooth, subprocess
from sys import stdout

class BluetoothServer():

	def checkPassword(self):
		passAttempt = 0
		while passAttempt < 4:
			data = client_sock.recv(1024)
			print("Data received: ", str(data))
			print "PassAttempt value: ", passAttempt
			if (str(data) != "MCS") & (passAttempt < 2):
				client_sock.send("Sorry, that is the wrong password. Try again.")
				client_sock.send("EOL")
				passAttempt += 1
			elif (str(data) != "MCS") & (passAttempt >= 2):
				client_sock.send("Sorry, that is the wrong password. Exiting program.")
				client_sock.send("EOL")
				client_sock.close()
				break
			else:
				print "run the rest of the program"
				client_sock.send("Enter your bash command.")
				client_sock.send("EOL")
				self.psuedoServer()

	def psuedoServer(self):
		print "Password accepted. Accepting cmds."
		while True:
			data = client_sock.recv(1024)
			print "Data received:", str(data)
			#Method for executing the commands

			cmd = str(data)
			print "cmd: ", cmd
			proc = subprocess.Popen(cmd, shell=True, bufsize=256, stdout=subprocess.PIPE)
			for line in proc.stdout:
				stdoutLine = line.rstrip()
				client_sock.send(stdoutLine)
				print ">>> " + stdoutLine
			client_sock.send("EOL")
			stdout.flush()

	def run(self):
		print("Accepted connection from ",address)
		try:
			#Ask for password for this round. Refuse to connect if given wrong value.
			self.checkPassword()
		except bluetooth.btcommon.BluetoothError:
			print "caught bluetooth error"
			pass


if __name__ == '__main__':
	blS = BluetoothServer()
	while True:
		server_sock=bluetooth.BluetoothSocket( bluetooth.L2CAP )
		bluetooth.set_l2cap_mtu( server_sock, 65535 )

		port = 0x1001

		server_sock.bind(("",port))
		server_sock.listen(1)

		print "waiting to accept sock"
		client_sock, address = server_sock.accept()
		blS.run()

	client_sock.close()
	server_sock.close()