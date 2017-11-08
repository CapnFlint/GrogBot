from helper import *

import utils.twitch_utils as twitch
import modules.overlay.overlay as overlay

@processes("!fleet", PERM_MOD)
def command_fleet(self, data):
    self.connMgr.send_message(data['sender'] + " calls forth the fleet!")
    viewers = twitch.get_viewers()
    if len(viewers) == 0:
        print "No viewers :("
    for viewer in viewers:
        print viewer
        sub = twitch.get_subscription(viewer)
        char = self.charMgr.load_character(viewer)
        if self.charMgr.subbed(viewer):
            print "SUBSCRIBER"
            if char['ship'] > 0:
                ship = char['ship']
            else:
                ship = char['sub_count']
            overlay.ship("join", viewer, ship)
