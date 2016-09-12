import time
import thread
import random
import copy

from helper import *
import utils.twitch_utils as utils

arena_running = False
last_arena = 0
cooldown = 0

@processes("!startarena", PERM_MOD)
def command_startarena(self, sender, args):
    global arena_running
    self.arena_entries = {}

    # Set up arena thread here
    def arena_thread(self):
        countdown = 120
        # add !joinarena command
        def command_joinarena(self, sender, args):
            if check_permission(sender, PERM_NONE):
                arena_register_entry(self, sender, args)
        self.add_command("!joinarena", command_joinarena)

        self.connMgr.send_message("A winner takes all Arena Battle has been started by "
                                    + sender
                                    + "! To enter type !joinarena now! The entry fee is "
                                    + str(self.arena_max_bet) + " Doubloon(s)")

        if countdown > 60:
            time.sleep(countdown - 60)
            self.connMgr.send_message("The arena is still open for entries! Type !joinarena now to have a chance of winning!")
            time.sleep(60)
        else:
            time.sleep(countdown)

        self.remove_command("!joinarena")
        if self.arena_entries:
            arena_fight_battles(self)

    if arena_running:
        self.connMgr.send_message("Arena already running! Use !joinarena [x] to join!")
        return

    #if not utils.check_follows_me(sender):
    #    self.connMgr.send_message("Sorry " + sender + " but you need to be a follower to start arena battles!")
    #    return
    elif self.grog.event_running:
        self.connMgr.send_message("An event is running, please try again once it's done!")
        return
    else:
        self.arena_max_bet = 0

        try:
            self.arena_max_bet = int(args[0])
        except:
            self.connMgr.send_message("Invalid value specified for !startarena. Specify an number between 1 and 100")
            return

        if self.arena_max_bet < 1:
            self.arena_max_bet = 1
        elif self.arena_max_bet > 100:
            self.arena_max_bet = 100

        self.arena_running = True
        self.grog.event_running = True

        thread.start_new_thread(arena_thread, (self,))

def arena_register_entry(self, sender, args):
    char = self.charMgr.load_character(sender)
    if char['follows']:
        if char['booty'] >= self.arena_max_bet:
            self.arena_entries[sender] = self.arena_max_bet
            self.connMgr.send_message(sender + " has entered the arena!")
        else:
            self.connMgr.send_message("Sorry " + sender + ", you don't have enough booty to enter :(")
    else:
        self.connMgr.send_message("Sorry " + sender + ", you need to be a follower to do battle in the arena!")

def arena_prize_fund(self):
    total = 0
    for entry in self.arena_entries:
        total += self.arena_entries[entry]
    return total

def arena_collect_fees(self):
    for entry in self.arena_entries:
        char = self.charMgr.load_character(entry)
        char['booty'] -= self.arena_max_bet
        self.charMgr.save_character(char)

def arena_fight_battles(self):
    self.connMgr.send_message("Let battle commence! May the odds be ever in your favour!")
    print self.arena_entries

    win_messages = [
        "Shaking the blood off their blade, and wiping the sweat from their brow {0} walks away victorious!"
    ]

    competitors = copy.copy(self.arena_entries)
    if len(competitors) == 1:
        competitors['grogbot'] = self.arena_max_bet
    winners = []

    rnd = 1
    while len(competitors) > 1:
        if len(competitors) == 2:
            self.connMgr.send_message("Final Round!!!")
        else:
            self.connMgr.send_message("STARTING ROUND: " + str(rnd))

        temp = competitors.keys()

        random.shuffle(temp)
        while len(temp) > 1:
            red = temp.pop(0)
            blue = temp.pop(0)
            self.connMgr.send_message(red + " is facing " + blue + " in a fight to the DEATH! Who will win?")
            # start betting
            self.run_command("!runbet", [red, blue])
            time.sleep(125)

            fight_array = []
            red_count = 5 + (self.charMgr.load_character(red)['level'] / 5)
            blue_count = 5 + (self.charMgr.load_character(blue)['level'] / 5)
            for _ in range(red_count):
                fight_array.append(red)
            for _ in range(blue_count):
                fight_array.append(blue)
            print fight_array
            winner = random.choice(fight_array)
            # add logic for second and third place
            if winner == red:
                exp = self.charMgr.load_character(blue)['level']

                del competitors[blue]
            else:
                exp = self.charMgr.load_character(red)['level']
                del competitors[red]
            self.charMgr.give_exp(exp, [winner])
            self.connMgr.send_message(winner + " wins! (+" + str(exp) + "exp)")
            time.sleep(5)
            self.run_command("!winner", [winner])
            time.sleep(30)
            # bet winner
        rnd += 1

    winnings = arena_prize_fund(self)
    winner = competitors.keys()[0]
    self.connMgr.send_message("The Grand Champion is " + winner + " winning " + str(winnings) + " Doubloons!")
    arena_collect_fees(self)
    self.charMgr.give_booty(winnings, [winner])

    self.arena_running = False
    self.grog.event_running = False
