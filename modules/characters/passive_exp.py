import logging
import thread
import time
import random

import utils.twitch_utils as twitch

class passive_exp():
    def __init__(self, mgr):
        self.exp_timer = 60 * 5
        self.charMgr = mgr

    def passive_exp(self, delay):
        while 1:
            time.sleep(delay)
            self.charMgr.give_exp(5)
            self.charMgr.give_booty(1)
            logging.info("Current viewer count: " + str(twitch.get_viewcount()))

    def start(self):
        thread.start_new_thread(self.passive_exp, (self.exp_timer,))
