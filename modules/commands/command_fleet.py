from helper import *

import utils.twitch_utils as twitch
import modules.overlay.overlay as overlay

@processes("!fleet", PERM_MOD)
def command_fleet(self, data):
    self.connMgr.send_message(data['sender'] + " calls forth the fleet!")
    viewers = twitch.get_viewers()
    if len(viewers) == 0:
        logging.debug("No viewers :(")
    for viewer in viewers:
        char = self.charMgr.load_char_name(viewer)
        if char['subscriber']:
            if char['ship'] > 0:
                ship = char['ship']
            else:
                ship = char['sub_count']
            overlay.ship("join", viewer, ship)
