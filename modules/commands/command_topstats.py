from helper import *
import utils.twitch_utils as utils
from config.strings import strings

@processes('!top')
def command_top(self, data):
    viewers = utils.get_viewers(False)
    highest = None
    for viewer in viewers:
        char = self.charMgr.load_char_name(viewer)
        if highest is None:
            highest = char
        else:
            if char['exp'] > highest['exp']:
                highest = char
    if highest:
        self.connMgr.send_message(strings['CMD_TOP_HIGHEST'].format(rank=self.charMgr.get_rank(highest, False, False), name=highest['name']))
    else:
        self.connMgr.send_message(strings['CMD_TOP_NONE'])

@processes('!topbooty')
def command_topbooty(self, data):
    viewers = utils.get_viewers(False)
    highest = None
    for viewer in viewers:
        char = self.charMgr.load_char_name(viewer)
        if highest is None:
            highest = char
        else:
            if char['booty'] > highest['booty']:
                highest = char
    if highest:
        self.connMgr.send_message(strings['CMD_TOPBOOTY_HIGHEST'].format(name=highest['name'], amount=str(highest['booty'])))
    else:
        self.connMgr.send_message(strings['CMD_TOP_NONE'])
