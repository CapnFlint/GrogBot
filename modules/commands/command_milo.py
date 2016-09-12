from helper import *
import time

# -----[ Milo Command ]---------------------------------------------------------

last_milo = 0

def feed_milo(self, name):
    char = self.charMgr.load_character(name)
    if char['booty'] >= 5:
        char['booty'] -= 5
        self.connMgr.send_message("Milo loved his Milo snax! Thanks! capnMilo Woof!")
        self.charMgr.save_character(char)
        return True
    else:
        self.connMgr.send_message("Sorry " + name + ", but you don't have enough booty to buy Milo snax!")
        return False

# ------------------------------------------------------------------------------

@processes('!milo')
def command_milo(self, sender, args):
    global last_milo
    now = time.time()
    if int(now - last_milo) > 600: # Flood protection on !exp command
        if feed_milo(self, sender):
            last_milo = now
    else:
        self.connMgr.send_message("Milo is a little full right now, but thanks for the offer!")
