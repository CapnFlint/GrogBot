import logging

import utils.twitch_utils as twitch
import utils.db_utils as db

import modules.overlay.overlay as overlay

from modules.commands.helper import *
from modules.commands import *

import core.workers as workers
import core.command_buffer as cmd_buffer
import config.twitch_config as config

from config.strings import strings

class MessageProcessor():

    def __init__(self, grog):
        self.grog = grog
        self.connMgr = grog.connMgr
        self.charMgr = grog.charMgr
        self.eventMgr = grog.eventMgr
        self.session_running = False
        self.commands = None
        self.options = command_dict
        self.raid_running = False
        self.cmdBuffer = cmd_buffer.command_buffer(self)
        self.cmdBuffer.start()
        self.seen_senders = []
        self.custom_commands = db.get_custom_commands()

    def add_custom_command(self, command, message):
        if command in self.options.keys():
            self.connMgr.send_message("Cannot overwrite core command: " + command)
        else:
            db.add_custom_command(command, message)
            self.custom_commands[command] = message
            self.connMgr.send_message("Command " + command + " added!")

    def remove_custom_command(self, command):
        if command in self.custom_commands:
            del self.custom_commands[command]
            db.del_custom_command(command)
            self.connMgr.send_message("Command " + command + " removed!")
        else:
            self.connMgr.send_message("Command " + command + " not found!")

    def parse_command(self, msg, sender, perms):
        logging.debug('[CMD] ' + sender + ": " + msg)
        logging.debug('[PERMS]' + str(perms))
        logging.debug('Sub: ' + str(self.grog.charMgr.subbed(sender)))

        if perms['sub'] and not self.grog.charMgr.subbed(sender):
            self.grog.charMgr.subbed(sender, force_check = True)

        if len(msg) >= 1:
            msg = msg.split(' ')[:-1]
            cmd = msg.pop(0).lower()

            if self.grog.charMgr.is_alive(sender):
                if cmd in self.options.keys():
                    self.options[cmd](self, sender, msg)
                elif cmd in self.custom_commands.keys():
                    self.grog.connMgr.send_message(self.custom_commands[cmd])
                else:
                    logging.debug("Unknown command: " + cmd)
            else:
                self.grog.connMgr.send_message('Shhhh ' + sender + "... You're dead! capnRIP")


    def parse_message(self, msg, sender, perms, emotes):
        # Do any normal message parsing we need here, e.g. spam/banned word checks
        # capnHi = 81912

        #hi_reg = '(^|\s)capnHi(\s)+'
        if perms['sub']:
            if '81912' in emotes.keys():
                if sender not in self.seen_senders:
                    self.seen_senders.append(sender)
                    overlay.alert_hello(sender)
        logging.debug('[MSG] ' + sender + ": " + msg)

    def parse_raid_message(self, msg, sender):
        if self.raid_running:
            if self.grog.charMgr.char_exists(sender):
                logging.debug(sender + " has taken part in the raid!!!")



# -----[ Command Functions ]----------------------------------------------------

    def add_command(self, option, cmd):
        logging.info("Adding Command: " + option)
        self.options[option] = cmd

    def remove_command(self, option):
        if option in self.options:
            del self.options[option]

    def run_command(self, cmd, args=[]):
        logging.info("Running command: " + cmd)
        if cmd in self.options.keys():
            self.options[cmd](self, config.twitch_channel, args)
        else:
            logging.warning("Command not valid: " + cmd)

    @processes('!quit', PERM_MOD)
    def command_quit(self, sender, args):
        #self.run_command("!clearstats", [])
        self.grog.connMgr.send_message('Bye!')
        self.grog.connMgr.running = False

    @processes('!delete', PERM_ADMIN)
    def command_delete(self, sender, args):
        target = args[0]
        self.grog.charMgr.delete_character(target)
        self.grog.connMgr.send_message(target + ' has been deleted.')

    @processes('!event', PERM_MOD)
    def command_event(self, sender, args):
        evtID = 0
        if args:
            evtID = int(args[0])
        if evtID > 0:
            self.grog.eventMgr.loadAndRun(evtID)
        else:
            self.grog.eventMgr.random_event()
