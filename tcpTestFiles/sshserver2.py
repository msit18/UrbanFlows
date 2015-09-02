from twisted.conch import avatar, recvline
from twisted.conch.interfaces import IConchUser, ISession
from twisted.conch.ssh import factory, keys, session, channel, common
from twisted.conch.insults import insults
from twisted.cred import portal, checkers
from twisted.internet import reactor
from zope.interface import implements
import os

class SSHDemoAvatar(avatar.ConchUser):
    implements(ISession)

    def __init__(self, username):
        avatar.ConchUser.__init__(self)
        self.username = username
        self.channelLookup.update({'session': session.SSHSession})
        numConnections += 1

    # def openShell(self, protocol):
    #     print "running openShell"
    #     serverProtocol = insults.ServerProtocol(SSHDemoProtocol, self)
    #     serverProtocol.makeConnection(protocol)
    #     protocol.makeConnection(session.wrapProtocol(serverProtocol))

    def execCommand(self, protocol, cmd):
        print "running execCommand"
        print cmd
        os.system(cmd)
        #os.system("scp /home/pi/success.jpg pi")

    def closed(self):
        print "running closed"
        pass

class SSHDemoRealm(object):
    implements(portal.IRealm)

    def requestAvatar(self, avatarId, mind, *interfaces):
        print "running requestAvatar"
        if IConchUser in interfaces:
            return interfaces[0], SSHDemoAvatar(avatarId), lambda: None
        else:
            raise NotImplementedError("No supported interfaces found.")

def getRSAKeys():
    with open('/home/pi/.ssh/id_rsa') as privateBlobFile:
        privateBlob = privateBlobFile.read()
        privateKey = keys.Key.fromString(data=privateBlob)

    with open('/home/pi/.ssh/id_rsa.pub') as publicBlobFile:
        publicBlob = publicBlobFile.read()
        publicKey = keys.Key.fromString(data=publicBlob)

    return publicKey, privateKey

if __name__ == "__main__":
    print "waiting"
    sshFactory = factory.SSHFactory()
    sshFactory.portal = portal.Portal(SSHDemoRealm())

    users = {'admin': 'aaa', 'guest': 'bbb', 'pi':'raspberry'}
    sshFactory.portal.registerChecker(
        checkers.InMemoryUsernamePasswordDatabaseDontUse(**users))

    pubKey, privKey = getRSAKeys()
    sshFactory.publicKeys = {'ssh-rsa': pubKey}
    sshFactory.privateKeys = {'ssh-rsa': privKey}

    global numConnections
    numConnections = 0
    reactor.listenTCP(2222, sshFactory)
    reactor.run()
