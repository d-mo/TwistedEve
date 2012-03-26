from tlslite.utils.compat import stringToBytes, bytesToString
from tlslite.api import *

def handshake(source):
    if 'client2server' in str(source.__class__): # client to server message
        if source.factory.key:
            source.transport.socket = TLSConnection(source.transport.socket)
            #When tls connection closes, close the socket as well
            source.transport.socket.closeSocket = True
            
            # Configure handshake settings
            settings = HandshakeSettings()
            #settings.minKeySize = 2048
            #settings.cipherNames = ["aes256"]
            #settings.minVersion = (3,0)
            source.transport.socket.handshakeServer(certChain=source.factory.certChain, 
                                                    privateKey=source.factory.key, 
                                                    settings=settings)
    else: # server to client message
        if source.peer.factory.key:
            source.transport.socket = TLSConnection(source.transport.socket)
            #When tls connection closes, close the socket as well
            source.transport.socket.closeSocket = True
            
            # Configure handshake settings
            # settings = HandshakeSettings()
            source.transport.socket.handshakeClientCert()
        


def filter(packetNo, data, source, target):
    bytes = stringToBytes(data)
    if packetNo == 0 and 'Client2Server' in str(source):
        pass
    elif packetNo == 1 and 'Client2Server' not in str(source):
        print "server says hello"
        print bytes
        
    result = bytesToString(bytes)
    target.write(result)
    return result