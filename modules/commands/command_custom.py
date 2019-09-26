from helper import *
import utils.db_utils as db

@processes('!addcmd', PERM_MOD)
def command_addcmd(self, data):
    if len(data['args']) > 1:
        command = "!" + data['args'][0].lstrip('!').lower()
        message = " ".join(data['args'][1:])
        self.add_custom_command(command, message)
    else:
        "wut?"

@processes('!removecmd', PERM_MOD)
def command_removecmd(self, data):
    if len(data['args']) > 0:
        command = "!" + data['args'][0].lstrip('!').lower()
        self.remove_custom_command(command)
    else:
        "wut?"
