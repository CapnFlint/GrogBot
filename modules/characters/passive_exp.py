import thread
import time
import random

class passive_exp():
    def __init__(self, grog):
        self.exp_timer = 60 * 5
        self.charMgr = grog.charMgr

    def passive_exp(self, delay):
        while 1:
            time.sleep(delay)
            self.charMgr.give_exp(5)
            self.charMgr.give_booty(1)
            print "Current viewer count: " + str(utils.get_viewcount())

    def start(self):
        thread.start_new_thread(self.passive_exp, (self.exp_timer,))
