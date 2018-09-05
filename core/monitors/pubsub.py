import logging
import websocket
import thread
import time
import json
import ssl

from config.config import config

import modules.overlay.overlay as overlay
import utils.db_utils as db
import utils.twitch_utils as twitch


class pubsub():

    def __init__(self, grog=None, host=""):
        self.grog = grog
        self.HOST = host
        self.ws = None
        self.ping_ok = True

    # send PING
    def _ping(self, ws):
        # Send a ping Message
        print "PubSub:: PING!!!"
        self.ping_ok = False
        msg = {
            "type":"PING"
        }
        ws.send(json.dumps(msg))

    def _pong(self):
        # Handle pong response
        print "PubSub:: PONG!!!"
        self.ping_ok = True


    # send LISTEN
    def _listen(self, ws):
        print "Sending LISTEN"
        msg = {
            "type": "LISTEN",
            "nonce": "foobar",
            "data": {
                "topics": ["channel-bits-events-v1." + config['twitch']['channel_id'],"channel-subscribe-events-v1." + config['twitch']['channel_id'],"channel-commerce-events-v1." + config['twitch']['channel_id']],
                "auth_token": config['api']['access_token']
            }
        }

        ws.send(json.dumps(msg))

    # handle RESPONSE
    def _response(self, msg):
        print "Handling RESPONSE"
        if(msg["error"] != ""):
            print "Error found: '%s'" % msg["error"]

    # handle RECONNECT
    def _reconnect(self, ws):
        # Handle reconnect Messages
        ws.close()
        self.start()

    # handle Message
    def on_message(self, ws, message):
        msg = json.loads(message)
        print msg['type']
        mtype = msg['type']

        if mtype == "PONG":
            self._pong()
        elif mtype == "MESSAGE":
            self._message(msg['data'])
        elif mtype == "RESPONSE":
            self._response(msg)
        elif mtype == "RECONNECT":
            self._reconnect(ws)
        else:
            print "Unhandled type: " + mtype


    def _message(self, data):
        '''
        Bits:
        {
           "type": "MESSAGE",
           "data": {
              "topic": "channel-bits-events-v1.44322889",
              "message": "{\"data\":{\"user_name\":\"dallasnchains\",\"channel_name\":\"dallas\",\"user_id\":\"129454141\",\"channel_id\":\"44322889\",\"time\":\"2017-02-09T13:23:58.168Z\",\"chat_message\":\"cheer10000 New badge hype!\",\"bits_used\":10000,\"total_bits_used\":25000,\"context\":\"cheer\",\"badge_entitlement\":{\"new_version\":25000,\"previous_version\":10000}},\"version\":\"1.0\",\"message_type\":\"bits_event\",\"message_id\":\"8145728a4-35f0-4cf7-9dc0-f2ef24de1eb6\"}"
           }
        }
        '''

        if(data["topic"] == "channel-subscribe-events-v1." + config['twitch']['channel_id']):
            logging.info("PUBSUB: Sub event recieved")

#            sub_types = {
#                "Prime":"1",
#                "1000":"1",
#                "2000":"2",
#                "3000":"3"
#            }

            msg = json.loads(data['message'])

            if msg['sub_plan'] == 'Prime':
                msg['sub_plan'] = '1000'

            sub_type = msg['sub_plan']
            count = msg['months']
            #TODO: Remove Z once we clean up the DB
            time = msg['time'].split('.')[0] + "Z"
            context = msg['context']
            sub_message = msg['sub_message']

            # Send alert
            #TODO: update so higher sub tiers add more to the subathon timer
            if context == "sub" or context == "resub":
                name = msg['display_name']
                user_id = msg['user_id']
                if context == "sub":
                    timer = 10
                    self.grog.connMgr.send_message("Welcome new crewmate {0}!!!".format(name))
                else:
                    timer = 5
                    self.grog.connMgr.send_message("Welcome back {0}, {1} months at sea! YARRR!!!".format(name, count))
                if sub_type in ["1000","Prime"]:
                    #overlay.update_timer(timer)
                    pass
                elif sub_type == "2000":
                    #overlay.update_timer(timer * 2)
                    pass
                elif sub_type == "3000":
                    #overlay.update_timer(timer * 5)
                    pass
                self.grog.charMgr.give_booty(50, [name])

            elif context == "subgift":
                user_id = msg['recipient_id']
                name = msg['recipient_display_name']
                sender = msg['display_name']
                self.grog.connMgr.send_message("{1} slipped the kings shilling into {0}'s grog, welcome to the crew!!!".format(name, sender))
                if sub_type in ["1000","Prime"]:
                    #overlay.update_timer(10)
                    pass
                elif sub_type == "2000":
                    #overlay.update_timer(20)
                    pass
                elif sub_type == "3000":
                    #overlay.update_timer(50)
                    pass
                self.grog.charMgr.give_booty(50, [sender, name])

            else:
                print "NEW CONTEXT: " + context
                print msg
                return

            char = self.grog.charMgr.load_character(user_id)

            self.grog.charMgr.update_subscriber(char, time, sub_type, count)

            self.grog.charMgr.save_character(char)

            overlay.ship("sub", name, count)
            overlay.alert_sub(name, sub_type, count, context, sub_message['message'])

            #self.grog.charMgr.give_booty(50, [name])
            #overlay.ship("sub", name, count)
            #overlay.alert_sub(name, sub_type, count, context, sub_message)
            self.update_subcount()

            stat = db.add_stat('sessionSubs', 1)
            overlay.update_stat('subs', stat)

        elif (data["topic"] == "channel-bits-events-v1." + config['twitch']['channel_id']):
            logging.info("PUBSUB: Bits event received")

        elif (data["topic"] == "channel-commerce-events-v1." + config['twitch']['channel_id']):
            logging.info("PUBSUB: Commerce event received")


    def update_subcount(self):
        count = twitch.get_sub_points()
        count = count - 2
        db.clear_stat('subCount')
        stat = db.add_stat('subCount', int(count))
        logging.debug("New SubCount: " + str(stat))
        overlay.update_stat('subcount', stat)

    def on_error(self, ws, error):
        print error
        self._reconnect(ws)

    def on_close(self, ws):
        print "### closed ###"
        self._reconnect(ws)

    def on_open(self, ws):
        self._listen(ws)
        def run(*args):
            # ping!
            while(1):
                self._ping(ws)
                time.sleep(10)
                if(self.ping_ok == False):
                    self._reconnect(ws)
                time.sleep(230)
        thread.start_new_thread(run, ())

    def _connect(self):
        print "Connecting..."
        #websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp("wss://pubsub-edge.twitch.tv",
                                    on_message = self.on_message,
                                    on_error = self.on_error,
                                    on_close = self.on_close)
        self.ws.on_open = self.on_open
        self.ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

    def start(self):
        thread.start_new_thread(self._connect, ())
