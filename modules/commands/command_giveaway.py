import time
import thread
import random
import logging

from helper import *
import modules.overlay.overlay as overlay
import utils.twitch_utils as twitch

giveaway_running = False
giveaway_picked = ""
#winner = ""
#claimed = False

@processes('!giveaway')
def command_giveaway(self, data):
    global giveaway_running, giveaway_picked

    def giveaway_thread(self, max_entry):
        global giveaway_picked, giveaway_running

        countdown = 300 # 5 minutes
        self.winner = ''
        self.claimed = False
        self.giveaway_entries = {}
        self.max_entry = max_entry

        def command_enter(self, data):
            if check_permission(data, PERM_NONE):
                register_entry(self, data)
        self.add_command("!enter", command_enter)

        self.connMgr.send_message("Type !enter [x] now, with x being the number of entries (max entries: " + str(self.max_entry) + "), for a chance to win! You must be a follower to enter!")
        if countdown > 60:
            time.sleep(countdown - 60)
            self.connMgr.send_message("The giveaway is still running! Type !enter [x] now to have a chance of winning! (max entries: " + str(self.max_entry) + ")")
            time.sleep(60)
        else:
            time.sleep(countdown)

        self.remove_command("!enter")

        if self.giveaway_entries:
            while not self.winner:
                giveaway_picked = random.choice(get_tickets(self))
                self.passed = False
                sub = twitch.check_subscriber(giveaway_picked, "capn_flint")
                overlay.giveaway_winner(giveaway_picked, [x.lower() for x in get_entries(self)])
                self.connMgr.send_message("Drawing a winner!")
                time.sleep(80)
                self.connMgr.send_message("The winner is: " + giveaway_picked + "! You have two minutes to !claim or !pass the booty!")

                def claim_prize(self, data):
                    logging.info(data['sender'] + " is trying to claim! (" + giveaway_picked + ")")
                    if data['sender'] == giveaway_picked.lower():
                        logging.info("Giveaway Claimed!!!")
                        self.claimed = True
                        self.winner = giveaway_picked
                    else:
                        self.connMgr.send_message("Scurvy landlubbers trying to claim capnBooty they did not win must walk the plank!")
                        self.run_command("!plank",{'args':[data['sender']]})
                self.add_command("!claim", claim_prize)

                def pass_prize(self, data):
                    logging.info("PASS: " + data['sender'] + " :: " + giveaway_picked)
                    if data['sender'] == giveaway_picked.lower():
                        if giveaway_picked in self.giveaway_entries.keys():
                            del self.giveaway_entries[giveaway_picked]
                        self.connMgr.send_message(giveaway_picked + " has passed on the prize!")
                        self.passed = True
                self.add_command("!pass", pass_prize)

                if sub:
                    countdown = 30
                else:
                    countdown = 120

                while not self.claimed:
                    logging.info("Countdown: " + str(countdown))
                    time.sleep(2)
                    if self.passed:
                        self.remove_command("!claim")
                        self.remove_command("!pass")
                        self.passed = False
                        break
                    countdown -= 2
                    if countdown == 0:
                        if sub:
                            self.connMgr.send_message("The winner is: " + giveaway_picked + "! As a sub, they automatically claim the booty!")
                            self.claimed = True
                            self.winner = giveaway_picked
                        else:
                            self.connMgr.send_message("Hard luck " + giveaway_picked + "! You snooze, you lose!")
                            self.remove_command("!claim")
                            self.remove_command("!pass")
                            del self.giveaway_entries[giveaway_picked]
                            break
                    if countdown == 60:
                        self.connMgr.send_message(giveaway_picked + ", you only have " + str(countdown) + " seconds left to [claim]!")

            self.connMgr.send_message("YARRR! " + self.winner + " has claimed the booty!")
            self.remove_command("!claim")
            self.remove_command("!pass")
            charge_entry_fees(self)
            overlay.giveaway_end()
        else:
            self.connMgr.send_message("I guess noone wants this booty! I'll keep it for meself R)")
            overlay.giveaway_end()

        self.giveaway_entries = {}
        giveaway_running = False
        self.grog.event_running = False

    if self.grog.event_running and not giveaway_running:
        self.connMgr.send_message("Cannot start a giveaway while an event is running!")
    if not giveaway_running:
        if check_permission(data, PERM_MOD):
            if data['args']:
                args = data['args']
                try:
                    max_entry = int(args[len(args)-1])
                    item = " ".join(args[:-1])
                except:
                    max_entry = 9001
                    item = " ".join(args)
            else:
                max_entry = 9001
                item = "Something AWESOME!"

            logging.info("MAX ENTRY: " + str(max_entry))
            overlay.giveaway_start(item)
            self.connMgr.send_message("There be BOOTY to be plundered!!!")
            self.connMgr.send_message("A giveaway has started! Type [HL]!enter [x][/HL] now!", screen=True, chat=False)
            giveaway_running = True
            self.grog.event_running = True
            thread.start_new_thread(giveaway_thread, (self,max_entry))
        else:
            self.connMgr.send_message("Giveaways are started whenever target follower goals are met and other special occasions. The prize will be either one of the games listed below the stream, or will be announced when the giveaway is started! You must follow to enter giveaways.")
    else:
        if check_permission(data, PERM_MOD):
            self.connMgr.send_message("Giveaway already started!")
        else:
            self.connMgr.send_message("To enter the current giveaway, type !enter [x] now! You can type !booty to check how many tickets you can afford.")

def register_entry(self, data):
    tickets = 0
    args = data['args']

    if self.charMgr.follows_me(data['sender_id'], True):
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

        char = self.charMgr.load_character(data['sender_id'])

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
        self.connMgr.send_message("Sorry " + data['sender'] + "! You must follow to enter giveaways.")

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
            char = self.charMgr.load_char_name(name)
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
        for sub in sublist:
            entries.append(self.charMgr.load_character(sub)['name'])
    return entries
