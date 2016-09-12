import logging
import random
import time
import thread


class events():
    def __init__(self, mgr):
        self.eventMgr = mgr
        logging.info("Event thread initialized")

    def events_thread(self):
        while 1:
            cooldown = random.choice(range(10*60, 30*60))
            time.sleep(cooldown)
            self.eventMgr.random_event()

    def start(self):
        thread.start_new_thread(self.events_thread, ())
        logging.info("Event thread started")
