from helper import *
import time
import random
import thread
import modules.overlay.overlay as overlay

duel_active = False

@processes("!toggleduel", PERM_MOD)
def command_toggleduel(self, data):
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
def command_duel(self, data):
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
            self.connMgr.send_message("Sorry " + data['sender'] + ", duels cannot be fought during events!")
            return

        attacker = self.charMgr.load_character(data['sender_id'])
        now = time.time()
        if attacker['id'] in self.duel_cooldowns.keys():
            if now - self.duel_cooldowns[attacker['id']] < 3600:
                self.connMgr.send_message("Sorry " + attacker['name'] + ", you're still recovering from your last duel! Please wait " + str(int((3600 - (now - self.duel_cooldowns[attacker['id']])) / 60)) + " minutes before trying again.")
                return
            else:
                del self.duel_cooldowns[attacker['id']]
        if not duel_active:
            if data['args']:
                # do the duel thing
                name = data['args'][0].lstrip('@').lower()
                target = self.charMgr.load_char_name(name)
                if target != attacker and target['level'] > 0:
                    duel_active = True
                    self.duel_cooldowns[attacker['id']] = now

                    challenge_player(self, attacker, target)
                else:
                    self.connMgr.send_message("Sorry, " + name + " is not a valid target.")
            else:
                self.connMgr.send_message("You must specify who you would like to duel!")
        else:
            self.connMgr.send_message("A duel is currently being fought, or the cleaners are busy mopping up the blood. Try again later!")
    else:
        self.connMgr.send_message("Sorry, dueling is currently disabled. Ask a mod nicely if you would like to duel!")

def challenge_player(self, attacker, target):
    # add accept or decline commands
    def command_accept(self, data):
        if data['sender_id'] == target['id']:
            self.connMgr.send_message(target['name'] + " has accepted the duel! Let battle commence!")
            self.responded = True
            self.remove_command("!accept")
            self.remove_command("!decline")
            thread.start_new_thread(fight_duel, (self, attacker, target))
    self.add_command("!accept", command_accept)

    def command_decline(self, data):
        if data['sender_id'] == target['id']:
            self.connMgr.send_message(target['name'] + " has declined the duel. Honour will not be reclaimed today!")
            self.responded = True
            self.remove_command("!accept")
            self.remove_command("!decline")
            end_duel(self)
    self.add_command("!decline", command_decline)

    # wait for accept or decline
    self.connMgr.send_message(target['name'] + " you have been challenged by " + attacker['name'] + " to a duel to the DEATH! Will you [accept] or [decline]?")

    self.responded = False

    def countdown_thread():
        countdown = 120
        while not self.responded:
            time.sleep(2)
            countdown -= 2
            if countdown <= 0:
                self.connMgr.send_message(target['name'] + " is dozing in the corner after drinking too much rum! They are in no fit state to duel.")
                self.responded = True
                end_duel(self)

    thread.start_new_thread(countdown_thread, ())

    # if timeout, auto-decline

def end_duel(self):
    global duel_active
    duel_active = False


def fight_duel(self, attacker, target):
    self.connMgr.send_message(attacker['name'] + " has challenged " + target['name'] + " to a duel to the DEATH! Who will win?")
    # start betting
    self.run_command("!runbet", {'args':[attacker['name'].lower(), target['name'].lower()]})
    time.sleep(125)

    fight_array = []
    red_count = 5 + (attacker['level'] / 5)
    blue_count = 5 + (target['level'] / 5)
    for _ in range(red_count):
        fight_array.append(attacker['name'])
    for _ in range(blue_count):
        fight_array.append(target['name'])
    print fight_array
    winner = random.choice(fight_array)
    # add logic for second and third place
    if winner == attacker['name']:
        exp = target['level'] * 10
        loser = target['name']
    else:
        exp = attacker['level'] * 10
        loser = attacker['name']

    self.charMgr.give_exp(exp, [winner])
    self.charMgr.give_exp(-exp, [loser])
    self.connMgr.send_message(winner + " wins! (+" + str(exp) + "exp)")
    time.sleep(5)
    self.run_command("!winner", {'args':[winner]})
    time.sleep(900)
    self.connMgr.send_message("The Dueling arena has been cleaned and is ready for the next match!")
    end_duel(self)
