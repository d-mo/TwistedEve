BAD_WORDS = ['stupid', 'fat', 'weird', 'ugly', 'bitch']
GOOD_WORDS = ['smart', 'fit', 'amazing', 'georgeous', 'mermaid']

def filter(packetNo, data, source, target):
    """
        This will replace any bad words with nice ones in any message
        that originates from the client and mentions Eve
    """
    if 'Client2Server' in str(source): # message coming from client
        # check if Eve is mentioned
        if 'Eve' in data:
            for b in BAD_WORDS:
                # replace any bad words with nice ones
                data = data.replace(b,GOOD_WORDS[BAD_WORDS.index(b)])        
        # forward the (possibly edited) data
        target.write(data)
    else:
        # message coming from trusted server, pass along
        target.write(data)
    return data

print "Loaded censoring filter"
