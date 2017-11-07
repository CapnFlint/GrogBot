from helper import *
import utils.twitch_utils as utils

import modules.overlay.overlay as overlay

# retrieves a quote
@processes("!potato")
def command_quote(self, data):
    self.connMgr.send_message("capnYarr capnHype capnYarr capnHype capnYarr capnHype capnYarr capnHype capnYarr capnHype capnYarr capnHype")
    overlay.send_emotes(data['sender'], ['138934','138934','138934','138934','138934','138934','81534','81534','81534','81534','81534','81534','81534'])
