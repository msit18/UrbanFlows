import threading
import Queue
import threadTestA
import threadTestB
import sys

from twisted.internet import reactor, protocol, defer

class hi():

	def failed(self, failure):
		print "FAILURE"
		sys.stderr.write(str(failure))

	def go(self, value):
		print value
		d.addCallback(tAstart.start)
		d.addErrback(h.failed)

	# def stuff(self, value):
	# 	print valu
	# 	print "STUFF"

if __name__ == '__main__':
	h = hi()
	queue = Queue.Queue()
	# tA = threadTestA()
	# tB = threadTestB()

	d = defer.Deferred()

	tAstart = threadTestA.thread1(queue)
	tBstart = threadTestB.thread2(queue)
	# d.addCallback(h.go)
	# d.addErrback(h.failed)
	# d.callback("stuff")
	# d.addCallback(tAstart.run)
	# d.addErrback(h.failed)

	tAstart.start()
	tBstart.start()

	reactor.run()