from helper import *
import utils.db_utils as db

import modules.overlay.overlay as overlay

@processes('!clearstats', PERM_ADMIN)
def command_register(self, data):
    db.clear_stats()
    overlay.update_stat('follows', 0)
    overlay.update_stat('subs', 0)
    self.connMgr.send_message("Stats reset!")
