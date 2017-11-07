import thread
import time

from helper import *
import utils.twitch_utils as utils

raiding = False

#@processes('!raid', PERM_MOD)
def command_raid(self, sender, args):
    global raiding
    target = args[0]

    def raid_thread(self, target, game):
        global raiding
        raid_url = "http://twitch.tv/" + target
        self.connMgr.send_message("YARRR!!! Prepare to raid me hearties!!!", screen=True)
        time.sleep(5)
        self.connMgr.send_message(target + " shall learn to fear the good ship Narwhal and all who sail in her!")
        self.connMgr.send_message("They are currently playing: " + game)
        self.connMgr.send_message("Join their chat, await the Capn's command, then give em hell!!!")
        self.connMgr.send_message("The raid will commence in 30 seconds!")
        self.connMgr.send_message("Let's see your YARRR face!!!")
        self.connMgr.send_message(raid_url)
        self.connMgr.send_message(raid_url)
        self.connMgr.send_message(raid_url)
        time.sleep(15)
        self.connMgr.send_message("R) R) R) 15 seconds!!! R) R) R)")
        time.sleep(15)
        self.connMgr.send_message("GO RAID GO!!! R) YARRR!!! R)")
        raiding = False

    streamer = utils.check_streamer(target)
    if streamer:
        if not raiding:
            raiding = True
            thread.start_new_thread(raid_thread, (self,target,streamer['game']))
    else:
        self.connMgr.send_message(target + " isn't a valid streamer!")
