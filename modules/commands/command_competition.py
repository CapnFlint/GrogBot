from helper import *
import utils.twitch_utils as twitch
import utils.db_utils as db


#@processes('!register')
def command_register(self, sender, args):
    if args:
        handle = args[0]
        if handle:
            if twitch.check_follower(sender):
                res = db.sc_register(handle, sender)
                if res:
                    self.connMgr.send_message(sender + ", you are already registered!")
                else:
                    self.connMgr.send_message(sender + " registered!")
            else:
                self.connMgr.send_message("Sorry " + sender + ", but you need to be a follower to enter!")
        else:
            self.connMgr.send_message("To register type !register <SC Handle>")
    else:
        self.connMgr.send_message("To register type !register <SC Handle>")


#@processes('!unregister', PERM_MOD)
def command_unregister(self, sender, args):
    name = args[0]
    db.sc_unregister(name)
    self.connMgr.send_message(name + " unregistered.")

#@processes('!addpoints', PERM_MOD)
def command_addpoints(self, sender, args):
    name = args[0]
    try:
        points = int(args[1])
    except:
        points = 0
    if name and points:
        res = db.sc_addpoints(name, points)
        if res:
            self.connMgr.send_message(str(points) + " added to " + name + "!")
        else:
            self.connMgr.send_message("No points added.")

#@processes('!clearscores', PERM_MOD)
def command_clearscores(self, sender, args):
    db.sc_clearscores()
    self.connMgr.send_message("Scores cleared!")
