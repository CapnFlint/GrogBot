from helper import *
import random
import utils.db_utils as db
import utils.twitch_utils as twitch
import modules.overlay.overlay as overlay


@processes('!randomsub', PERM_MOD)
def command_randomsub(self, sender, args):
    subs = twitch.get_subscribers()
    sublist = subs['1000'] + subs['2000'] + subs['3000']
    sublist.remove('grogbot')
    sublist.remove('capn_flint')
    random.shuffle(sublist)
    sub = random.choice(sublist)
    overlay.giveaway_winner(sub, sublist)
