from helper import *
import time

# -----[ Milo Command ]---------------------------------------------------------

last_milo = 0

def feed_milo(self, uid):
    char = self.charMgr.load_character(uid)
    if char and char['booty'] >= 5:
        char['booty'] -= 5
        self.connMgr.send_message("Milo loved his Milo snax! Thanks! capnMilo Woof!")
        self.charMgr.save_character(char)
        return True
    else:
        self.connMgr.send_message("Sorry " + char['name'] + ", but you don't have enough booty to buy Milo snax!")
        return False

# ------------------------------------------------------------------------------

@processes('!milo')
def command_milo(self, data):
    global last_milo
    now = time.time()
    if int(now - last_milo) > 600: # Flood protection on !exp command
        if feed_milo(self, data['sender_id']):
            last_milo = now
    else:
        self.connMgr.send_message("Milo is a little full right now, but thanks for the offer!")
