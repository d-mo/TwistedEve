from twisted.internet.protocol import ClientFactory
from twisted.protocols.portforward import Proxy


class Server2ClientProxy(Proxy):
    """
        Receives from the server and forwards to the client, unless an
        attack is underway, in which case the message gets intercepted
        and perhaps edited first
    """
    def __init__(self):
        self.tlsStarted = False

    def connectionMade(self):
        self.packetCount = 0
        self.peer.setPeer(self)
        if self.peer.factory.handshake:
            self.peer.factory.handshake(self)
        self.peer.transport.resumeProducing()

    def dataReceived(self, data):
        self.packetCount += 1

        # just print the data if no filter present
        if not self.peer.factory.filter:
            lines = data.split('\r\n')
            for l in lines:
                if l != '':
                    print "\t\t" + repr(l)

        if self.peer.factory.attacker:
            self.peer.factory.attacker[0].intercept(data, self.transport,
                                               self.peer.transport)
        elif self.peer.factory.filter:
            try:
                filtered_data = self.peer.factory.filter(self.packetCount-1, data, self.transport, self.peer.transport)
                if filtered_data != data:
                    print "changed some data"
            except Exception as e:
                print "Error forwarding filtered data to client: %s" % e
        else:
            try:
                self.peer.transport.write(data)
            except Exception as e:
                print "Error forwarding data to client: %s" % e


class Server2ClientProxyFactory(ClientFactory):

    protocol = Server2ClientProxy

    def setServer(self, server):
        self.server = server

    def buildProtocol(self, *args, **kw):
        prot = ClientFactory.buildProtocol(self, *args, **kw)
        prot.setPeer(self.server)
        return prot

    def clientConnectionFailed(self, connector, reason):
        self.server.transport.loseConnection()
