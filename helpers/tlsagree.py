#!/usr/bin/env python 
#
# A  simple TLS server that agrees to everything the client says
# 

import socket 
from tlslite.api import *

host = 'localhost' 
port = 50000 
backlog = 5 
size = 1024 

#Load X.509 certChain and privateKey.
s = open("./helpers/server.crt").read()
x509 = X509()
x509.parse(s)
certChain = X509CertChain([x509])
s = open("./helpers/server.key").read()
privateKey = parsePEMKey(s, private=True)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.bind((host,port)) 
s.listen(backlog) 

while 1: 
    client, address = s.accept()
    conn = TLSConnection(client) 
    conn.handshakeServer(certChain=certChain, privateKey=privateKey)
    try:
        data = conn.recv(size)
    except Exception as e:
        data = None 
    if data:
        print "got data: " + data
        data = "I agree that " + data 
        conn.send(data) 
    conn.close()

