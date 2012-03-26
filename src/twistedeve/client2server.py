from twisted.protocols.portforward import ProxyServer, ProxyFactory
from twistedeve.server2client import Server2ClientProxyFactory
from tlslite.api import *

class Client2ServerProxy(ProxyServer):
    """
        Receives from the client and forwards to the server, unless an attack 
        is underway, in which case the messages are being intercepted and 
        perhaps edited by the attacker
    """
    
    clientProtocolFactory = Server2ClientProxyFactory

    def __init__(self):
        self.tlsStarted = False
        self.attacker = False


    def connectionMade(self):
        """
            When client first connects, open a connection to the server
        """
        self.packetCount = 0
        if self.factory.attacker:
            self.factory.attacker[0].packetCount = 0
        if self.factory.handshake:
            self.factory.handshake(self)
        ProxyServer.connectionMade(self)          


    def dataReceived(self, data):
        self.packetCount += 1
        
        lines = data.split('\r\n')
        
        # just print the data if no filter present
        if not self.factory.filter:
            for l in lines:
                if l != '':
                    print "\t" + repr(l)

        if self.factory.attacker:
            self.factory.attacker[0].intercept(data, self.transport,
                                          self.peer.transport)
        elif self.factory.filter:
            try:
                filtered_data = self.factory.filter(self.packetCount-1, 
                                                    data, 
                                                    self.transport, 
                                                    self.peer.transport)
                if filtered_data != data:
                    print "changed some data"
            except Exception as e:
                print "Error forwarding filtered data to server: %s" % e
             
        else:
            try:
                self.peer.transport.write(data)
            except Exception as e:
                print "Error forwarding data to server: %s" % e


class Client2ServerProxyFactory(ProxyFactory):
    protocol = Client2ServerProxy

    def __init__(self, host, port, filter, 
                 handshake, key, certChain, attacker):
        self.host = host
        self.port = port
        self.attacker = attacker
        self.filter = filter
        self.handshake = handshake
        self.key = key
        self.certChain = certChain

        
