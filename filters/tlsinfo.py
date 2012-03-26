# display TLS version and ciphersuites supported by the client and the server

from tlslite.utils.compat import stringToBytes, bytesToString
from tlslite.api import *
from tlslite.utils.codec import Parser
from tlslite.messages import ClientHello, ServerHello

def handshake(source):
    pass

def filter(packetNo, data, source, target):
    bytes = stringToBytes(data)
    if packetNo == 0 and 'Client2Server' in str(source):
        p = Parser(bytes[5:])
        p.get(1)
        clientHello = ClientHello()
        clientHello.parse(p)
        print "Client supports TLS version: %s" % str(clientHello.client_version)
        print "Client supports ciphersuites: %s" % str(clientHello.cipher_suites)
    elif packetNo == 0 and 'Client2Server' not in str(source):
        p = Parser(bytes[5:])
        p.get(1)
        serverHello = ServerHello()
        serverHello.parse(p)
        print "Server selected TLS version: %s" % str(serverHello.server_version)
        print "Server selected ciphersuite: %s" % str(serverHello.cipher_suite)

    target.write(data)        
    return data