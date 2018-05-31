import time
import thread
import random

from helper import *
import modules.overlay.overlay as overlay
import utils.twitch_utils as twitch

raffle_running = False
raffle_picked = ""
#winner = ""
#claimed = False

#TODO: Make sure we use ID not NAME

#@processes('!raffle')
def command_raffle(self, sender, args):
    global raffle_running, raffle_picked

    if args and check_permission(data, PERM_MOD):
        if self.grog.event_running and not raffle_running:
            self.connMgr.send_message("Cannot start a raffle while an event is running!")
        if not raffle_running:
            command = args[0]
            data = args[1:]

            valid_commands = ["start", "draw"]

            if command in valid_commands:
                if command == "start":
                    if data:
                        keyword = data[0]
                        prize = data[1:]
                        if not prize:
                            prize = "Something Awesome!"
                        overlay.raffle_start(prize, keyword)
                        start_raffle(self, keyword)
                    else:
                        self.connMgr.send_message("Must specify at least a keyword!")

                if command == "end":
                    end_raffle()
        else:
            if check_permission(data, PERM_MOD):
                self.connMgr.send_message("Raffle already started!")
            else:
                self.connMgr.send_message("To enter the current raffle, type !" + keyword + " ONCE now! You can type !booty to check how many tickets you can afford.")

    else:
        self.connMgr.send_message("There is no raffle currently running.");

def raffle_thread(self, keyword):
    global raffle_picked, raffle_running

    countdown = 300 # 5 minutes
    self.winner = ''
    self.claimed = False
    self.raffle_entries = {}
    self.max_entry = max_entry

    def command_raffle_enter(self, sender, args):
        if check_permission(data, PERM_NONE):
            raffle_entry(self, sender, args)
    self.add_command("!" + keyword, command_raffle_enter)

    self.connMgr.send_message("Type !" + keyword + " ONCE now for a chance to win! You must be a follower to enter!")
    if countdown > 60:
        time.sleep(countdown - 60)
        self.connMgr.send_message("The giveaway is still running! Type !enter now to have a chance of winning!")
        time.sleep(60)
    else:
        time.sleep(countdown)

    self.remove_command("!" + keyword)

    if self.raffle_entries:
        while not self.winner:
            raffle_picked = random.choice(get_tickets(self))
            self.passed = False
            sub = twitch.check_subscriber(raffle_picked, "capn_flint")
            overlay.raffle_winner(raffle_picked, [x.lower() for x in get_entries(self)])
            self.connMgr.send_message("Drawing a winner!")

            def claim_prize(self, data):
                print "INFO: " + data['sender'] + " is trying to claim! (" + raffle_picked + ")"
                if data['sender'] == raffle_picked.lower():
                    print "INFO: Claimed!!!"
                    self.claimed = True
                    self.winner = giveaway_picked
                else:
                    self.connMgr.send_message("Scurvy landlubbers trying to claim capnBooty they did not win must walk the plank!")
                    self.run_command("!plank",{'args':[data['sender']]})
            self.add_command("!claim", claim_prize)

            def pass_prize(self, data):
                print "PASS: " + data['sender'] + " :: " + raffle_picked
                if data['sender'] == raffle_picked.lower():
                    if raffle_picked in self.raffle_entries.keys():
                        del self.raffle_entries[raffle_picked]
                    self.connMgr.send_message(raffle_picked + " has passed on the prize!")
                    self.passed = True
            self.add_command("!pass", pass_prize)

            if sub:
                countdown = 30
            else:
                countdown = 120

            while not self.claimed:
                print "Countdown: " + str(countdown)
                time.sleep(2)
                if self.passed:
                    self.remove_command("!claim")
                    self.remove_command("!pass")
                    self.passed = False
                    break
                countdown -= 2
                if countdown == 0:
                    if sub:
                        self.connMgr.send_message("The winner is: " + raffle_picked + "! As a sub, they automatically claim the booty!")
                        self.claimed = True
                        self.winner = giveaway_picked
                    else:
                        self.connMgr.send_message("Hard luck " + raffle_picked + "! You snooze, you lose!")
                        self.remove_command("!claim")
                        self.remove_command("!pass")
                        del self.raffle_entries[raffle_picked]
                        break
                if countdown == 60:
                    self.connMgr.send_message(raffle_picked + ", you only have " + str(countdown) + " seconds left to [claim]!")

        self.connMgr.send_message("YARRR! " + self.winner + " has claimed the booty!")
        self.remove_command("!claim")
        self.remove_command("!pass")
        charge_entry_fees(self)
        overlay.raffle_end()
    else:
        self.connMgr.send_message("I guess noone wants this booty! I'll keep it for meself R)")
        overlay.raffle_end()

    self.raffle_entries = {}
    raffle_running = False
    self.grog.event_running = False

def start_raffle(self, item, keyword):
    global raffle_running
    self.connMgr.send_message("There be BOOTY to be plundered!!!")
    self.connMgr.send_message("A raffle has started! Type [HL]!" + keyword + "[/HL] ONCE now!", screen=True, chat=False)
    raffle_running = True
    self.grog.event_running = True
    thread.start_new_thread(raffle_thread, (self,keyword))


def register_entry(self, sender, args):
    tickets = 0
    if self.charMgr.follows_me(sender, True):
        if len(args) > 0:
            try:
                tickets = int(args[0])
                if tickets < 0:
                    tickets = 0
                if self.max_entry == 0:
                    tickets = 1
            except:
                tickets = 1
        else:
            tickets = 1

        if tickets > self.max_entry and self.max_entry > 0:
            tickets = self.max_entry

        char = self.charMgr.load_character(sender)

        if char['booty'] >= tickets:
            self.giveaway_entries[char['name']] = tickets

            # remove entry if tickets = 0
            if self.giveaway_entries[char['name']] == 0:
                del self.giveaway_entries[char['name']]
            else:
                self.cmdBuffer.buffer_command(buffered_entries, (char['name'],tickets))

                #self.connMgr.send_message(char['name'] + " entered with " + str(tickets) + " tickets.")
        else:
            self.connMgr.send_message("Sorry " + char['name'] + ", you don't have that much booty!")

    else:
        self.connMgr.send_message("Sorry " + sender + "! You must follow to enter giveaways.")

def buffered_entries(self, userlist):
    output = "New Entries: "
    for user in userlist:
        output += user[0] + " (" + str(user[1]) + ") "
    self.connMgr.send_message(output)

def charge_entry_fees(self):
    if self.max_entry == 0:
        pass
    else:
        for name in self.giveaway_entries.keys():
            char = self.charMgr.load_character(name)
            char['booty'] -= self.giveaway_entries[name]
            self.charMgr.save_character(char)

def get_entries(self):
    return self.giveaway_entries.keys()

def get_tickets(self):
    entries = []
    for name in self.giveaway_entries.keys():
        for _ in range(self.giveaway_entries[name]):
            entries.append(name)
    if self.max_entry > 0:
        subs = twitch.get_subscribers()
        sublist = subs['1000'] + subs['2000'] + subs['3000']
        entries = entries + sublist
    return entries
