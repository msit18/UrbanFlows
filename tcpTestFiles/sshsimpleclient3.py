#!/usr/bin/env python

# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

from twisted.conch.ssh import transport, userauth, connection, common, keys, channel
from twisted.internet import defer, protocol, reactor
from twisted.python import log
import struct, sys, getpass, os

USER = 'pi'  # replace this with a valid username
HOST = '18.111.53.136' # and a valid host
PASSPHRASE = 'raspberry'

class SimpleTransport(transport.SSHClientTransport):
    def verifyHostKey(self, hostKey, fingerprint):
        print "running SimpleTransport verifyHostKey"
        print 'host key fingerprint: %s' % fingerprint
        return defer.succeed(1) 

    def connectionSecure(self):
        print "running SimpleTransport connectionSecure"
        self.requestService(
            SimpleUserAuth(USER,
                SimpleConnection()))

class SimpleUserAuth(userauth.SSHUserAuthClient):
    def getPassword(self):
        print "running SimpleUserAuth getPassword"
        return defer.succeed(getpass.getpass("%s@%s's password: " % (USER, HOST)))
        #return defer.succeed(PASSPHRASE)
            
    def getPublicKey(self):
        print "running SimpleUserAuth getPublicKey"
        path = os.path.expanduser('/home/michelle/.ssh/known_hosts') 
        # this works with rsa too
        # just change the name here and in getPrivateKey
        if not os.path.exists(path) or self.lastPublicKey:
            # the file doesn't exist, or we've tried a public key
            return
        return keys.Key.fromFile(filename=path+'.pub').blob()

    def getPrivateKey(self):
        print "running SimpleUserAuth getPrivateKey"
        path = os.path.expanduser('~/.ssh/known_hosts')
        return defer.succeed(keys.Key.fromFile(path).keyObject)

class SimpleConnection(connection.SSHConnection):
    def serviceStarted(self):
        print "running SimpleConnection serviceStarted"
        self.openChannel(TrueChannel(2**16, 2**15, self))
        self.openChannel(FalseChannel(2**16, 2**15, self))
        self.openChannel(CatChannel(2**16, 2**15, self))

class AttemptChannel(channel.SSHChannel):
    name = 'session'

    def openFailed(self, reason):
        print "running TrueChannel openFailed"
        print 'true failed', reason

    def channelOpen(self, ignoredData):
        print "running TrueChannel channelOpen"
        self.conn.sendRequest(self, 'exec', common.NS('true'))



# class EchoProtocol(Protocol):
#     def connectionMade(self):
#         self.transport.write("Echo protocol connected\r\n")

#     def dataReceived(self, bytes):
#         self.transport.write("echo: " + repr(bytes) + "\r\n")

#     def connectionLost(self, reason):
#         print 'Connection lost', reason


class TrueChannel(channel.SSHChannel):
    name = 'session' # needed for commands

    def openFailed(self, reason):
        print "running TrueChannel openFailed"
        print 'true failed', reason
    
    def channelOpen(self, ignoredData):
        print "running TrueChannel channelOpen"
        self.conn.sendRequest(self, 'exec', common.NS('true'))

    def request_exit_status(self, data):
        print "running TrueChannel request_exit_status"
        status = struct.unpack('>L', data)[0]
        print 'true status was: %s' % status
        self.loseConnection()

class FalseChannel(channel.SSHChannel):
    name = 'session'

    def openFailed(self, reason):
        print "running FalseChannel openFailed"
        print 'false failed', reason

    def channelOpen(self, ignoredData):
        print "running FalseChannel channelOpen"
        self.conn.sendRequest(self, 'exec', common.NS('false'))

    def request_exit_status(self, data):
        print "running FalseChannel request_exit_status"
        status = struct.unpack('>L', data)[0]
        print 'false status was: %s' % status
        self.loseConnection()

class CatChannel(channel.SSHChannel):
    name = 'session'

    def openFailed(self, reason):
        print "running CatChannel openFailed"
        print 'echo failed', reason

    def channelOpen(self, ignoredData):
        print "running CatChannel channelOpen"
        self.data = ''
        d = self.conn.sendRequest(self, 'exec', common.NS('cat'), wantReply = 1)
        d.addCallback(self._cbRequest)

    def _cbRequest(self, ignored):
        print "running CatChannel _cbRequest"
        self.write('hello conch\n')
        self.conn.sendEOF(self)

    def dataReceived(self, data):
        print "running CatChannel dataReceived"
        self.data += data

    def closed(self):
        print "running CatChannel closed"
        print 'got data from cat: %s' % repr(self.data)
        # self.loseConnection()
        # reactor.stop()

protocol.ClientCreator(reactor, SimpleTransport).connectTCP(HOST, 2222)
reactor.run()
