import time
import thread
import random

from helper import *

#@processes("!mutiny", PERM_MOD)
def command_mutiny(self, sender, args):
    self.mutineers = {}
    self.defenders = {}
    self.connMgr.send_message("The Capn catches " + sender + " trying to start a mutiny!")
    self.run_command("!plank", {'args':[sender, 15]})

    # Have a mutiny window... Random event every X to Y minutes.
    # a viewer starts a mutiny... anyone or subscriber?

    # a timer starts, and others can choose to !join the mutiny, or !defend the captain
    def mutiny_thread(self):
        countdown = 120

        def command_join(self, sender, args):
            if check_permission(data, PERM_NONE):
                mutiny_join(self, sender)
        self.add_command("!join", command_join)

        def command_defend(self, sender, args):
            if check_permission(data, PERM_NONE):
                mutiny_defend(self, sender)
        self.add_command("!defend", command_defend)

        time.sleep(countdown)

        self.remove_command("!join")
        self.remove_command("!defend")

        print self.mutineers

        if self.mutineers:
            self.connMgr.send_message("The Mutiny has begun!")
            mutiny_start(self)
        else:
            self.connMgr.send_message("No one joined the mutiny today...")

    # if mutiny isn't already running, and no other event is running...
    #mutiny_join(self, sender)
    #thread.start_new_thread(mutiny_thread, (self,))
    #self.connMgr.send_message(sender + " has started a mutiny! Would you like to !join the mutiny, or !defend the Captain?!")


def mutiny_join(self, sender):
    # handle adding player to the mutiny
    if sender not in self.mutineers.keys() + self.defenders.keys():
        self.connMgr.send_message(sender + " has joined the mutiny!")
        self.mutineers[sender] = self.charMgr.load_character(sender)['level']

def mutiny_defend(self, sender):
    # handle adding a player to the defence
    if sender not in self.mutineers.keys() + self.defenders.keys():
        self.connMgr.send_message(sender + " is defending the ship!")
        self.defenders[sender] = self.charMgr.load_character(sender)['level']

def sum_array(values):
    total = 0
    for i in values:
        total += i

def mutiny_start(self):
    # See if mutiny succeeds (determine what this means)
    result = 50 + sum_array(self.defenders.values()) - sum_array(self.mutineers.values())
    print self.defenders
    print self.mutineers
    print result
    if result <= 0:
        self.connMgr.send_message("The Mutiny succeeds! Mutineers: " + ", ".join(self.mutineers))
        # Success!
        # If mutiny succeeds, start a mutiny timer. During timer, mutineers gain access
        # to special functionality. What functionality?
        # - Turn on song requests?
        # - Manage song requests
        # - Gain access to on-screen sounds/animations?
        # - Can /plank anyone, including a mod? One /plank per mutineer.
        # - Free grog for mutineers?
        # - New captain mod for x minutes?
        # - Can start a battle arena?
        # - Start certain events (treasure hunt?)
        # Vote for a new captain? Or person who started mutiny?
    else:
        self.connMgr.send_message("The Mutiny fails. Off the ship with ya!")
        # Mutiny fail
        # Else it fails, all mutineers get planked/timed out for 5 minutes. Lose EXP and Booty.
        # Everyone who defends the ship gains exp and booty

    # Timer ends, Grog regains control of the ship, returns it to the captain, mutineers
    # get planked/timed out for X minutes, lose EXP and Booty.

    self.defenders = {}
    self.mutineers = {}

    # cooldown timer
