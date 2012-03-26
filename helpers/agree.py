#!/usr/bin/env python 
#
# A  simple server that agrees to everything the client says
# 

from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor

### Protocol Implementation
class Echo(Protocol):
    def dataReceived(self, data):
        """
        As soon as any data is received, write it back.
        """
        self.transport.write("I agree that " + data)


def main():
    f = Factory()
    f.protocol = Echo
    reactor.listenTCP(50000, f)
    reactor.run()

if __name__ == '__main__':
    main()
