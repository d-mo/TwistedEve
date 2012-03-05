import sys
import optparse

from time import sleep

from twisted.internet import reactor
from twisted.python import log

from twistedeve.attackshell import AttackShellFactory
from twistedeve.client2server import Client2ServerProxyFactory


def main():
    
    # Parse command line options
    parser = optparse.OptionParser()
    
    parser.add_option('-b', '--bind', dest='bind', help='address to bind to',
                      metavar='HOST:PORT', default='0.0.0.0:8000')
    parser.add_option('-f', '--forward', dest='target',
                      help='target host and port to forward data',
                      metavar='HOST:PORT')
    parser.add_option('-a', '--attack', dest="attacker",
                      help='host and port for the attacker to connect to',
                      metavar="HOST:PORT", default='0.0.0.0:31337')
    parser.add_option('-d', '--delay', dest='delay',
                      help='number of seconds to delay messages if attacker ' \
                           'is connected', default='3')
    parser.add_option('-k', '--key', dest='key',
                      help='TLS private key file', default=None)
    parser.add_option('-s', '--script', dest='script',
                      help='script file for auto-filtering', default=None)
    
    (options, args) = parser.parse_args()

    if not options.target:
        parser.print_help()
        sys.exit(1)

    target = options.target.split(':')

    if len(target) == 2:
        try:
            target[1] = int(target[1])
        except ValueError:
            target[1] = None

    if len(target) != 2 or not target[0] or not target[1]:
        print 'Target \'%s\' not in format HOST:PORT' % options.target
        sys.exit(1)

    options.target = tuple(target)

    try:
        delay = int(options.delay)
    except ValueError:
        print "Invalid delay value"
        sys.exit(1)

    if options.bind:
        bind = options.bind.split(':')

        if len(bind) == 2:
            address = bind[0]
            port = int(bind[1])
        else:
            address = '0.0.0.0'
            port = int(bind[0])

        try:
            options.bind = (address, int(port))
        except ValueError:
            print 'Bind address \'%s\' not in format HOST:PORT' % options.bind
            sys.exit(1)
    else:
        options.bind = ('0.0.0.0', 8000)

    if options.attacker:
        attacker = options.attacker.split(':')

        if len(attacker) == 2:
            address = attacker[0]
            port = int(attacker[1])
        else:
            address = '0.0.0.0'
            port = int(attacker[0])

        try:
            options.attacker = (address, int(port))
        except ValueError:
            print 'Attacker address \'%s\' not in format HOST:PORT' % \
                    options.bind
            sys.exit(1)
    else:
        options.attacker = ('0.0.0.0', 31337)

    # open key file
    privateKey = None
    if options.key:
        try:
            s = open(options.key).read()
            x509 = X509()
            x509.parse(s)
            certChain = X509CertChain([x509])
            s = open(options.key).read()
            privateKey = parsePEMKey(s, private=True)
            print "TLS key loaded"
        except Exception as e:
            print "Invalid TLS key file"
            sys.exit(1)
    
    if options.script:
        try:
            ns = {'filter': None}
            f = open(options.script)
            code = f.read()
            exec code in ns
            if not ns['filter']:
                print "paparia"
        except Exception as e:
            print e
            print options.script
            print "Invalid script file. Check out the examples in the scripts directory"
            sys.exit(1)
            
    filter = ns['filter']
    attacker = []

    log.startLogging(sys.stdout)

    client2server_proxy = Client2ServerProxyFactory(options.target[0], options.target[1], attacker)
    attack_server = AttackShellFactory(delay, filter, attacker)
    reactor.listenTCP(options.bind[1], client2server_proxy,
                      interface=options.bind[0])
    reactor.listenTCP(options.attacker[1], attack_server,
                      interface=options.attacker[0])
    reactor.run()
