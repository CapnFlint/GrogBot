from helper import *
import time
import random
import thread
import modules.overlay.overlay as overlay

duel_active = False

@processes("!toggleduel", PERM_MOD)
def command_toggleduel(self, sender, args):
    try:
        self.duel_toggle
    except NameError:
        self.duel_toggle = False
    self.duel_toggle = not self.duel_toggle
    if self.duel_toggle:
        self.connMgr.send_message("Dueling has been enabled!")
    else:
        self.connMgr.send_message("Dueling has been disabled.")

@processes("!duel")
def command_duel(self, sender, args):
    global duel_active

    try:
        self.duel_toggle
    except:
        self.duel_toggle = True
    try:
        self.duel_cooldowns
    except:
        self.duel_cooldowns = {}

    if self.duel_toggle:
        if self.grog.event_running:
            self.connMgr.send_message("Sorry " + sender + ", duels cannot be fought during events!")
            return
        now = time.time()
        if sender in self.duel_cooldowns.keys():
            if now - self.duel_cooldowns[sender] < 3600:
                self.connMgr.send_message("Sorry " + sender + ", you're still recovering from your last duel! Please wait " + str(int((3600 - (now - self.duel_cooldowns[sender])) / 60)) + " minutes before trying again.")
                return
            else:
                del self.duel_cooldowns[sender]
        if not duel_active:
            if args:
                # do the duel thing
                target = args[0].lstrip('@').lower()
                if self.charMgr.char_exists(target) and target != sender and self.charMgr.is_alive(target):
                    duel_active = True
                    self.duel_cooldowns[sender] = now
                    player1 = sender
                    player2 = target
                    challenge_player(self, player1, player2)
                else:
                    self.connMgr.send_message("Sorry, " + target + " is not a valid target.")
            else:
                self.connMgr.send_message("You must specify who you would like to duel!")
        else:
            self.connMgr.send_message("A duel is currently being fought, or the cleaners are busy mopping up the blood. Try again later!")
    else:
        self.connMgr.send_message("Sorry, dueling is currently disabled. Ask a mod nicely if you would like to duel!")

def challenge_player(self, player1, player2):
    # add accept or decline commands
    def command_accept(self, sender, args):
        print "DEBUG:: sender - " + sender + ", player2 - " + player2
        if sender == player2:
            self.connMgr.send_message(sender + " has accepted the duel! Let battle commence!")
            self.responded = True
            thread.start_new_thread(fight_duel, (self, player1, player2))
    self.add_command("!accept", command_accept)
    def command_decline(self, sender, args):
        if sender == player2:
            self.connMgr.send_message(sender + " has declined the duel. Honour will not be reclaimed today!")
            self.responded = True
            duel_active = False
            end_duel(self)
    self.add_command("!decline", command_decline)

    # wait for accept or decline
    self.connMgr.send_message(player2 + " you have been challenged by " + player1 + " to a duel to the DEATH! Will you [accept] or [decline]?")

    self.responded = False
    def countdown_thread():
        countdown = 120
        while not self.responded:
            time.sleep(2)
            countdown -= 2
            if countdown <= 0:
                self.connMgr.send_message(player2 + " is dozing in the corner after drinking too much rum! They are in no fit state to duel.")
                self.responded = True
                end_duel(self)

    thread.start_new_thread(countdown_thread, ())

    # if timeout, auto-decline

def end_duel(self):
    global duel_active
    self.remove_command("!accept")
    self.remove_command("!decline")
    duel_active = False


def fight_duel(self, player1, player2):
    self.connMgr.send_message(player1 + " has challenged " + player2 + " to a duel to the DEATH! Who will win?")
    # start betting
    self.run_command("!runbet", [player1, player2])
    time.sleep(125)

    fight_array = []
    red_count = 5 + (self.charMgr.load_character(player1)['level'] / 5)
    blue_count = 5 + (self.charMgr.load_character(player2)['level'] / 5)
    for _ in range(red_count):
        fight_array.append(player1)
    for _ in range(blue_count):
        fight_array.append(player2)
    print fight_array
    winner = random.choice(fight_array)
    # add logic for second and third place
    if winner == player1:
        exp = self.charMgr.load_character(player2)['level']
        loser = player2
    else:
        exp = self.charMgr.load_character(player1)['level']
        loser = player1

    self.charMgr.give_exp(exp, [winner])
    self.charMgr.give_exp(-exp, [loser])
    self.connMgr.send_message(winner + " wins! (+" + str(exp) + "exp)")
    time.sleep(5)
    self.run_command("!winner", [winner])
    time.sleep(900)
    self.connMgr.send_message("The Dueling arena has been cleaned and is ready for the next match!")
    end_duel(self)
