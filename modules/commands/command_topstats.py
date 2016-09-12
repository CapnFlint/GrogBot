from helper import *
import utils.twitch_utils as utils

@processes('!top')
def command_top(self, sender, args):
    viewers = utils.get_viewers(False)
    highest = None
    for viewer in viewers:
        char = self.charMgr.load_character(viewer)
        if highest is None:
            highest = char
        else:
            if char['exp'] > highest['exp']:
                highest = char
    if highest:
        self.connMgr.send_message("The highest ranked " + self.language['member'] + " in the ship is " + highest['name'] + "!")
    else:
        self.connMgr.send_message("No " + self.language['member'] + "s aboard sir!")

@processes('!topbooty')
def command_topbooty(self, sender, args):
    viewers = utils.get_viewers(False)
    highest = None
    for viewer in viewers:
        char = self.charMgr.load_character(viewer)
        if highest is None:
            highest = char
        else:
            if char['booty'] > highest['booty']:
                highest = char
    if highest:
        self.connMgr.send_message("The richest " + self.language['member'] + " in the ship be " + highest['name'] + " with " + str(highest['booty']) + " " + self.language['currency'] + "s!")
    else:
        self.connMgr.send_message("No " + self.language['member'] + " aboard sir!")
