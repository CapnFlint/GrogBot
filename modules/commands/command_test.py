from helper import *
import modules.overlay.overlay as overlay
import utils.twitter as twitter

@processes("!test1", PERM_ADMIN)
def command_test1(self, sender, args):
    overlay.alert_sub("GrogBot", "1", "1", "sub", "This is a basic sub!")

@processes("!test2", PERM_ADMIN)
def command_test2(self, sender, args):
    overlay.alert_sub("GrogBot", "2", "1", "sub", "This is a $9.99 sub!")

@processes("!test3", PERM_ADMIN)
def command_test2(self, sender, args):
    overlay.alert_sub("GrogBot", "3", "1", "sub", "This is a $24.99 sub!")
