from helper import *
import modules.overlay.overlay as overlay

import time

@processes('!ship')
def command_ask(self, sender, args):
    try:
        self.ship_cooldowns
    except:
        self.ship_cooldowns = {}
    char = self.charMgr.load_character(sender)
    if char['subscriber']:
        now = time.time()
        if sender in self.ship_cooldowns.keys():
            if now - self.ship_cooldowns[sender] < 300:
                return
            else:
                del self.ship_cooldowns[sender]
        if char['ship'] > 0:
            ship = char['ship']
        else:
            ship = char['sub_count']
        overlay.ship("join", sender, ship)
        self.ship_cooldowns[sender] = now
