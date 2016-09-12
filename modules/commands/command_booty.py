from helper import *
import time


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
            self.connMgr.send_message(char['name'] + ' you have ' + str(char['booty']) + ' ' + self.language['currency'] + 's!')
        else:
            self.connMgr.send_message(char['name'] + ' you have no ' + self.language['currency'] + 's :(')

    self.lastBooty = now

def buffered_booty(self, userlist):
    message = "Booty Amounts: "
    chars = []
    for char in userlist:
        chars.append(char['name'] + " (" + str(char['booty']) + ")")

    message = message + ", ".join(chars)
    self.connMgr.send_message(message)
