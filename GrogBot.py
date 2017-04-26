#!/usr/bin/env python27
import logging

from core.message_processor import MessageProcessor
from core.connection_manager import ConnectionManager

from core.monitors.pubsub import pubsub
from core.monitors.follows import follows
from core.monitors.teespring import teespring
from core.monitors.bits import bits
from core.random_messages import random_messages

from modules.characters.character_manager import CharacterManager
from modules.events.event_manager import EventManager

import modules.overlay.overlay as overlay
import utils.db_utils as db

import config.twitch_config as twitch

class GrogBot():

    def __init__(self, channel):
        logging.basicConfig(level=logging.DEBUG)

        self.event_running = False

        self.channel = twitch.twitch_channel
        self.worklist = []

        # Set up all the managers, order is important!
        self.connMgr = ConnectionManager(self, channel)
        self.charMgr = CharacterManager(self)
        self.eventMgr = EventManager(self)
        self.msgProc = MessageProcessor(self)

        # Initialize all the worker threads
        self.add_worker(random_messages(self))
        self.add_worker(follows(self))
        self.add_worker(pubsub(self))
        #self.add_worker(bits(self))
        #self.add_worker(teespring(self, "spud citizen Capn_Flint", True))
        #self.add_worker(workers.twitter(self))

        overlay.update_stat("follows", db.get_stat("sessionFollowers"))
        overlay.update_stat("subs", db.get_stat("sessionSubs"))
        overlay.update_stat("lootcrate", db.get_stat("lootcrate"))

    def add_worker(self, worker):
        self.worklist.append(worker)

    def start_workers(self):
        for job in self.worklist:
            job.start()

    def run(self):
        # Start all the worker threads
        self.start_workers()

        # Connect and start bot
        logging.info("Starting Up!!!")
        self.connMgr.connect()


def main():
    grog = GrogBot(twitch.twitch_channel)
    grog.run()

if __name__ == "__main__":
    main()
