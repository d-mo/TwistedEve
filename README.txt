Eve has the twisted habit of eavesdropping all communication between her
friends, Bob and Alice. But she also hates being gossiped upon, so she wants to
be able to edit any message sent between Bob and Alice on real time, in order to
replace it with a more acceptable one.

TwistedEve is a tool that facilitates eavesdropping and
man-in-the-middle attacks.

Start TwistedEve as a proxy server on any host/port and ask it to forward
incoming traffic to the target server (e.g. Alice's mail server). Then make
sure that the target client (e.g. Bob's mail client) connects through
TwistedEve (e.g. social engineering, ARP spoofing, etc).

TwistedEve will then log all messages exchanged between the target client and
the target server and will also provide a backdoor port that can be used to
monitor and edit messages in real time. When an eavesdropper is connected,
TwistedEve will delay all messages for a configurable amount of time (3 seconds
by default). During that time the eavesdropper will have the option to forward,
edit, or block the message. After that time the message will be forwarded
automatically unless the eavesdropper chose to edit or block it.

TwistedEve uses Twisted, the asynchronous networking framework and TLSlite, a
native implementation of SSL/TLS in Python.
