from helper import *
import utils.twitch_utils as utils
import time

last_exp = 0

@processes('!exp', PERM_MOD)
def command_exp(self, data):
    global last_exp
    now = time.time()
    args = data['args']
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

        logging.debug("USER: " + user)
        viewers = utils.get_viewers()
        logging.debug(viewers)
        if user and user in viewers:
            self.connMgr.send_message('Bounty for ' + user + '!!!')
            self.charMgr.give_exp(amount, [user])
            self.charMgr.give_booty(amount / 5, [user])
        else:
            self.connMgr.send_message('Bounty for ALL!!!')
            self.charMgr.give_exp(amount)
            self.charMgr.give_booty(amount / 5)

    else:
        self.connMgr.send_message("Whoa! Slow down there mateys! (command flood protection)")
