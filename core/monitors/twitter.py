import logging
import random
import time
import thread

import utils.twitter as twitter

import modules.overlay.overlay as overlay

class twitter():
    '''TODO: Update/fix this code'''
    def __init__(self, owner):
        self.count = 20
        self.latest_mentions = twitter.get_latest_mentions(self.count)
        self.latest_retweets = twitter.get_latest_retweets(self.count)

    def twitter_thread(self):
        cooldown = 120
        while 1:
            time.sleep(cooldown)
            new_mentions = twitter.get_latest_mentions(self.count)
            new_retweets = twitter.get_latest_retweets(self.count)
            if new_mentions:
                for mention in new_mentions:
                    if mention not in self.latest_mentions:
                        logging.debug("sending: " + str(mention))
                        overlay.twitter_mention(mention)
                self.latest_mentions = new_mentions
            if new_retweets:
                for retweet in new_retweets:
                    if retweet not in self.latest_retweets:
                        overlay.twitter_retweet(retweet)
                self.latest_retweets = new_retweets

    def start(self):
        thread.start_new_thread(self.twitter_thread, ())
