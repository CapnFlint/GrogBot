from helper import *
import modules.overlay.overlay as overlay

@processes("!timerset", PERM_ADMIN)
def command_timerset(self, data):
    if data['args']:
        try:
            time = int(data['args'][0])
        except:
            time = 0

        if time:
            overlay.set_timer(time)
            self.connMgr.send_message("Timer adjusted!")
