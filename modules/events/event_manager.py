import logging
import random
import thread
import time
from collections import defaultdict
import modules.overlay.overlay as overlay
import re
import utils.twitch_utils as twitch
import utils.db_utils as db

from events import EventThread

class EventManager():

    def __init__(self, grog):
        self.events = {}
        self.grog = grog
        self.entries = defaultdict(list)

        self.grog.add_worker(EventThread("Event-Thread", self))

# -----[ Event Management ]-----------------------------------------------------

    def random_event(self):
        #event = random.choice(eventList)
        event = db.getEvent();
        self.loadAndRun(event['eventID'])

    def loadAndRun(self, evtID=0, evtConfig=None):
        if not self.is_running():
            if not evtConfig:
                evtConfig = db.getEventById(evtID)
            event = Event(self, self.grog, evtConfig)
            self.start_event(event)

    def is_running(self):
        return self.grog.event_running

    def start_event(self, event):
        self.grog.event_running = True
        event.run()

    def end_event(self, next):
        self.grog.event_running = False
        if next:
            self.loadAndRun(int(random.choice(next.split(','))))

# -----[ Event Entry Management ]-----------------------------------------------

    def record_entry(self, entrant, choice):
        logging.debug("Trying to record an entry...")

        if entrant not in self.entries[choice]:
            self.entries[choice].append(entrant)

    def get_entries(self):
        return self.entries

    def get_all_entries(self, key=None):
        all = []
        logging.debug(self.entries)
        if key:
            all = all + self.entries[key]
        else:
            for key in self.entries.keys():
                all = all + self.entries[key]
        return all

    def get_top_entry(self):
        #TODO: Figure out a better way of doing this.
        top = ''
        topCount = 0
        if self.entries:
            for key in self.entries.keys():
                if not top:
                    logging.debug("Top set to: " + key + "(" + str(len(self.entries[key])) + ")")
                    top = key
                    topCount = len(self.entries[key])
                else:
                    logging.debug(str(len(self.entries[key])) + "::" + str(topCount))
                    if len(self.entries[key]) > topCount:
                        logging.debug("Top set to: " + key + "(" + str(len(self.entries[key])) + ")")
                        top = key
                        topCount = len(self.entries[key])
            return top
        else:
            return None

    def get_random_entry(self, key):
        if self.entries:
            return random.choice(self.entries[key])
        else:
            return None

    def reset_entries(self):
        self.entries = defaultdict(list)

# ------------------------------------------------------------------------------


class Event():

    def __init__(self, eventMgr, grog, evtConfig):
        self.eventMgr = eventMgr
        self.charMgr = grog.charMgr
        self.connMgr = grog.connMgr
        self.msgProc = grog.msgProc

        self.config = evtConfig

        self.prizeFund = 0
        self.running = False

    def end_event(self, next):
        self.running = False
        self.eventMgr.end_event(next)

    def is_running(self):
        logging.debug("Is it running? - " + str(self.running))
        return self.running

    def event_message(self, text):
        '''
        Use this to substitute in fancy things, like random viewer names etc
        TODO: Add rand_entry???
        '''
        if "#rand_user#" in text:
            viewers = twitch.get_viewers(False)
            if viewers:
                text = re.sub('#rand_user#', random.choice(viewers), text)
            else:
                text = re.sub('#rand_user#', 'A sailor', text)
        self.connMgr.send_message(text)

    def anon_instant_result(self, command, name):
        # I'm using c_self as the anonfunc's self is the callers self
        def anonfunc(c_self, data):
            self.connMgr.send_message(command['text'].format(data['sender']))
            self.charMgr.give_exp(command['exp'], [data['sender']])
            if command['exp'] > 0:
                self.connMgr.send_message(data['sender'] + " has gained experience! capnYarr")
            elif command['exp'] < 0:
                self.connMgr.send_message(data['sender'] + " has lost experience! capnFeels")
            c_self.remove_command(command['command'])
            self.end_event(command['next'])
        anonfunc.__name__ = name
        return anonfunc

    def anon_register_entry(self, command, name):
        def anonfunc(self, data):
            self.eventMgr.record_entry(data['sender'], command['command'])
        anonfunc.__name__ = name
        return anonfunc

    def fail_event(self):
        self.charMgr.give_exp(self.config['exp'])
        self.event_message(self.config['timeout'])
        self.end_event(self.config['next'])

    def exp_booty_message(self, exp, booty, users):
        if users:
            if exp != 0:
                if exp > 0:
                    self.connMgr.send_message("The following pirates gained experience: " + ', '.join(users) + " capnYarr")
                elif exp < 0:
                    self.connMgr.send_message("The following pirates lost experience: " + ', '.join(users) + " capnFeels")
            if booty != 0:
                if booty > 0:
                    self.connMgr.send_message("The following pirates gained booty: " + ', '.join(users) + " capnBooty")
                elif booty < 0:
                    self.connMgr.send_message("The following pirates lost booty: " + ', '.join(users))

    def run(self):
        self.running = True
        self.commands = db.getEventCommands(self.config['eventID'])
        logging.debug(self.commands)
        for command in self.commands:
            if self.config['type'] == 1:
                self.msgProc.add_command(command['command'], self.anon_instant_result(command, command['command'].lstrip('!')))

            elif self.config['type'] in [2,3,4,5]:
                self.msgProc.add_command(command['command'], self.anon_register_entry(command, command['command'].lstrip('!')))

        if self.config['text']:
            self.event_message(self.config['text'])

        def timer_thread(countdown):
            time.sleep(countdown)
            user = ''
            commands = self.commands
            command = None

            if self.config['type'] == 1:
                # Do nothing. Handled as an instant result.
                pass

            if self.config['type'] == 2:
                command = self.commands[0]
                entries = self.eventMgr.get_all_entries(command['command'])

            elif self.config['type'] == 3:
                command = self.commands[0]
                winner = self.eventMgr.get_random_entry(command['command'])

            elif self.config['type'] == 4:
                top = self.eventMgr.get_top_entry()
                entries = self.eventMgr.get_all_entries(top)
                for cmd in self.commands:
                    if cmd['command'] == top:
                        command = cmd

            elif self.config['type'] == 5:
                entryDict = {}
                for cmd in self.commands:
                    entryDict[cmd['command']] = self.eventMgr.get_all_entries(cmd['command'])

            # clean up
            self.eventMgr.reset_entries()
            for cmd in self.commands:
                self.msgProc.remove_command(cmd['command'])

            # Granting exp
            if self.config['type'] == 1: # do nothing, handled in the command
                if self.is_running():
                    self.fail_event()

            elif self.config['type'] == 2:
                if entries:
                    self.charMgr.give_exp(command['exp'], entries)
                    self.charMgr.give_booty(command['booty'], entries)
                    if command['text']:
                        self.event_message(command['text'])
                    self.exp_booty_message(command['exp'], command['booty'], entries)
                    self.end_event(command['next'])
                else:
                    self.fail_event()

            elif self.config['type'] == 3:
                if winner:
                    self.charMgr.give_exp(command['exp'], [winner])
                    self.charMgr.give_booty(command['booty'], [winner])
                    if command['text']:
                        self.event_message(command['text'].format(winner))
                    self.exp_booty_message(command['exp'], command['booty'], [winner])
                    self.end_event(command['next'])
                else:
                    self.fail_event()

            elif self.config['type'] == 4:
                if top:
                    self.charMgr.give_exp(command['exp'], entries)
                    self.charMgr.give_booty(command['booty'], entries)
                    if command['text']:
                        self.event_message(command['text'])
                    self.exp_booty_message(command['exp'], command['booty'], entries)
                    self.end_event(command['next'])
                else:
                    self.fail_event()

            elif self.config['type'] == 5:
                if entryDict:
                    logging.debug(entryDict)
                    winner = random.choice(self.commands)
                    exp = commands[0]['exp']
                    booty = commands[0]['booty']
                    win_entries = []
                    lose_entries = []
                    for cmd in commands:
                        entries = entryDict[cmd['command']]
                        logging.debug(cmd['command'] + " = " + str(entries))
                        if entries:
                            if cmd['command'] == winner['command']:
                                win_entries += entries
                                self.charMgr.give_exp(exp, entries)
                                self.charMgr.give_booty(booty, entries)
                            else:
                                lose_entries += entries
                                self.charMgr.give_exp(-exp, entries)
                                self.charMgr.give_booty(-booty, entries)

                    if winner['text']:
                        self.event_message(winner['text'])

                    self.exp_booty_message(exp, booty, win_entries)
                    self.exp_booty_message(-exp, -booty, lose_entries)
                    self.end_event(winner['next'])
                else:
                    self.fail_event()

        thread.start_new_thread(timer_thread, (self.config['timer'],))
