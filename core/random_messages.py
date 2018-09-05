import thread
import time
import random
import logging

import utils.db_utils as db


# -----[ Random Messages Thread ]-----------------------------------------------
class random_messages():
    def __init__(self, grog):
        self.current = 0
        self.grog = grog

    def message_thread(self):
        while 1:
            cooldown = 10 * 60
            time.sleep(cooldown)
            message = db.get_message(self.current)
            if not message:
                self.current = 0
                message = db.get_message(self.current)
            logging.debug(message)
            self.current += 1

            if message['command']:
                self.grog.msgProc.run_command(message['command'])
            else:
                self.grog.connMgr.send_message(message['text'])

    def start(self):
        thread.start_new_thread(self.message_thread, ())

# ------------------------------------------------------------------------------
