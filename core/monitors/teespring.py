import logging
import random
import time
import thread

import utils.teespring as tee_utils

import modules.overlay.overlay as overlay

class teespring():
    def __init__(self, owner, query, international = False):
        self.query = query
        self.intl = international
        self.count = tee_utils.get_orders(self.query, self.intl)
        logging.info("Teespring monitor initialized")

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
        logging.info("Teespring monitor started")
