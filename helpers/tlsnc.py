#!/usr/bin/env python
#
# Simple python implementation of netcat over TLS using TLSlite
#

import socket
import sys
import fileinput
from time import sleep
from tlslite.api import *

def netcat(hostname, port, content):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((hostname, port))
    conn = TLSConnection(s)
    conn.handshakeClientCert()
    conn.sendall(content)
    while 1:
        try:
            data = conn.recv(1024)
        except Exception as e:
            break
        if data == "":
            break
        print data
    #s.shutdown(socket.SHUT_WR)
    conn.close()
    s.close()
    
if __name__ == '__main__':
    try:
        if len(sys.argv) > 1:
            host = sys.argv[1]
            port = sys.argv[2]
        else:
            host, port = ('localhost', '40000')
        while True:
            try:
                line = raw_input()
            except Exception as e:
                break
            if not line:
                break
            netcat(host, int(port), line)
    except ValueError as e:
        print "error: %s" % e