from twisted.protocols.portforward import ProxyServer, ProxyFactory
from twistedeve.server2client import Server2ClientProxyFactory


class Client2ServerProxy(ProxyServer):
    """
        Receives from the client and forwards to the server, unless an attack is underway, 
        in which case the messages are being intercepted and perhaps edited by
        the attacker
    """
    
    clientProtocolFactory = Server2ClientProxyFactory

    def __init__(self):
        self.tlsStarted = False
        self.attacker = False


    def connectionMade(self):
        """
            When client first connects, open a connection to the server
        """
        ProxyServer.connectionMade(self)


    def dataReceived(self, data):
        lines = data.split('\r\n')
        for l in lines:
            if l != '':
                print "\t" + repr(l)

        if self.factory.attacker:
            self.factory.attacker[0].intercept(data, self.transport,
                                          self.peer.transport)
        else:
            try:
                self.peer.transport.write(data)
            except Exception as e:
                print "Error forwarding data to server: %s" % e


class Client2ServerProxyFactory(ProxyFactory):
    protocol = Client2ServerProxy

    def __init__(self, host, port, attacker):
        self.host = host
        self.port = port
        self.attacker = attacker
