from helper import *
import utils.db_utils as db


@processes('!mod', PERM_ADMIN)
def command_mod(self, sender, args):
    user = args[0]
    db.make_mod(user)
