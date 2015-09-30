from twisted.internet import defer, reactor


class Getter:
	def __init__(self, d):
		self.d = defer.Deferred()

	def gotResults(self, x):
	    # if self.d is None:
	    #     print "Nowhere to put results"
	    #     return
        #d = self.d
        #self.d = None
		if x % 2 == 0:
		    d.callback(x*3)
		else:
		    d.errback(ValueError("You used an odd number!"))

	def _toHTML(self, r):
	    return "Result: %s" % r

	def getDummyData(self, x):
	    #self.d = defer.Deferred()
	    # simulate a delayed result by asking the reactor to schedule
	    # gotResults in 2 seconds time
	    #reactor.callLater(2, self.gotResults, x)
	    self.d.callback(2)
	    self.d.addCallback(self._toHTML)
	    self.d.addCallback(self.gotResults(x))
	    return self.d

class methods:
	def printData(self, d):
	    print d

	def printError(self, failure):
	    import sys
	    sys.stderr.write(str(failure))

if __name__ == '__main__':
	d = defer.Deferred()

	# this series of callbacks and errbacks will print an error message
	g = Getter(d)
	f = methods()
	d = g.getDummyData(3)
	d.addCallback(f.printData)
	d.addErrback(f.printError)

	# this series of callbacks and errbacks will print "Result: 12"
	g = Getter(d)
	d = g.getDummyData(4)
	d.addCallback(f.printData)
	d.addErrback(f.printError)

	#reactor.callLater(4, reactor.stop)
	#d.callback(4)
	reactor.run()



# class stuff:
# 	def getDummyData(self, x):
# 	    """
# 	    This function is a dummy which simulates a delayed result and
# 	    returns a Deferred which will fire with that result. Don't try too
# 	    hard to understand this.
# 	    """
# 	    d = defer.Deferred()
# 	    # simulate a delayed result by asking the reactor to fire the
# 	    # Deferred in 2 seconds time with the result x * 3
# 	    reactor.callLater(2, d.callback, x * 3)
# 	    return d

# 	def printData(self, d):
# 	    """
# 	    Data handling function to be added as a callback: handles the
# 	    data by printing the result
# 	    """
# 	    print d

# if __name__ == '__main__':
# 	f = stuff()
# 	d = f.getDummyData(3)
# 	d.addCallback(f.printData)

# 	# manually set up the end of the process by asking the reactor to
# 	# stop itself in 4 seconds time
# 	reactor.callLater(4, reactor.stop)
# 	# start up the Twisted reactor (event loop handler) manually
# 	reactor.run()


# class stuff:
# 	def getIP (self, x):
# 		return x

# 	def secondIP (self, s):
# 		print "ran secondIP"

# 	def ipfailed(self, err):
# 		print "didn't get that"

# if __name__ == '__main__':

# 	d  = defer.Deferred()
# 	f = stuff()

# 	d.addCallback(f.getIP("a"))
# 	d.addErrback(ipfailed())
# 	d.callback("10.0.0.10")
# 	#d.addErrback(ipfailed)

# 	print "finished"


# def got_poem(res):
#     print 'Your poem is served:'
#     print res
 
# def poem_failed(err):
#     print 'No poetry for you.'
 
# d = Deferred()
 
# # add a callback/errback pair to the chain
# d.addCallbacks(got_poem, poem_failed)
 
# # fire the chain with a normal result
# d.callback('This poem is short.')
 
# print "Finished"