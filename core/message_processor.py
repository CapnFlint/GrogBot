import logging

import utils.db_utils as db

import modules.overlay.overlay as overlay

from modules.commands.helper import *
from modules.commands import *

import core.command_buffer as cmd_buffer

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

    def parse_command(self, msg):
        logging.debug('[CMD] ' + msg['sender'] + ": " + msg['text'])
        logging.debug('Sub: ' + str(msg['perms']['sub']))
        logging.debug('Mod: ' + str(msg['perms']['mod']))

        if len(msg['text']) >= 1:
            msg['args'] = msg['text'].split(' ')
            cmd = msg['args'].pop(0).lower()

            if self.grog.charMgr.is_alive(msg['sender']):
                if cmd in self.options.keys():
                    self.options[cmd](self, msg)
                elif cmd in self.custom_commands.keys():
                    self.grog.connMgr.send_message(self.custom_commands[cmd])
                else:
                    logging.debug("Unknown command: " + cmd)
            else:
                self.grog.connMgr.send_message('Shhhh ' + msg['sender'] + "... You're dead! capnRIP")


    def parse_message(self, msg): #, sender, perms, emotes):
        # Do any normal message parsing we need here, e.g. spam/banned word checks
        # capnHi = 81912

        #hi_reg = '(^|\s)capnHi(\s)+'
        print msg
        if msg['perms']['sub'] == '1':
            if '81912' in msg['emotes'].keys():
                if msg['sender_id'] not in self.seen_senders:
                    self.seen_senders.append(msg['sender_id'])
                    overlay.alert_hello(msg['sender'])
        logging.debug('[MSG] ' + msg['sender'] + ": " + msg['text'])



# -----[ Command Functions ]----------------------------------------------------

    def add_command(self, option, cmd):
        logging.info("Adding Command: " + option)
        self.options[option] = cmd

    def remove_command(self, option):
        if option in self.options:
            del self.options[option]

    def run_command(self, cmd, data = {}):
        logging.info("Running command: " + cmd)
        if not 'sender' in data.keys():
            data['sender'] = 'Capn_Flint'
            data['sender_id'] = '91580306'
            data['perms'] = {'mod':True,'sub':True}
        if cmd in self.options.keys():
            self.options[cmd](self, data)
        else:
            logging.warning("Command not valid: " + cmd)

    @processes('!quit', PERM_MOD)
    def command_quit(self, data):
        #self.run_command("!clearstats", [])
        self.grog.connMgr.send_message('Bye!')
        self.grog.connMgr.running = False

    @processes('!delete', PERM_ADMIN)
    def command_delete(self, data):
        target = data['args'][0]
        self.grog.charMgr.delete_character(target)
        self.grog.connMgr.send_message(target + ' has been deleted.')

    @processes('!event', PERM_MOD)
    def command_event(self, data):
        evtID = 0
        if data['args']:
            evtID = int(data['args'][0])
        if evtID > 0:
            self.grog.eventMgr.loadAndRun(evtID)
        else:
            self.grog.eventMgr.random_event()
