from helper import *
import time

from config.strings import strings

@processes('!booty')
def command_booty(self, sender, args):
    char = self.charMgr.load_character(sender)
    booty = char['booty']

    try:
        self.lastBooty
    except AttributeError:
        self.lastBooty = 0

    now = time.time()

    if (now - self.lastBooty) < 5:
        self.cmdBuffer.buffer_command(buffered_booty, char)
    else:
        if int(booty) > 0:
            self.connMgr.send_message(strings['CMD_BOOTY_AMOUNT'].format(name=char['name'], amount=str(char['booty'])))
        else:
            self.connMgr.send_message(strings['CMD_BOOTY_NONE'].format(name=char['name']))

    self.lastBooty = now

def buffered_booty(self, userlist):
    chars = []
    for char in userlist:
        chars.append(char['name'] + " (" + str(char['booty']) + ")")

    message = strings['CMD_BOOTY_BUFFERED'].format(amounts=", ".join(chars))
    self.connMgr.send_message(message)
