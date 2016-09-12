from helper import *
from datetime import datetime
import utils.twitch_utils as twitch

@processes("!uptime")
def command_uptime(self, sender, args):
    start = twitch.get_starttime()
    start = datetime.strptime(start, '%Y-%m-%dT%H:%M:%SZ')
    now = datetime.utcnow()
    delta = now - start

    seconds = delta.seconds % 60
    minutes = int(delta.seconds / 60)
    hours = int(minutes / 60)
    minutes = minutes % 60

    self.connMgr.send_message("Current uptime: {0} hours, {1} minutes, {2} seconds.".format(hours, minutes, seconds))
