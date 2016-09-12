from helper import *
import utils.db_utils as db
import time

last_sub = 0

@processes('!sub', PERM_MOD)
def command_sub(self, sender, args):
    global last_sub
    now = time.time()
    if int(now - last_sub) > 0: # Flood protection on !exp command
        last_sub = now
        if args:
            user = args[0]
            if user and self.charMgr.char_exists(user):
                db.make_sub(user)
                self.connMgr.send_message(user + " added as a subscriber!")
            else:
                self.connMgr.send_message("The user " + user + " does not exist...")
        else:
            self.connMgr.send_message("Usage: !sub <newsub>")
    else:
        self.connMgr.send_message("Whoa! Slow down there mateys! (command flood protection)")
