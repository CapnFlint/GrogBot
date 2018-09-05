import logging
import random
import time
import threading


class EventThread(threading.Thread):
    def __init__(self, threadID, mgr):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.threadID = threadID
        self.eventMgr = mgr
        logging.info("Event thread initialized")

    def run(self):
        logging.info("Event thread started")
        while 1:
            cooldown = random.choice(range(10*60, 30*60))
            time.sleep(cooldown)
            self.eventMgr.random_event()
