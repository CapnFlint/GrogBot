#!/usr/bin/env python27

from core.message_processor import MessageProcessor
from core.connection_manager import ConnectionManager
import core.workers as workers

from modules.characters.character_manager import CharacterManager
from modules.events.event_manager2 import EventManager

import modules.overlay.overlay as overlay
import utils.db_utils as db

import config.twitch_config as config

class GrogBot():

    def __init__(self, channel):
        self.event_running = False

        self.channel = config.twitch_channel

        # Set up all the managers, order is important!
        self.connMgr = ConnectionManager(self, channel)
        self.charMgr = CharacterManager(self)
        self.eventMgr = EventManager(self)
        self.msgProc = MessageProcessor(self)

        # Initialize all the worker threads
        self.worklist = []
        self.add_worker(workers.passive_exp(self))
        self.add_worker(workers.events(self))
        self.add_worker(workers.messages(self))
        self.add_worker(workers.followers(self))
        self.add_worker(workers.teespring(self, "spud citizen Capn_Flint", True))
        #self.add_worker(workers.twitter(self))

        overlay.update_stat("follows", db.get_stat("sessionFollowers"))
        overlay.update_stat("subs", db.get_stat("sessionSubs"))

    def add_worker(self, worker):
        self.worklist.append(worker)

    def start_workers(self):
        for job in self.worklist:
            job.start()

    def run(self):
        # Start all the worker threads
        self.start_workers()

        # Connect and start bot
        print "Starting Up!!!"
        self.connMgr.connect()

def main():
    grog = GrogBot(self.channel)
    grog.run()

if __name__ == "__main__":
    main()
