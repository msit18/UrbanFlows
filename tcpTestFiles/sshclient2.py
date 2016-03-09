#Current working ssh client file

from twisted.conch.ssh import transport, connection, userauth, channel, common
from twisted.internet import defer, protocol, reactor
from twisted.python import log
import sys, getpass
log.startLogging(sys.stderr)

class ClientCommandFactory(protocol.ClientFactory):
    def __init__(self, username, password, command):
        self.username = username
        self.password = password
        self.command = command

    def buildProtocol(self, addr):
        protocol = ClientCommandTransport(
            self.username, self.password, self.command)
        return protocol

class ClientCommandTransport(transport.SSHClientTransport):
    def __init__(self, username, password, command):
        self.username = username
        self.password = password
        self.command = command

    def verifyHostKey(self, pubKey, fingerprint):
        # in a real app, you should verify that the fingerprint matches
        # the one you expected to get from this server
        return defer.succeed(True)

    def connectionSecure(self):
        print "running connectionSecure"
        self.requestService(
            PasswordAuth(self.username, self.password, ClientConnection(self.command) ) )

class PasswordAuth(userauth.SSHUserAuthClient):
    def __init__(self, user, password, connection):
        userauth.SSHUserAuthClient.__init__(self, user, connection)
        self.password = password

    def getPassword(self, prompt=None):
        return defer.succeed(self.password)

class ClientConnection(connection.SSHConnection):
    def __init__(self, cmd, *args, **kwargs):
        connection.SSHConnection.__init__(self)
        self.command = cmd

    def serviceStarted(self):
        print "running serviceStarted"
        self.openChannel(CommandChannel(self.command, conn=self))

class CommandChannel(channel.SSHChannel):
    name = 'session'

    def __init__(self, command, *args, **kwargs):
        channel.SSHChannel.__init__(self, *args, **kwargs)
        self.command = command

    def channelOpen(self, data):
        print "running channelOpen for client"
        pass
        # self.conn.sendRequest(
        #     self, 'exec', common.NS(self.command), wantReply=True).addCallback(
        #     self._gotResponse)

    def _gotResponse(self, _):
        print "running _gotResponse"
        #self.conn.sendEOF(self)

    def dataReceived(self, data):
        print "received: {0}".format(data)
        print data

    def closed(self):
        reactor.stop()


server = '18.111.37.15' #hostname that this file connects to
#command = 'python /home/pi/UrbanFlows/slavePi2/takepic.py'
command = 'whoami'
username = 'pi'
password = 'raspberry'
factory = ClientCommandFactory(username, password, command)
#Use port 22 for direct commands.  Use 2222 if there's a server waiting on the other side
#reactor.connectTCP(server, 22, factory)
reactor.connectTCP(server, 2222, factory)
reactor.run()
