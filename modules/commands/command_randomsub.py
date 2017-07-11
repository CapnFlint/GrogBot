from helper import *
import random
import utils.db_utils as db
import utils.twitch_utils as twitch
import modules.overlay.overlay as overlay


@processes('!randomsub', PERM_MOD)
def command_randomsub(self, sender, args):
    subs = twitch.get_subscribers().keys()
    subs.remove('grogbot')
    subs.remove('capn_flint')
    random.shuffle(subs)
    sub = random.choice(subs)
    overlay.giveaway_winner(sub, subs)
