from helper import *

import modules.overlay.overlay as overlay

#@processes("!kids", PERM_MOD)
def command_kids(self, sender, args):
    cost = 5
    overlay.sound("sounds/kids.mp3", 50)
    self.connMgr.send_message("YAAAAAY!!!")
