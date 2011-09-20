from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor, defer


class EveServer(Protocol):
    """
        Eve reads all the messages between Bob and Alice and can even edit them
        within a time window
    """

    def __init__(self):
        self.buffer = []
        self.timeouts = []
        self.packetcount = 0
        self.edit = False

    def connectionMade(self):
        """
            Inform BobProxy and AliceProxy that Eve is around. Ensure that
            there can be only one Eve connected.
        """
        if not self.factory.eve:
            self.factory.eve.append(self)
            print "Eve is here"
            self.transport.write("Hello Eve!\n")
        else:
            self.transport.write('There can be only one Eve eavesdropping at '\
                                 'any time\r\n')
            self.transport.loseConnection()

    def connectionLost(self, reason):
        """
            When Eve drops the line, the communication between Bob and Alice
            resumes without delays
        """
        self.factory.eve.pop()
        print "Eve is gone"

    def dataReceived(self, data):
        """
            Data sent by Eve will replace the buffered data
        """
        if len(self.buffer):
            if self.edit:  # edit message
                (packetNo, olddata, source, target) = self.buffer.pop()
                target.write(data)
                print "Eve changed some data"
                self.transport.write("%d: OK! Edited\n" % packetNo)
                self.edit = False
                self.ask()
            elif data.startswith('e'):  # mark message for editing
                self.edit = True
            elif data.startswith('f'):  # forward it
                (packetNo, olddata, source, target) = self.buffer.pop()
                target.write(olddata)
                self.transport.write("%d: OK! Forwarded\n" % packetNo)
                self.ask()
            elif data.startswith('b'):  # block it
                self.buffer.pop()
                self.ask()
            else:  # invalid input, ask again
                self.transport.write("%d: (f)orward, (e)dit, (b)lock? "
                                     % self.buffer[-1][0])

    def intercept(self, data, source, target):
        """
            Put message in Eve's buffer. If it's the only message in the buffer
            ask Eve what to do with it. Otherwise wait for the rest of the
            buffered messages to be processed
        """
        self.buffer.insert(0, (self.packetcount, data, source, target))
        if len(self.buffer) == 1:
            self.ask()
        self.packetcount += 1

    def ask(self):
        """
            Get the next message in the buffer and ask Eve if it should be
            forwarded, edited, or blocked
        """
        if len(self.buffer):
            (packetNo, data, source, target) = self.buffer.pop()
            if 'Client' in str(source):
                self.transport.write("%d: Intercepted message from %s:%d to "\
                                     "%s:%d \n---begin---\n%s\n----end----\n" \
                                     % (packetNo,
                                        source.addr[0],
                                        source.addr[1],
                                        target.server.interface,
                                        target.server.port, repr(data)))
            else:
                self.transport.write("%d: Intercepted message from %s:%d to "\
                                     "%s:%d \n---begin---\n%s\n----end----\n" \
                                     % (packetNo, source.server.interface,
                                        source.server.port, target.addr[0],
                                        target.addr[1], repr(data)))

            self.transport.write("%d: (f)orward it, (e)dit it, (b)lock it? " %
                                 packetNo)
            d = defer.Deferred()
            d.addCallback(self.timeout)
            reactor.callLater(self.factory.delay, d.callback,
                              (packetNo, data, source, target))
            self.buffer.append((packetNo, data, source, target))

    def timeout(self, (packetNo, data, source, target)):
        if len(self.buffer) and \
        (packetNo, data, source, target) == self.buffer[-1] and \
        not self.edit:
            self.transport.write("\n%d: timed out. Auto-forwarding\n"
                                 % packetNo)
            target.write(data)
            self.buffer.remove((packetNo, data, source, target))
            self.ask()


class EveServerFactory(Factory):
    protocol = EveServer

    def __init__(self, delay, eve):
        self.delay = delay
        self.eve = eve
