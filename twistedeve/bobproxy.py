from twisted.protocols.portforward import ProxyServer, ProxyFactory
from twistedeve.aliceproxy import AliceProxy, AliceProxyFactory


class BobProxy(ProxyServer):
    """
        Receives from Bob and forwards to Alice, unless Eve is around, in which
        case she gets to read and perhaps edit the message first
    """
    clientProtocolFactory = AliceProxyFactory

    def __init__(self):
        self.tlsStarted = False
        self.attacker = False

    def connectionMade(self):
        """
            When Bob first connects, open a connection to Alice
        """
        ProxyServer.connectionMade(self)
        """# Don't read anything from the connecting client until we have
        # somewhere to send it to.
        self.transport.pauseProducing()

        client = self.clientProtocolFactory()
        client.setServer(self)

        from twisted.internet import reactor
        reactor.connectTCP(self.factory.host, self.factory.port, client)
        """
        #if options.tls == 'auto' and stx:
        #    self.transport.startTLS(stx, BobProxyFactory)
        #    self.tlsStarted = True

    def dataReceived(self, data):
        lines = data.split('\r\n')
        for l in lines:
            if l != '':
                print "\t" + repr(l)

        if self.factory.eve:
            self.factory.eve[0].intercept(data, self.transport,
                                          self.peer.transport)
        else:
            try:
                self.peer.transport.write(data)
            except Exception as e:
                print "Error forwarding data to Alice: %s" % e


class BobProxyFactory(ProxyFactory):
    protocol = BobProxy

    def __init__(self, host, port, eve):
        self.host = host
        self.port = port
        self.eve = eve
