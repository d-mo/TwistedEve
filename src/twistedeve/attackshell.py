from binascii import a2b_qp, b2a_qp
from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor, defer


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


class AttackShell(Protocol):
    """
        Once the attacker is connected to the AttackShell, she can read
        and edit any message between the client and the server.
        
        There are two attack modes. In manual mode the attacker can edit
        messages by hand within a predefined time window. In auto mode the
        editing is done by a script.
    """

    def __init__(self):
        self.buffer = []
        self.timeouts = []
        self.packetCount = 0
        self.edit = False
        self.mode = None


    def connectionMade(self):
        """
            Inform the Client2Server and Server2Client proxies that an 
            attacker is around.
            
            Ensure that there can be only one attacker connected.
        """
        if not self.factory.attacker:
            self.factory.attacker.append(self)
            print bcolors.OKBLUE + "Eve is here" + bcolors.ENDC
            self.transport.write(bcolors.OKBLUE + "Hello Eve!\n" + bcolors.ENDC)
            if self.factory.filter:
                self.transport.write(bcolors.OKGREEN + "Select (a)uto or (m)anual mode:\n" + bcolors.ENDC)
            else:
                self.mode = 'manual'
        else:
            self.transport.write(bcolors.FAIL + 'There can be only one attacker at '\
                                 'any time\r\n' + bcolors.ENDC)
            self.transport.loseConnection()


    def connectionLost(self, reason):
        """
            When the attacker drops the line, the communication between the
            client and the server resumes without delays
        """
        self.factory.attacker.pop()
        print bcolors.OKBLUE + "Eve is gone" + bcolors.ENDC


    def dataReceived(self, data):
        """
            Data sent by the attacker will replace the buffered data
        """
        if not self.mode:
            if data.startswith('a'):
                self.transport.write(bcolors.OKBLUE + "Automatic mode selected. Sit back and check the script's output\n" + bcolors.ENDC)
                self.mode = 'auto'
            elif data.startswith('m'):
                self.transport.write(bcolors.OKBLUE + "Manual mode selected.\n" + bcolors.ENDC)
                self.mode = 'manual'
            else:
                self.transport.write(bcolors.FAIL + "Invalid option\n" + bcolors.ENDC)
                self.transport.write(bcolors.OKGREEN + "Select (a)uto or (m)anual mode:\n" + bcolors.ENDC)
                
        elif self.mode == 'manual' and len(self.buffer):
            
            if self.edit:  # edit message
                (packetNo, olddata, source, target) = self.buffer.pop()
                target.write(a2b_qp(data))
                print bcolors.WARNING + "Eve changed some data: " + bcolors.ENDC + "%s" % data
                self.transport.write(bcolors.OKBLUE + ("%d: OK! Edited\n" % packetNo) + bcolors.ENDC)
                self.edit = False
                self.ask()
                
            elif data.startswith('e'):  # mark message for editing
                self.edit = True
                
            elif data.startswith('f'):  # forward it
                (packetNo, olddata, source, target) = self.buffer.pop()
                target.write(olddata)
                self.transport.write(bcolors.OKBLUE + ("%d: OK! Forwarded\n" % packetNo) + bcolors.ENDC)
                self.ask()
                
            elif data.startswith('b'):  # block it
                self.buffer.pop()
                self.ask()
                
            else:  # invalid input, ask again
                self.transport.write(bcolors.OKGREEN + ("%d: (f)orward, (e)dit, (b)lock? "
                                     % self.buffer[-1][0]) + bcolors.ENDC)
                
        elif self.mode == 'auto':
            pass


    def intercept(self, data, source, target):
        """
            Put message in the attacker's buffer. If it's the only message in
            the buffer ask the attacker what to do with it. Otherwise wait for
            the rest of the buffered messages to be processed
        """
        self.buffer.insert(0, (self.packetCount, data, source, target))
        if len(self.buffer) == 1:
            if self.mode == 'manual':
                self.ask()
            elif self.mode == 'auto':
                self.act()
                
        self.packetCount += 1


    def act(self):
        """
            Call the imput filter
        """
        while len(self.buffer):
            (packetNo, dataIn, source, target) = self.buffer.pop()
            dataOut = self.factory.filter(packetNo, dataIn, source, target)
            if dataOut != dataIn:
                if self.factory.attacker:
                    self.transport.write("\n%d: edited message\n" % packetNo)
                    self.transport.write("<input>%s</input>\n" % dataIn)
                    self.transport.write("<output>%s</output>\n" % dataOut)      
                print "\n%d: edited message\n" % packetNo
                print "<input>%s</input>\n" % dataIn
                print "<output>%s</output>\n" % dataOut
        
    def ask(self):
        """
            Get the next message in the buffer and ask the attacker if it 
            should be forwarded, edited, or blocked
        """
        if len(self.buffer):
            (packetNo, data, source, target) = self.buffer.pop()
            if 'Client2Server' in str(source):
                self.transport.write("\n%d: Intercepted message from client"\
                                     "\n---begin---\n%s\n----end----\n" \
                                     % (packetNo,
                                        b2a_qp(data)))
            else:
                self.transport.write("%d: Intercepted message from server"\
                                     "\n---begin---\n%s\n----end----\n" \
                                     % (packetNo, b2a_qp(data)))

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


class AttackShellFactory(Factory):
    protocol = AttackShell

    def __init__(self, delay, filter, attacker):
        self.delay = delay
        self.filter = filter
        self.attacker = attacker
