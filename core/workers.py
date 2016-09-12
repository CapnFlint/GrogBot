import thread
import time
import random

import modules.overlay.overlay as overlay
import utils.twitch_utils as twitch
import utils.donation_utils as donor_utils
import utils.teespring as tee_utils
import utils.twitter as twitter_utils
import utils.db_utils as db




# -----[ Random Messages Thread ]-----------------------------------------------
class messages():
    def __init__(self, grog):
        self.current = 0
        self.grog = grog
        self.messages = [
          "Follow the Cap'n on Twitter! - http://twitter.com/Capn_Flint",
          "YARRRR!",
          "If you're having fun, please consider hitting that follow button!",
          "Hey, you... yes, you. You're AWESOME!",
          "Check out http://youtube.com/c/CapnFlintTV for Highlights and Tutorials!",
          "Say hello! We don't bite!",
          "If you wish to give a little ongoing support to the Capn, you can now subscribe to him! Check it out here: https://www.twitch.tv/capn_flint/subscribe",
          "Why aren't you following yet? Huh? HUH?!",
          "If you have any questions, speak up. The Cap'n loves to help!"
        ]

    def message_thread(self):
        while 1:
            cooldown = 10 * 60
            time.sleep(cooldown)
            message = db.get_message(self.current)
            if not message:
                self.current = 0
                message = db.get_message(self.current)
            print message
            self.current += 1
            #message = self.messages.pop(0)
            #self.messages.append(message)
            if message['command']:
                self.grog.msgProc.run_command(message['command'])
            else:
                self.grog.connMgr.send_message(message['text'])

    def start(self):
        thread.start_new_thread(self.message_thread, ())

# ------------------------------------------------------------------------------
class followers():
    def __init__(self, owner):
        self.connMgr = owner.connMgr
        self.charMgr = owner.charMgr
        print "[WORKERS] Follower worker init"

    def follow_thread(self):
        cooldown = 5
        print "[WORKERS] Follower worker started"
        while 1:
            first = True
            time.sleep(cooldown)
            follows = utils.get_latest_follows(25)
            new = []
            if follows:
                first = True
                for user in follows:
                    if user:
                        if not self.charMgr.follows_me(user):
                            print "[NEW FOLLOWER] " + user
                            overlay.alert_follow(user, first)
                            new.append(user)
                            self.charMgr.give_booty(25, [user])
                            self.charMgr.add_follower(user)
                            first = False
            if new:
                self.connMgr.send_message("Welcome to our new Crewmembers: " + ", ".join(new) +"! Have some welcome capnBooty ! R)")
                stat = db.add_stat('sessionFollowers', len(new))
                overlay.update_stat('follows', stat)

    def start(self):
        thread.start_new_thread(self.follow_thread, ())

class tips():
    def __init__(self, owner):
        self.latest_donations = donor_utils.get_latest_donations()
        self.connMgr = owner.connMgr

        for donation in self.latest_donations:
            if not donation['name']:
                donation['name'] = "Anonymous"

    def tip_thread(self):
        cooldown = 10
        while 1:
            time.sleep(cooldown)
            donations = donor_utils.get_latest_donations()
            if donations:
                for donation in donations:
                    if not donation['name']:
                        donation['name'] = "Anonymous"
                    if donation not in self.latest_donations:
                        print "[NEW] " + donation['name']
                        overlay.alert_donate(donation['name'], donation['amount'])
                        to = ""
                        if donation['type'] == 1:
                            to = " to extra-life"
                        self.connMgr.send_message(donation['name'] + " has donated $" + format(donation['amount'], '.2f') + to + "! Give them some love!!!")
                        if donation['message']:
                            self.connMgr.send_message("They left the message: " + donation['message'])

                self.latest_donations = donations

    def start(self):
        thread.start_new_thread(self.tip_thread, ())

class teespring():
    def __init__(self, owner, query, international = False):
        self.query = query
        self.intl = international
        self.count = tee_utils.get_orders(self.query, self.intl)

    def teespring_thread(self):
        cooldown = 35
        while 1:
            time.sleep(cooldown)
            count = tee_utils.get_orders(self.query, self.intl)
            if count > self.count:
                self.count += 1
                overlay.alert_teespring(self.count)

    def start(self):
        thread.start_new_thread(self.teespring_thread, ())

class twitter():
    def __init__(self, owner):
        self.count = 20
        self.latest_mentions = twitter_utils.get_latest_mentions(self.count)
        self.latest_retweets = twitter_utils.get_latest_retweets(self.count)

    def twitter_thread(self):
        cooldown = 120
        while 1:
            time.sleep(cooldown)
            new_mentions = twitter_utils.get_latest_mentions(self.count)
            new_retweets = twitter_utils.get_latest_retweets(self.count)
            if new_mentions:
                for mention in new_mentions:
                    if mention not in self.latest_mentions:
                        print "sending: " + str(mention)
                        overlay.twitter_mention(mention)
                self.latest_mentions = new_mentions
            if new_retweets:
                for retweet in new_retweets:
                    if retweet not in self.latest_retweets:
                        overlay.twitter_retweet(retweet)
                self.latest_retweets = new_retweets

    def start(self):
        thread.start_new_thread(self.twitter_thread, ())
