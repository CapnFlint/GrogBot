import logging
import random
import time
import threading

import utils.twitch_utils as twitch
import utils.db_utils as db

import modules.overlay.overlay as overlay

from config.strings import strings

class follows(threading.Thread):
    def __init__(self, grog):
        threading.Thread.__init__(self)
        self.connMgr = grog.connMgr
        self.charMgr = grog.charMgr
        self.name = "Follow-Monitor"
        logging.info("Follow monitor initialized")

    def run(self):
        logging.info("Follow monitor started")
        cooldown = 5
        while 1:
            first = True
            time.sleep(cooldown)
            follows = twitch.get_latest_follows(100)

            ids = twitch.get_ids(follows)
            new = []
            if ids:
                first = True
                for user in ids.keys():
                    if not self.charMgr.follows_me(ids[user]):
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
