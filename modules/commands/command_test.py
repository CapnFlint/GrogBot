from helper import *
import modules.overlay.overlay as overlay
import utils.twitter as twitter

@processes("!test", PERM_ADMIN)
def command_test(self, sender, args):
    overlay.alert_follow("GrogBot", True)
