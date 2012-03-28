# display TLS version and ciphersuites supported by the client and the server

from tlslite.utils.compat import stringToBytes, bytesToString
from tlslite.api import *
from tlslite.utils.codec import Parser
from tlslite.messages import ClientHello, ServerHello
from twistedeve.attackshell import bcolors

def handshake(source):
    pass

def filter(packetNo, data, source, target):
    bytes = stringToBytes(data)
    if packetNo == 0 and 'Client2Server' in str(source):
        p = Parser(bytes[5:])
        p.get(1)
        clientHello = ClientHello()
        clientHello.parse(p)
        print bcolors.OKGREEN + "Client supports TLS version: %s" % \
            str(clientHello.client_version)
        print "Client supports ciphersuites: %s" % \
            str([CIPHER_MAP.get(i,i) for i in clientHello.cipher_suites]) \
            + bcolors.ENDC
    elif packetNo == 0 and 'Client2Server' not in str(source):
        p = Parser(bytes[5:])
        p.get(1)
        serverHello = ServerHello()
        serverHello.parse(p)
        print bcolors.OKGREEN + "Server selected TLS version: %s" % \
            str(serverHello.server_version)
        print "Server selected ciphersuite: %s" % \
            str(CIPHER_MAP.get(serverHello.cipher_suite,
                               serverHello.cipher_suite)) + bcolors.ENDC

    target.write(data)        
    return data

CIPHER_MAP = {}

CIPHER_MAP[0x00] = 'TLS_NULL_WITH_NULL_NULL'
CIPHER_MAP[0x01] = 'TLS_RSA_WITH_NULL_MD5'
CIPHER_MAP[0x02] = 'TLS_RSA_WITH_NULL_SHA'
CIPHER_MAP[0x3B] = 'TLS_RSA_WITH_NULL_SHA256 '
CIPHER_MAP[0x04] = 'TLS_RSA_WITH_RC4_128_MD5'
CIPHER_MAP[0x05] = 'TLS_RSA_WITH_RC4_128_SHA'
CIPHER_MAP[0x0A] = 'TLS_RSA_WITH_3DES_EDE_CBC_SHA'
CIPHER_MAP[0x2F] = 'TLS_RSA_WITH_AES_128_CBC_SHA'
CIPHER_MAP[0x35] = 'TLS_RSA_WITH_AES_256_CBC_SHA'
CIPHER_MAP[0x3C] = 'TLS_RSA_WITH_AES_128_CBC_SHA256'
CIPHER_MAP[0x3D] = 'TLS_RSA_WITH_AES_256_CBC_SHA256'

CIPHER_MAP[0x0D] = 'TLS_DH_DSS_WITH_3DES_EDE_CBC_SHA'
CIPHER_MAP[0x10] = 'TLS_DH_RSA_WITH_3DES_EDE_CBC_SHA'
CIPHER_MAP[0x13] = 'TLS_DHE_DSS_WITH_3DES_EDE_CBC_SHA'
CIPHER_MAP[0x16] = 'TLS_DHE_RSA_WITH_3DES_EDE_CBC_SHA'
CIPHER_MAP[0x30] = 'TLS_DH_DSS_WITH_AES_128_CBC_SHA'
CIPHER_MAP[0x31] = 'TLS_DH_RSA_WITH_AES_128_CBC_SHA'
CIPHER_MAP[0x32] = 'TLS_DHE_DSS_WITH_AES_128_CBC_SHA'
CIPHER_MAP[0x33] = 'TLS_DHE_RSA_WITH_AES_128_CBC_SHA'
CIPHER_MAP[0x36] = 'TLS_DH_DSS_WITH_AES_256_CBC_SHA'
CIPHER_MAP[0x37] = 'TLS_DH_RSA_WITH_AES_256_CBC_SHA'
CIPHER_MAP[0x38] = 'TLS_DHE_DSS_WITH_AES_256_CBC_SHA'
CIPHER_MAP[0x39] = 'TLS_DHE_RSA_WITH_AES_256_CBC_SHA'
CIPHER_MAP[0x3E] = 'TLS_DH_DSS_WITH_AES_128_CBC_SHA256'
CIPHER_MAP[0x3F] = 'TLS_DH_RSA_WITH_AES_128_CBC_SHA256'
CIPHER_MAP[0x40] = 'TLS_DHE_DSS_WITH_AES_128_CBC_SHA256'
CIPHER_MAP[0x67] = 'TLS_DHE_RSA_WITH_AES_128_CBC_SHA256'
CIPHER_MAP[0x68] = 'TLS_DH_DSS_WITH_AES_256_CBC_SHA256'
CIPHER_MAP[0x69] = 'TLS_DH_RSA_WITH_AES_256_CBC_SHA256'
CIPHER_MAP[0x6A] = 'TLS_DHE_DSS_WITH_AES_256_CBC_SHA256'
CIPHER_MAP[0x6B] = 'TLS_DHE_RSA_WITH_AES_256_CBC_SHA256'

CIPHER_MAP[0x18] = 'TLS_DH_anon_WITH_RC4_128_MD5'
CIPHER_MAP[0x1B] = 'TLS_DH_anon_WITH_3DES_EDE_CBC_SHA'
CIPHER_MAP[0x34] = 'TLS_DH_anon_WITH_AES_128_CBC_SHA'
CIPHER_MAP[0x3A] = 'TLS_DH_anon_WITH_AES_256_CBC_SHA'
CIPHER_MAP[0x6C] = 'TLS_DH_anon_WITH_AES_128_CBC_SHA256'
CIPHER_MAP[0x6D] = 'TLS_DH_anon_WITH_AES_256_CBC_SHA256'
