from helper import *
import utils.twitter as twitter
import random

@processes("!tweet")
@processes("!rt")
def command_tweet(self, sender, args):
    messages = [
        "If you want to support the stream, please like and retweet: ",
        "capnMilo loves retweets! - ",
        "Retweet the stream, for great glory!!! - "
    ]
    self.connMgr.send_message(random.choice(messages) + twitter.get_latest_tweet())
