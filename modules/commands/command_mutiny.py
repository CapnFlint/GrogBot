from helper import *

@processes("!mutiny")
def command_mutiny(self, sender, args):
    self.connMgr.send_message("The Capn catches " + sender + " trying to start a mutiny!")
    self.run_command("!plank", [sender, 15])
