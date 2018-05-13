from helper import *
import modules.overlay.overlay as overlay

@processes("!timerfix", PERM_ADMIN)
def command_timerfix(self, data):
    if data['args']:
        try:
            time = int(data['args'][0])
        except:
            time = 0

        if time:
            overlay.fix_timer(time)
            self.connMgr.send_message("Timer adjusted!")
