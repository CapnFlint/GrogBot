import logging
import random
import time
import thread

from config.strings import strings

import utils.tip_utils as tip_utils

class tips():
    def __init__(self, owner):
        self.latest_tips = tips.get_latest_tips()
        self.connMgr = owner.connMgr

        for tip in self.latest_tips:
            if not tip['name']:
                tip['name'] = "Anonymous"
        logging.info("Tip monitor initialized")

    def tip_thread(self):
        cooldown = 10
        while 1:
            time.sleep(cooldown)
            tips = tip_utils.get_latest_tips()
            if tips:
                for tip in tips:
                    if not tip['name']:
                        tip['name'] = "Anonymous"
                    if tip not in self.latest_tips:
                        logging.info("[TIP] " + tip['name'] + " - " + str(tip['amount']))
                        overlay.alert_tip(tip['name'], tip['amount'], tip['message'])
                        to = ""
                        if tip['type'] == 1:
                            to = " to extra-life"
                        self.connMgr.send_message(strings['TIP_MESSAGE'].format(name=tip['name'], amount=format(tip['amount'], '.2f'), to=to))
                        if tip['message']:
                            self.connMgr.send_message("They left the message: " + tip['message'])

                self.latest_donations = donations

    def start(self):
        thread.start_new_thread(self.tip_thread, ())
        logging.info("Tip monitor started")
