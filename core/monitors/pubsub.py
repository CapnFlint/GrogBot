import logging
import websocket
import thread
import time
import json

import config.twitch_config as config

import modules.overlay.overlay as overlay
import utils.db_utils as db
import utils.twitch_utils as twitch


'''
config.access_token
'''

class pubsub():

    def __init__(self, grog=None, host=""):
        self.grog = grog
        self.HOST = host
        self.ws = None

    # send PING
    def _ping(self):
        # Send a ping Message
        pass

    def _pong(self):
        # Handle pong response
        pass

    # send LISTEN
    def _listen(self):
        print "Sending LISTEN"
        msg = {
            "type": "LISTEN",
            "nonce": "foobar",
            "data": {
                "topics": ["channel-bits-events-v1." + config.channel_id,"channel-subscribe-events-v1." + config.channel_id],
                "auth_token": config.access_token
            }
        }

        self.ws.send(json.dumps(msg))
        res = self.ws.recv()
        print "Received: '%s'" % res

    # handle RESPONSE
    def _response(self, msg):
        print "Handling RESPONSE"
        if(msg["error"] != ""):
            print "Error found: '%s'" % msg["error"]

    # handle RECONNECT
    def _reconnect(self):
        # Handle reconnect Messages
        pass

    # handle Message
    def on_message(self, msg):
        print msg
        mtype = msg['type']
        if mtype == "MESSAGE":
            self._handle_message(msg['message'])
        elif mtype == "RESPONSE":
            self._handle_response(msg)
        else:
            print "Unhandled type: " + mtype


    def _handle_message(self, msg):
        '''
        Bits:
        {
           "type": "MESSAGE",
           "data": {
              "topic": "channel-bits-events-v1.44322889",
              "message": "{\"data\":{\"user_name\":\"dallasnchains\",\"channel_name\":\"dallas\",\"user_id\":\"129454141\",\"channel_id\":\"44322889\",\"time\":\"2017-02-09T13:23:58.168Z\",\"chat_message\":\"cheer10000 New badge hype!\",\"bits_used\":10000,\"total_bits_used\":25000,\"context\":\"cheer\",\"badge_entitlement\":{\"new_version\":25000,\"previous_version\":10000}},\"version\":\"1.0\",\"message_type\":\"bits_event\",\"message_id\":\"8145728a4-35f0-4cf7-9dc0-f2ef24de1eb6\"}"
           }
        }

        Subs:
        {
           "type": "MESSAGE",
           "data": {
              "topic": "channel-subscribe-events-v1.44322889",
              "message": {
                 "user_name": "dallas",
                 "display_name": "dallas",
                 "channel_name": "twitch",
                 "user_id": "44322889",
                 "channel_id": "12826",
                 "time": "2015-12-19T16:39:57-08:00",
                 "sub_plan": "Prime"/"1000"/"2000"/"3000",
                 "sub_plan_name": "Mr_Woodchuck - Channel Subscription (mr_woodchuck)",
                 "months": 9,
                 "context": "sub"/"resub",
                 "sub_message": {
                    "message": "A Twitch baby is born! KappaHD",
                    "emotes": [
                    {
                       "start": 23,
                       "end": 7,
                       "id": 2867
                    }]
                 }
             }
           }
        }
        '''
        if(msg["topic"] == "channel-subscribe-events-v1." + config.channel_id):
            print "Sub message recieved!"

            sub_types = {
                "Prime":"1",
                "1000":"1",
                "2000":"2",
                "3000":"3"
            }

            name = msg['user_name']
            sub_type = sub_types[msg['sub_plan']]
            count = msg['months']
            time = msg['time']
            context = msg['context']
            sub_message = msg['sub_message']

            #TODO REMOVE ME when all of the database is updated, and code migrated to use ID
            grog.charMgr.update_id(name, user_id)

            grog.charMgr.add_sub(name, sub_type, time, count)

            # Confirm correct channel_id
            if msg['channel_id'] != config.channel_id:
                print "ERROR channel_id doesn't match"
                print msg['channel_id'] + " != " + config.channel_id
                return

            # Send alert
            #TODO: update so higher sub tiers add more to the subathon timer
            if context == "sub":
                self.grog.connMgr.send_message("Welcome to the inner circle, Pirate {0}!!!".format(name))
                if sub_type == "1":
                    overlay.update_timer(10)
                elif sub_type == "2":
                    overlay.update_timer(20)
                elif sub_type == "3":
                    overlay.update_timer(50)
            else:
                self.grog.connMgr.send_message("Welcome back {0}, {1} months at sea! YARRR!!!".format(name, count))
                if sub_type == "1":
                    overlay.update_timer(5)
                elif sub_type == "2":
                    overlay.update_timer(10)
                elif sub_type == "3":
                    overlay.update_timer(25)

            self.grog.charMgr.give_booty(50, [name])
            overlay.ship("sub", name, count)
            overlay.alert_sub(name, sub_type, dur, sub_message)
            self.update_subcount()

            stat = db.add_stat('sessionSubs', 1)
            overlay.update_stat('subs', stat)

    def update_subcount(self):
        count = twitch.get_sub_count()
        db.clear_stat('subCount')
        stat = db.add_stat('subCount', int(count))
        logging.debug("New SubCount: " + str(stat))
        overlay.update_stat('subcount', stat)

    def on_error(self, ws, error):
        print error


    def on_close(self, ws):
        print "### closed ###"

    def on_open(self, ws):
        def run(*args):
            # do things
            self._listen()
            pass
        thread.start_new_thread(run, ())

    def _connect(self):
        print "Connecting..."
        websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp("wss://pubsub-edge.twitch.tv",
                                    on_message = self.on_message,
                                    on_error = self.on_error,
                                    on_close = self.on_close)
        self.ws.on_open = self.on_open
        self.ws.run_forever()

    def start(self):
        thread.start_new_thread(self._connect, ())
