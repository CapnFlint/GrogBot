from helper import *
import utils.db_utils as db
import utils.twitch_utils as utils

last_rip = 0

#@processes('!rip')
def command_rip(self, sender, args):
    if check_permission(sender, 1): #Mods update death counter
        db.stats_add_death(utils.get_game('capn_flint'))

    self.connMgr.send_message("capnRIP capnRIP RIP Capn capnRIP capnRIP")

#@processes('!unrip', PERM_MOD)
def command_unrip(self, sender, args):
    db.stats_remove_death(utils.get_game('capn_flint'))
