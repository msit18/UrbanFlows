from twisted.internet.protocol import Protocol
from twisted.cred.portal import Portal
from twisted.cred.checkers import FilePasswordDB
from twisted.conch.ssh.factory import SSHFactory
from twisted.internet import reactor
from twisted.conch.ssh.keys import Key
from twisted.conch.interfaces import IConchUser
from twisted.conch.avatar import ConchUser
from twisted.conch.ssh.session import (
    SSHSession, SSHSessionProcessProtocol, wrapProtocol)
import os
from twisted.conch.ssh import keys

# with open('/home/michelle/.ssh/known_hosts') as privateBlobFile:
#     privateBlob = privateBlobFile.read()
#     privateKey = Key.fromString(data=privateBlob)

with open('/home/michelle/.ssh/id_rsa') as privateBlobFile:
    privateBlob = privateBlobFile.read()
    privateKey = Key.fromString(data=privateBlob)

with open('/home/michelle/.ssh/id_rsa.pub') as publicBlobFile:
    publicBlob = publicBlobFile.read()
    publicKey = Key.fromString(data=publicBlob)

class EchoProtocol(Protocol):
    def connectionMade(self):
        self.transport.write("Echo protocol connected\r\n")

    def dataReceived(self, bytes):
        self.transport.write("echo: " + repr(bytes) + "\r\n")

    def connectionLost(self, reason):
        print 'Connection lost', reason

def nothing():
    pass

class SimpleSession(SSHSession):
    name = 'session'

    def request_pty_req(self, data):
        return True

    def request_shell(self, data):
        protocol = EchoProtocol()
        transport = SSHSessionProcessProtocol(self)
        protocol.makeConnection(transport)
        transport.makeConnection(wrapProtocol(protocol))
        self.client = transport
        return True

class SimpleRealm(object):
    def requestAvatar(self, avatarId, mind, *interfaces):
        user = ConchUser()
        user.channelLookup['session'] = SimpleSession
        return IConchUser, user, nothing

factory = SSHFactory()
factory.privateKeys = {'ssh-rsa': privateKey}
factory.publicKeys = {'ssh-rsa': publicKey}
factory.portal = Portal(SimpleRealm())
factory.portal.registerChecker(FilePasswordDB("ssh-passwords"))

reactor.listenTCP(2022, factory)
reactor.run()