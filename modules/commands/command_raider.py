from helper import *
import utils.twitch_utils as twitch

import modules.overlay.overlay as overlay

# retrieves a quote
@processes("!raider", PERM_MOD)
def command_quote(self, sender, args):
    raider = args[0]
    streamer = twitch.check_streamer(raider)
    if streamer and streamer['game']:
        self.connMgr.send_message("We are being raided by " + raider + "! DEFEND THE SHIP!!!")
        overlay.start_raid(raider, streamer['logo'])
    else:
        self.connMgr.send_message(raider + " isn't a valid streamer!")
