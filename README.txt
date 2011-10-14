Introduction
===============
Eve has the twisted habit of eavesdropping all communication between her
friends, Bob and Alice. But she also hates being gossiped upon, so she wants to
be able to edit any message sent between Bob and Alice on real time, in order to
replace it with a more acceptable one.

TwistedEve is a tool that facilitates eavesdropping and
man-in-the-middle attacks.

Assuming that you are in a man-in-the-middle position between Bob and
Alice, you should be able to redirect all traffic from Bob's client that's
heading to Alice's server. Forward it to a port of your choice and start
TwistedEve on that port. TwistedEve will act as a proxy,
while logging all exchanged messages and providing you with a backdoor
to intercept and optionally edit the content of the messages.

When an eavesdropper is connected to the backdoor port (31337 by default),
TwistedEve will delay all messages for a configurable amount of time (3 seconds
by default). During that time the eavesdropper will have the option to forward,
edit, or block the message. After that time the message will be forwarded
automatically unless the eavesdropper chose to edit or block it.

TwistedEve uses Twisted, the asynchronous networking framework and TLSlite, a
native implementation of SSL/TLS in Python.

Installation
===============
It's recommended to install TwistedEve inside a Python virtualenv using pip or
easy_install:

    $ virtualenv te-env
    $ cd te-env
    $ ./bin/pip install git://github.com/d-mo/TwistedEve.git
    $ ./bin/twistedeve -b 0.0.0.0:8025 -f mail.google.com:25
    2011-10-13 22:10:57+0300 [-] Log opened.
    2011-10-13 22:10:57+0300 [-] twistedeve.bobproxy.BobProxyFactory starting on 8000
    2011-10-13 22:10:57+0300 [-] Starting factory <twistedeve.bobproxy.BobProxyFactory instance at 0x1017335f0>
    2011-10-13 22:10:57+0300 [-] twistedeve.eveserver.EveServerFactory starting on 31337
    2011-10-13 22:10:57+0300 [-] Starting factory <twistedeve.eveserver.EveServerFactory instance at 0x101733638>

You should now be able to connect to the backdoor port.

    $ telnet localhost 31337
    Trying 127.0.0.1...
    Connected to localhost.
    Escape character is '^]'.
    Hello Eve!


Usage
===============

Usage: twistedeve [options]

Options:
  -h, --help            show this help message and exit
  -b HOST:PORT, --bind=HOST:PORT
                        address to bind to
  -f HOST:PORT, --forward=HOST:PORT
                        target host and port to forward data
  -a HOST:PORT, --attack=HOST:PORT
                        host and port for the attacker to connect to
  -d DELAY, --delay=DELAY
                        number of seconds to delay messages if attacker is
                        connected
                        
