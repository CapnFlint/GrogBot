from helper import *
from threading import Timer
import utils.twitch_utils as twitch

import modules.overlay.overlay as overlay

# retrieves a quote
@processes("!raider", PERM_MOD)
def command_quote(self, data):
    raider = data['args'][0]
    streamer = twitch.check_streamer(raider)
    if streamer and streamer['game']:
        self.connMgr.send_message("We are being raided by " + raider + "! DEFEND THE SHIP!!!")
        overlay.start_raid(raider, streamer['logo'], self.grog.emotes)
        self.connMgr._send_message(".slow 2")

        def slow_off():
            self.connMgr._send_message(".slowoff")
        # set a timer
        t = Timer(140.0, slow_off)
        t.start()
    else:
        self.connMgr.send_message(raider + " isn't a valid streamer!")
