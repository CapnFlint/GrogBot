import urllib2
import urllib
import json
import time
import thread

from twitchsocket import twitchsocket


class bits():
    def __init__(self, grog):
        topic = "channel-bitsevents.44322889"
        ts = twitchsocket(topic, self.handler)
        logging.info("Bits monitor initialized")

    def handler(self, message):
        print message['message']
