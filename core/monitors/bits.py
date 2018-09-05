import urllib2
import urllib
import json
import time
import thread
import logging

from twitchsocket import twitchsocket


class bits():
    def __init__(self, grog):
        topic = "channel-bits-events.44322889"
        ts = twitchsocket(topic, self.handler)
        logging.info("Bits monitor initialized")

    def handler(self, message):
        logging.info(message['message'])
