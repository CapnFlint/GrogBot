from helper import *
import utils.twitch_utils as twitch

@processes('!follow', PERM_MOD)
def command_raid(self, data):
    print "Entered follow command"
    target = data['args'][0]
    print target
    streamer = twitch.check_streamer(target)
    print streamer
    if streamer and streamer['game']:
        self.connMgr.send_message("Hey! You should all go give " + target + " some love, and a follow! They last played " + streamer['game'] + ". Clicky for their channel: http://twitch.tv/" + target)
    else:
        self.connMgr.send_message(target + " isn't a valid streamer!")
