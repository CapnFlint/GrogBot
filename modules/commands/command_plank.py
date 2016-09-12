from helper import *
import utils.db_utils as db

import modules.overlay.overlay as overlay

@processes('!plank', PERM_MOD)
def command_plank(self, sender, args):
    target = args[0]
    if len(args) > 1:
        try:
            duration = int(args[1])
        except:
            duration = 0
    else:
        duration = 0

    if self.charMgr.char_exists(target):
        if db.get_access(target) == 0:
            self.connMgr.send_message(target + ', you have been sentenced to walk the PLANK!!!')
            sound = [{"file": "sounds/davey.mp3", "volume": 50}, {"file": "sounds/splash.mp3", "volume": 60}]
            overlay.alert(1, "[HL]{0}[/HL] has walked the PLANK!!!".format(target), sound)
            self.charMgr.kill_character(target, duration)
    else:
        self.connMgr.send_message(target + " doesn't exist!")