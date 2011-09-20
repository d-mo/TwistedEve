import sys
import optparse

from time import sleep

from twisted.internet import reactor
from twisted.python import log

from twistedeve.eveserver import EveServerFactory
from twistedeve.bobproxy import BobProxyFactory


def main():
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
    """
    parser.add_option('-t', '--tls', dest='tls',
                      help='[auto] start TLS or, [wait] for STARTTLS msg',
                      metavar = "[auto|wait]", default='wait')
    parser.add_option('-k', '--key', dest='key',
                      help='TLS key file', default=None)
    parser.add_option('-c', '--crt', dest='crt',
                      help='TLS certificate file', default=None)
    """
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

    """ctx = stx = False
    if options.key and options.crt:
        try:
            stx = ServerTLSContext(
                privateKeyFileName=options.key,
                certificateFileName=options.crt,
            )
            ctx = ClientTLSContext()
            print "TLS key and cert loaded"
        except Exception as e:
            print "Invalid TLS key and/or cert file"
    """

    eve = []

    log.startLogging(sys.stdout)

    bob_proxy = BobProxyFactory(options.target[0], options.target[1], eve)
    eve_server = EveServerFactory(delay, eve)
    reactor.listenTCP(options.bind[1], bob_proxy,
                      interface=options.bind[0])
    reactor.listenTCP(options.attacker[1], eve_server,
                      interface=options.attacker[0])
    reactor.run()
