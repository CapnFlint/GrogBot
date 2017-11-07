from helper import *
import modules.overlay.overlay as overlay

#@processes("!timerfix", PERM_ADMIN)
def command_timerfix(self, sender, args):
    if args:
        try:
            time = int(args[0])
        except:
            time = 0

        if time:
            overlay.fix_timer(time)
            self.connMgr.send_message("Timer adjusted!")
