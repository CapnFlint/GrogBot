import thread
import time
from collections import defaultdict
from itertools import chain

from helper import *
from config.strings import strings

bet_rollover = 0

@processes('!runbet', PERM_MOD)
def command_runbet(self, data):
    global bet_rollover
    #TODO: We need to lower() these so it works right
    self.bet_options = data['args'][:6]
    self.bet_entries = defaultdict(list)
    #self.bet_rollover = bet_rollover
    bet_len = 120
    if len(self.bet_options) > 1:
        self.connMgr.send_message('Betting has opened!', screen=True, chat=False)

        def command_bet(self, data):
            if check_permission(data, PERM_NONE):
                register_bet(self, data)

        self.add_command('!bet', command_bet)
        option_text = "Place your bets! Your choices are: "
        option_text += ", ".join(self.bet_options)
        option_text += " (use \"!bet <choice> <amount>\")."
        self.connMgr.send_message(option_text)
        self.connMgr.send_message('You have ' + str(bet_len) + 's, so get betting!')

        def bet_thread(self, countdown):
            def bet_winner(self, data):
                winner = data['args'][0]
                if winner in self.bet_options:
                    pay_winners(self,winner)
                    self.remove_command('!winner')
                else:
                    self.connMgr.send_message(winner + ' isn\'t a valid choice')

            time.sleep(countdown)
            if total_bets(self) == 0:
                self.connMgr.send_message('Betting has ended with no bets.')
                self.remove_command('!bet')
                return
            self.add_command('!winner', bet_winner)
            self.remove_command('!bet')
            self.connMgr.send_message(strings['CMD_BET_PRIZE_POOL'].format(amount=str(total_bets(self) + bet_rollover)))

        thread.start_new_thread(bet_thread, (self,bet_len))

def register_bet(self, data):
    global bet_rollover
    if len(data['args']) > 1:
        choice = data['args'][0].lower()
        try:
            amount = int(data['args'][1])
        except:
            amount = 0
        if amount <= 0:
            self.connMgr.send_message("Sorry " + data['sender'] + ", but that isn't a valid amount")
            return

        char = self.charMgr.load_character(data['sender_id'])

        if char['booty'] >= amount:
            if choice in self.bet_options:
                if not data['sender'] in list(chain.from_iterable([[b[0] for b in self.bet_entries[a]] for a in self.bet_entries])):
                    self.bet_entries[choice].append((data['sender'],amount))
                    char['booty'] -= amount
                    print "bet - " + str(amount)
                    bet_rollover += 2
                    print "rollover - " + str(bet_rollover)
                    self.charMgr.save_character(char)
                    self.connMgr.send_message(str(amount) + " placed on " + choice + " by " + data['sender'])
                else:
                    self.connMgr.send_message(data['sender'] + " you have already placed a bet!")
            else:
                self.connMgr.send_message("Sorry " + data['sender'] + ", but that isn't a valid choice")
        else:
            self.connMgr.send_message("Sorry " + data['sender'] + ", you don't have that much booty!")
    else:
        self.connMgr.send_message("To bet, it's: !bet <choice> <amount>")


def total_bets(self):
    total = 0
    for choice in self.bet_entries:
        for entry in self.bet_entries[choice]:
            total += entry[1]
    print self.bet_entries
    return total

def pay_winners(self, option):
    global bet_rollover
    winners = self.bet_entries[option]
    if winners:
        total = 0
        # get total for winners of THIS bet, so percentages are right
        for winner in winners:
            total += winner[1]
        win_str = "The bet winners are: "
        for winner in winners:
            pct = float(winner[1]) / total
            amt = int((total_bets(self) + bet_rollover) * pct)
            win_str += winner[0] + " - " + str(amt) + " (" + str(winner[1]) + ") "
            self.charMgr.give_booty(amt, [winner[0]])
        self.connMgr.send_message(win_str)
        bet_rollover = 0
    else:
        self.connMgr.send_message('No-one wins. Pot rolls over to next bet!')
        bet_rollover += total_bets(self)
    pass

# ------------------------------------------------------------------------------
