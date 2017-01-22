import logging
import random
import time
import thread

import utils.twitch_utils as twitch
import utils.db_utils as db

import modules.overlay.overlay as overlay

from config.strings import strings

class follows():
    def __init__(self, grog):
        self.connMgr = grog.connMgr
        self.charMgr = grog.charMgr
        logging.info("Follow monitor initialized")

    def follow_thread(self):
        cooldown = 5
        while 1:
            first = True
            time.sleep(cooldown)
            follows = twitch.get_latest_follows(100)
            new = []
            if follows:
                first = True
                for user in follows:
                    user = user.encode('utf-8')
                    if user:
                        if not self.charMgr.follows_me(user):
                            logging.info("[NEW FOLLOWER] " + user)
                            overlay.alert_follow(user, first)
                            new.append(user)
                            self.charMgr.give_booty(25, [user])
                            self.charMgr.add_follower(user)
                            first = False
            if new:
                self.connMgr.send_message(strings["FOLLOW_WELCOME"].format(names=", ".join(new)))
                stat = db.add_stat('sessionFollowers', len(new))
                overlay.update_stat('follows', stat)
                #overlay.update_timer(2 * len(new))

    def start(self):
        thread.start_new_thread(self.follow_thread, ())
        logging.info("Follow monitor started")
