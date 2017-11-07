from helper import *
import utils.twitch_utils as utils
import time

last_exp = 0

#@processes('!exp', PERM_MOD)
def command_exp(self, sender, args):
    global last_exp
    now = time.time()
    if int(now - last_exp) > 10: # Flood protection on !exp command
        last_exp = now

        amount = 10

        user = None
        if len(args) > 1:
            user = args[0]
            amount = args[1]
        elif args:
            amount = args[0]

        try:
            amount = int(amount)
        except ValueError:
            amount = 10

        if user and user in utils.get_viewers():
            self.connMgr.send_message('Bounty for ' + user + '!!!')
            self.charMgr.give_exp(amount, [user])
            self.charMgr.give_booty(amount / 5, [user])
        else:
            self.connMgr.send_message('Bounty for ALL!!!')
            self.charMgr.give_exp(amount)
            self.charMgr.give_booty(amount / 5)

    else:
        self.connMgr.send_message("Whoa! Slow down there mateys! (command flood protection)")
