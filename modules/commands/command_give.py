from helper import *
import utils.twitch_utils as utils

from config.strings import strings

@processes('!give')
def command_give(self, data):
    args = data['args']
    try:
        if len(args) > 1:
            print args
            recipient = args[0].lower()
            if recipient == data['sender']:
                self.connMgr.send_message(strings['CMD_GIVE_SELF'])
                return
            try:
                amount = int(args[1])
            except:
                amount = 0

            if amount <= 0:
                self.connMgr.send_message(strings['CMD_GIVE_INVALID'].format(sender=data['sender']))
                return

            if recipient in utils.get_viewers():
                source = self.charMgr.load_character(data['sender'])
                if source['booty'] >= amount:
                    target = self.charMgr.load_character(recipient)
                    target['booty'] += amount
                    source['booty'] -= amount
                    self.charMgr.save_character(target)
                    self.charMgr.save_character(source)
                    self.connMgr.send_message(strings['CMD_GIVE_SENT'].format(amount=str(amount), recipient=recipient, sender=data['sender']))
                else:
                    self.connMgr.send_message(strings['CMD_GIVE_INSUFFICIENT'].format(sender=data['sender']))
            else:
                self.connMgr.send_message(strings['CMD_GIVE_MISSING'].format(recipient=recipient))
        else:
            self.connMgr.send_message(strings['CMD_GIVE_USAGE'])
    except:
        self.connMgr.send_message(strings['CMD_GIVE_INVALID'].format(sender=data['sender']))
