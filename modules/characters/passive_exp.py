import logging
import thread
import random
import time

from datetime import datetime, timedelta

import utils.twitch_utils as twitch

class passive_exp():
    def __init__(self, mgr):
        self.exp_timer = 60 * 1
        self.charMgr = mgr
        self.active_viewers = {}
        self.passive_viewers = []

        self.charMgr.grog.msgProc.register_hook(self.boost)


    def boost(self, mproc, msg):
        #when they talk, add them to active_viewers
        now = datetime.now()
        logging.debug(msg['sender'] + " activated BOOST!")
        self.active_viewers[msg['sender']] = now


    def passive_exp(self, delay):
        while 1:
            time.sleep(delay)
            viewers = twitch.get_viewers()
            now = datetime.now()
            for char in self.active_viewers:
                if char in viewers:
                    if (now - self.active_viewers[char]) > timedelta(minutes=1):
                        logging.debug(char + "'s BOOST expired...'")
                        del self.active_viewers[char]
                        if not char in self.passive_viewers:
                            self.passive_viewers.append(char)
                    else:
                        viewers.remove(char)
                else:
                    del self.active_viewers[char]
                    if not char in self.passive_viewers:
                        self.passive_viewers.append(char)
            for char in self.passive_viewers:
                if char in viewers:
                    viewers.remove(char)

            logging.debug("Basic exp for: " + ", ".join(viewers))
            logging.debug("passive exp for: " + ", ".join(self.passive_viewers))
            logging.debug("active exp for: " + ", ".join(self.active_viewers.keys()))
            self.charMgr.give_exp(2, viewers)
            self.charMgr.give_exp(5, self.passive_viewers)
            self.charMgr.give_booty(1, self.passive_viewers)
            self.charMgr.give_exp(10, self.active_viewers.keys())
            self.charMgr.give_booty(2, self.active_viewers.keys())
            logging.info("Current viewer count: " + str(twitch.get_viewcount()))


    def start(self):
        thread.start_new_thread(self.passive_exp, (self.exp_timer,))
