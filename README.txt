Introduction
===============
Eve has the twisted habit of eavesdropping all communication between her
friends, Alice and Bob. But she also hates being gossiped upon, so she wants to
be able to edit any message sent between Alice and Bob in real time, in order to
replace it with a more acceptable one.

TwistedEve is a tool that facilitates eavesdropping and
man-in-the-middle attacks.

Assuming that you are in a man-in-the-middle position between Alice and
Bob, you should be able to redirect all traffic from Alice's client
heading to Bob's server. Forward it to a port of your choice and start
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
You can install like any Python egg using setuptools or pip, but it's better
to use buildout: 

    $ git clone https://d-mo@github.com/d-mo/TwistedEve.git 
    $ cd TwistedEve
    $ python bootstrap.py
    ...
    $ ./bin/buildout
    ...
    Updating _mr.developer.
    Updating eve.
    Updating py.    
    
Usage
===============

Usage: twistedeve [options]

Options:
  -h, --help            show this help message and exit
  -b HOST:PORT, --bind=HOST:PORT
                        address to bind to
  -t HOST:PORT, --target=HOST:PORT
                        target host and port to forward data
  -a HOST:PORT, --attack=HOST:PORT
                        host and port for the attacker to connect to
  -d DELAY, --delay=DELAY
                        number of seconds to delay messages if attacker is
                        connected
  -k KEY, --key=KEY     TLS private key file
  -c CHAIN, --certchain=CHAIN
                        X.509 cert chain
  -f FILTER, --filter=FILTER
                        script file for auto-filtering


Examples
===============
Let's first start a simple server that agrees to everything it's told:

    $ ./bin/python helpers/agree.py &
    $ nc localhost 50000
    Eve is cool
    I agree that Eve is cool
    ^C

Manual mode
---------------
    
Now let's start up TwistedEve in manual mode to listen at port 40000 and 
forward to port 50000

    $ ./bin/twistedeve -b localhost:40000 -t localhost:50000
    2012-03-26 01:58:41+0300 [-] Log opened.
    2012-03-26 01:58:41+0300 [-] Client2ServerProxyFactory starting on 40000
    2012-03-26 01:58:41+0300 [-] Starting factory <twistedeve.client2server.Client2ServerProxyFactory instance at 0x1006cc4d0>
    2012-03-26 01:58:41+0300 [-] AttackShellFactory starting on 31337
    2012-03-26 01:58:41+0300 [-] Starting factory <twistedeve.attackshell.AttackShellFactory instance at 0x1018325a8>

We should now be able to telnet to the backdoor port (31337 by default) in 
order to edit, block, or forward messages in real time.

    $ telnet localhost 31337
    Trying 127.0.0.1...
    Connected to localhost.
    Escape character is '^]'.
    Hello Eve!

Automatic mode
---------------

We can also configure TwistedEve to use an automatic filter script, like the
censor.py in ./filters/ directory

    $ ./bin/twistedeve -b localhost:40000 -t localhost:50000 -f filters/censor.py
    Loaded censoring filter
    ...
    
If we now send a message to port 40000 that contains bad words about Eve, the
bad words will be replaced with nice ones before reaching the server:

    $ netcat localhost 40000
    Eve is a ugly bitch
    I agree that Eve is a georgeous mermaid
    ^D
    
Check out the filters folder for examples on making your own filters.

Don't forget to shut down the agree.py server when finished:

    $ fg
    ./bin/python helpers/agree.py
    ^C
    $


TLS filtering
--------------
You can also use TwistedEve against TLS connections by supplying a server key
and a certificate chain.

Let's first start a TLS enabled server that agrees to everything it's told:

    $ ./bin/python helpers/tlsagree.py &
    
Now let's load our filter over TLS, effectively running a man in the middle
attack using our self signed certificate:

    $ ./bin/twistedeve -b localhost:40000 -t localhost:50000 \
           -k helpers/server.key -c helpers/server.crt -f filters/censor.py
           
Let's send a message over TLS to confirm that it's filtered:

    $ ./bin/python helpers/tlsnc.py localhost 40000
    Eve is fat and stupid
    I agree that Eve is fit and smart
    ^C

TLS version & ciphersuite detection
------------------------------------
You can use the tlsinfo.py filter script to detect the TLS version and the
cipher suites that are offered by the client and selected by the server:

    $ ./bin/twistedeve -b localhost:40000 -t localhost:50000 \
            -k helpers/server.key -c helpers/server.crt -f filters/tlsinfo.py 
    TLS key loaded
    2012-03-26 03:49:47+0300 [-] Log opened.
    2012-03-26 03:49:47+0300 [-] Client2ServerProxyFactory starting on 40000
    2012-03-26 03:49:47+0300 [-] Starting factory <twistedeve.client2server.Client2ServerProxyFactory instance at 0x1006cc4d0>
    2012-03-26 03:49:47+0300 [-] AttackShellFactory starting on 31337
    2012-03-26 03:49:47+0300 [-] Starting factory <twistedeve.attackshell.AttackShellFactory instance at 0x10187a4d0>
    2012-03-26 03:49:49+0300 [twistedeve.client2server.Client2ServerProxyFactory] Starting factory <twistedeve.server2client.Server2ClientProxyFactory instance at 0x10187c248>
    2012-03-26 03:49:49+0300 [Client2ServerProxy,0,127.0.0.1] Client supports TLS version: (3, 2)
    2012-03-26 03:49:49+0300 [Client2ServerProxy,0,127.0.0.1] Client supports ciphersuites: [255, 53, 47, 5]
    2012-03-26 03:49:49+0300 [Server2ClientProxy,client] Server selected TLS version: (3, 2)
    2012-03-26 03:49:49+0300 [Server2ClientProxy,client] Server selected ciphersuite: 53
    2012-03-26 03:49:49+0300 [Server2ClientProxy,client] Stopping factory <twistedeve.server2client.Server2ClientProxyFactory instance at 0x10187c248>



                        
