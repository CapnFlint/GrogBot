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
    def _ping(self):
        # Send a ping Message
        logging.debug("PING!!!")
        self.ping_ok = False
        msg = {
            "type":"PING"
        }
        self.ws.send(json.dumps(msg))

    def _pong(self):
        # Handle pong response
        logging.debug("PONG!!!")
        self.ping_ok = True


    # send LISTEN
    def _listen(self):
        logging.debug("Sending LISTEN")
        msg = {
            "type": "LISTEN",
            "nonce": "foobar",
            "data": {
                "topics": ["channel-bits-events-v1." + config['twitch']['channel_id'],"channel-subscribe-events-v1." + config['twitch']['channel_id'],"channel-commerce-events-v1." + config['twitch']['channel_id']],
                "auth_token": config['api']['access_token']
            }
        }

        self.ws.send(json.dumps(msg))

    # handle RESPONSE
    def _response(self, msg):
        logging.debug("Handling RESPONSE")
        if(msg["error"] != ""):
            logging.error("Error found: '%s'" % msg["error"])

    # handle RECONNECT
    def _reconnect(self):
        # Handle reconnect Messages
        self.ws.close()
        time.sleep(2)
        self.start()

    # handle Message
    def on_message(self, message):
        msg = json.loads(message)
        mtype = msg['type']

        if mtype == "PONG":
            self._pong()
        elif mtype == "MESSAGE":
            self._message(msg['data'])
        elif mtype == "RESPONSE":
            self._response(msg)
        elif mtype == "RECONNECT":
            self._reconnect()
        else:
            logging.error("Unhandled type: " + mtype)


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
            logging.info("Sub event recieved")

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
            # remove this in a few weeks once the full rollout is done...
            if 'months' in msg:
                streak = msg['months']
            else:
                streak = 0
            if 'cumulative_months' in msg:
                count = msg['cumulative_months']
            else:
                logging.error("cumulative_months missing! :(")
                #TODO: do something if no months provided. Perhaps compute?
                count = 1

            #TODO: Remove Z once we clean up the DB
            time = msg['time'].split('.')[0] + "Z"
            context = msg['context']
            
            sub_message = ""
            if 'sub_message' in msg:
                sub_message = msg['sub_message']

            # Send alert
            #TODO: update so higher sub tiers add more to the subathon timer
            if context == "sub" or context == "resub":
                name = msg['display_name']
                user_id = msg['user_id']
                if context == "sub":
                    timer = 6
                    self.grog.connMgr.send_message("Welcome new crewmate {0}!!!".format(name))
                else:
                    timer = 3
                    message = "Welcome back {0}, {1} total months at sea".format(name, count)
                    if streak:
                        message = message + " and {0} months in a row".format(streak)
                    message = message + "! YARRR!!!"
                    self.grog.connMgr.send_message(message)
                if sub_type in ["1000","Prime"]:
                    overlay.update_timer(timer)
                    pass
                elif sub_type == "2000":
                    overlay.update_timer(timer * 2)
                    pass
                elif sub_type == "3000":
                    overlay.update_timer(timer * 5)
                    pass
                self.grog.charMgr.give_booty(50, [name])

            elif context == "subgift":
                user_id = msg['recipient_id']
                name = msg['recipient_display_name']
                sender = msg['display_name']
                self.grog.connMgr.send_message("{1} slipped the kings shilling into {0}'s grog, welcome to the crew!!!".format(name, sender))
                if sub_type in ["1000","Prime"]:
                    overlay.update_timer(6)
                    pass
                elif sub_type == "2000":
                    overlay.update_timer(12)
                    pass
                elif sub_type == "3000":
                    overlay.update_timer(30)
                    pass
                self.grog.charMgr.give_booty(50, [sender, name])

            else:
                logging.error("NEW CONTEXT: " + context)
                logging.debug(msg)
                return

            char = self.grog.charMgr.load_character(user_id)
            if char:

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
            logging.info("Bits event received")

        elif (data["topic"] == "channel-commerce-events-v1." + config['twitch']['channel_id']):
            logging.info("Commerce event received")


    def update_subcount(self):
        count = twitch.get_sub_points()
        count = count - 2
        db.clear_stat('subCount')
        stat = db.add_stat('subCount', int(count))
        logging.debug("New SubCount: " + str(stat))
        overlay.update_stat('subcount', stat)

    def on_error(self, error):
        logging.error(error)
        self._reconnect()

    def on_close(self):
        logging.debug("### closed ###")
        self._reconnect()

    def on_open(self):
        logging.debug("on_open called")
        self._listen()
        def run(*args):
            # ping!
            try:
                while(1):
                    self._ping()
                    time.sleep(10)
                    if(self.ping_ok == False):
                        logging.error("Ping failed, reconnecting!")
                        self._reconnect()
                    time.sleep(230)
            except WebSocketConnectionClosedException:
                logging.debug("Socket closed, restarting!")
                self._reconnect()
        thread.start_new_thread(run, ())

    def _connect(self):
        logging.info("Connecting...")
        #websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp("wss://pubsub-edge.twitch.tv",
                                    on_message = self.on_message,
                                    on_error = self.on_error,
                                    on_close = self.on_close)
        self.ws.on_open = self.on_open
        self.ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

    def start(self):
        thread.start_new_thread(self._connect, ())
