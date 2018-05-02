from helper import *
import utils.db_utils as db

import modules.overlay.overlay as overlay

@processes('!plank', PERM_MOD)
def command_plank(self, data):
    print "Trying to plank..."
    target = data['args'][0]
    if len(data['args']) > 1:
        try:
            duration = int(data['args'][1])
        except:
            duration = 0
    else:
        duration = 0

    if self.charMgr.char_exists(target):
        print target + " exists!"
        if not twitch.is_mod(twitch.get_ids([target])):
            if self.charMgr.is_alive(target):
                self.connMgr.send_message(target + ', you have been sentenced to walk the PLANK!!!')
                sound = [{"file": "sounds/davey.mp3", "volume": 50}, {"file": "sounds/splash.mp3", "volume": 60}]
                overlay.alert(1, "[HL]{0}[/HL] has walked the PLANK!!!".format(target), sound)
                self.charMgr.kill_character(target, duration)
            else:
                self.connMgr.send_message("Sorry sir, " + target + " is already dead!")
        else:
            self.connMgr.send_message("Trying to plank another officer? That's mutinous!")
    else:
        self.connMgr.send_message(target + " doesn't exist!")
