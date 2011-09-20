from twisted.internet.protocol import ClientFactory
from twisted.protocols.portforward import Proxy


class AliceProxy(Proxy):
    """
        Receives from Alice and forwards to Bob, unless Eve is around, in which
        case she gets to read and perhaps edit the message first
    """
    def __init__(self):
        self.tlsStarted = False

    def connectionMade(self):
        self.peer.setPeer(self)
        self.peer.transport.resumeProducing()

    def dataReceived(self, data):
        lines = data.split('\r\n')
        for l in lines:
            if l != '':
                print "\t\t" + repr(l)

        if self.peer.factory.eve:
            self.peer.factory.eve[0].intercept(data, self.transport,
                                               self.peer.transport)
        else:
            try:
                self.peer.transport.write(data)
            except Exception as e:
                print "Error forwarding data to Bob: %s" % e


class AliceProxyFactory(ClientFactory):

    protocol = AliceProxy

    def setServer(self, server):
        self.server = server

    def buildProtocol(self, *args, **kw):
        prot = ClientFactory.buildProtocol(self, *args, **kw)
        prot.setPeer(self.server)
        return prot

    def clientConnectionFailed(self, connector, reason):
        self.server.transport.loseConnection()
