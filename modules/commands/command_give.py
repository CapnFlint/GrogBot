from helper import *
import utils.twitch_utils as utils

@processes('!give')
def command_give(self, sender, args):
    try:
        if len(args) > 1:
            print args
            recipient = args[0].lower()
            if recipient == sender:
                self.connMgr.send_message("You can't send money to yourself!")
                return
            try:
                amount = int(args[1])
            except:
                amount = 0

            if amount <= 0:
                self.connMgr.send_message("Sorry " + sender + ", that isn't a valid amount.")
                return

            if recipient in utils.get_viewers():
                source = self.charMgr.load_character(sender)
                if source['booty'] >= amount:
                    target = self.charMgr.load_character(recipient)
                    target['booty'] += amount
                    source['booty'] -= amount
                    self.charMgr.save_character(target)
                    self.charMgr.save_character(source)
                    self.connMgr.send_message(str(amount) + ' ' + self.language['currency'] + 's sent to ' + recipient + '! Thanks ' + sender + '!')
                else:
                    self.connMgr.send_message('Sorry ' + sender + ", you don't have enough for that.")
            else:
                self.connMgr.send_message('Sorry, ' + recipient + " isn't here...")
        else:
            self.connMgr.send_message("To send money, it's: !give name amount, e.g. !give capn_flint 50")
    except:
        self.connMgr.send_message("That is an invalid amount. Please try again.")
