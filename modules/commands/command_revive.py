from helper import *

@processes('!revive', PERM_MOD)
def command_revive(self, sender, args):
    if args:
        target = args[0].lower()
        if target and self.charMgr.char_exists(target):
            revived = self.charMgr.revive_character(target)
            if revived:
                self.connMgr.send_message(target + ' has been revived!')
            else:
                self.connMgr.send_message(target + " isn't dead!")
        else:
            self.connMgr.send_message("That isn't a valid user.")
    else:
        self.connMgr.send_message("To revive a character, the command is: !revive <name>")
