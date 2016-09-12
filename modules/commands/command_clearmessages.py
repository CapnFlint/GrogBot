from helper import *
import utils.db_utils as db


@processes('!clearmessages', PERM_MOD)
def command_register(self, sender, args):
    db.clear_messages()
    self.connMgr.send_message("Message backlog cleared!")
