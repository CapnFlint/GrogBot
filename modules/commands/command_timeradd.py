from helper import *
import modules.overlay.overlay as overlay

#@processes("!timeradd", PERM_MOD)
def command_timeradd(self, sender, args):
    if args:
        try:
            time = int(args[0])
        except:
            time = 0

        if time:
            overlay.update_timer(time)
            self.connMgr.send_message(str(time) + " minutes added to the timer!")
