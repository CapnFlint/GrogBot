from helper import *
import utils.db_utils as db

@processes('!addcmd', PERM_MOD)
def command_addcmd(self, sender, args):
    if len(args) > 1:
        command = "!" + args[0].lstrip('!').lower()
        message = " ".join(args[1:])
        self.add_custom_command(command, message)
    else:
        "wut?"

@processes('!removecmd', PERM_MOD)
def command_removecmd(self, sender, args):
    if len(args) > 0:
        command = "!" + args[0].lstrip('!')
        self.remove_custom_command(command)
    else:
        "wut?"
