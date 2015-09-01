#!/usr/bin/env python

# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

from twisted.cred import portal, checkers
from twisted.conch import error, avatar
from twisted.conch.checkers import SSHPublicKeyDatabase
from twisted.conch.ssh import factory, userauth, connection, keys, session
from twisted.internet import reactor, protocol, defer
from twisted.python import log
from zope.interface import implements
import sys
#log.startLogging(sys.stderr)

"""
Example of running another protocol over an SSH channel.
log in with username "user" and password "password".
"""

class ExampleAvatar(avatar.ConchUser):

    def __init__(self, username):
        avatar.ConchUser.__init__(self)
        self.username = username
        self.channelLookup.update({'session':session.SSHSession})

class ExampleRealm:
    implements(portal.IRealm)

    def requestAvatar(self, avatarId, mind, *interfaces):
	print "running requestAvatar"
        return interfaces[0], ExampleAvatar(avatarId), lambda: None

class EchoProtocol(protocol.Protocol):
    """this is our example protocol that we will run over SSH
    """
    def dataReceived(self, data):
	print "running dataReceived"
        if data == '\r':
            data = '\r\n'
        elif data == '\x03': #^C
            self.transport.loseConnection()
            return
        self.transport.write(data)

publicKey = 'ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAGEArzJx8OYOnJmzf4tfBEvLi8DVPrJ3/c9k2I/Az64fxjHf9imyRJbixtQhlH9lfNjUIx+4LmrJH5QNRsFporcHDKOTwTTYLh5KmRpslkYHRivcJSkbh/C+BR3utDS555mV'

privateKey = """-----BEGIN RSA PRIVATE KEY-----
MIIByAIBAAJhAK8ycfDmDpyZs3+LXwRLy4vA1T6yd/3PZNiPwM+uH8Yx3/YpskSW
4sbUIZR/ZXzY1CMfuC5qyR+UDUbBaaK3Bwyjk8E02C4eSpkabJZGB0Yr3CUpG4fw
vgUd7rQ0ueeZlQIBIwJgbh+1VZfr7WftK5lu7MHtqE1S1vPWZQYE3+VUn8yJADyb
Z4fsZaCrzW9lkIqXkE3GIY+ojdhZhkO1gbG0118sIgphwSWKRxK0mvh6ERxKqIt1
xJEJO74EykXZV4oNJ8sjAjEA3J9r2ZghVhGN6V8DnQrTk24Td0E8hU8AcP0FVP+8
PQm/g/aXf2QQkQT+omdHVEJrAjEAy0pL0EBH6EVS98evDCBtQw22OZT52qXlAwZ2
gyTriKFVoqjeEjt3SZKKqXHSApP/AjBLpF99zcJJZRq2abgYlf9lv1chkrWqDHUu
DZttmYJeEfiFBBavVYIF1dOlZT0G8jMCMBc7sOSZodFnAiryP+Qg9otSBjJ3bQML
pSTqy7c3a2AScC/YyOwkDaICHnnD3XyjMwIxALRzl0tQEKMXs6hH8ToUdlLROCrP
EhQ0wahUTCk1gKA4uPD6TMTChavbh4K63OvbKg==
-----END RSA PRIVATE KEY-----"""


class InMemoryPublicKeyChecker(SSHPublicKeyDatabase):

    def checkKey(self, credentials):
	print "running checkKey"
        return credentials.username == 'michelle' and \
            keys.Key.fromString(data=publicKey).blob() == credentials.blob

class ExampleSession:
    
    def __init__(self, avatar):
        """
        We don't use it, but the adapter is passed the avatar as its first
        argument.
        """

    def getPty(self, term, windowSize, attrs):
	print "running getPty"
        pass
    
    def execCommand(self, proto, cmd):
	print "running execCommand"
        raise Exception("no executing commands")

    def openShell(self, trans):
	print "running openShell"
        ep = EchoProtocol()
        ep.makeConnection(trans)
        trans.makeConnection(session.wrapProtocol(ep))

    def eofReceived(self):
	print "running eofReceived"
        pass

    def closed(self):
	print "running closed"
        pass

from twisted.python import components
components.registerAdapter(ExampleSession, ExampleAvatar, session.ISession)

class ExampleFactory(factory.SSHFactory):
    publicKeys = {
        'ssh-rsa': keys.Key.fromString(data=publicKey)
    }
    privateKeys = {
        'ssh-rsa': keys.Key.fromString(data=privateKey)
    }
    services = {
        'ssh-userauth': userauth.SSHUserAuthServer,
        'ssh-connection': connection.SSHConnection
    }
    

portal = portal.Portal(ExampleRealm())
passwdDB = checkers.InMemoryUsernamePasswordDatabaseDontUse()
passwdDB.addUser('michelle', 'Li2ee9hi')
portal.registerChecker(passwdDB)
portal.registerChecker(InMemoryPublicKeyChecker())
ExampleFactory.portal = portal

if __name__ == '__main__':
    reactor.listenTCP(2222, ExampleFactory())
    reactor.run()
