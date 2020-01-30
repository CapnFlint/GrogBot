from helper import *
import modules.overlay.overlay as overlay
import utils.twitter as twitter
import utils.twitch_utils as twitch

@processes("!test", PERM_ADMIN)
def command_test(self, data):
    self.connMgr.send_message("You have {0} sub points!".format(twitch.get_sub_points()))

@processes("!test1", PERM_ADMIN)
def command_test1(self, data):
    overlay.alert_sub("GrogBot", "1000", "1", "sub", "This is a basic sub!")

#@processes("!test2", PERM_ADMIN)
def command_test2(self, data):
    overlay.alert_sub("GrogBot", "2000", "1", "sub", "This is a $9.99 sub!")

@processes("!test3", PERM_ADMIN)
def command_test2(self, data):
    overlay.alert_sub("GrogBot", "3000", "1", "sub", "This is a $24.99 sub!")
