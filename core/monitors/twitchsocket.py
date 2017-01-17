import json
import websocket
import random
import thread
import time

import config.twitch_config as config

'''
connect to wss://pubsub-edge.twitch.tv
send ping every 5 minutes, pong within 10 seconds or reconnect
must listen to topic within 15 seconds
must reconnect after receiving reconnect message
'''

class twitchsocket():
    def __init__(self, topics, handler):
        self.handler = handler
        self.topics = topics
        self.running = False
        websocket.enableTrace(True)
        self.connect()

    def on_message(self, ws, message):
        msg = json.loads(message)

        # handle messages for pings and reconnects
        if msg['type'] = "PONG":
            self.handle_pong()

        elif msg['type'] = "RECONNECT":
            self.reconnect(ws)

        elif msg['type'] = "MESSAGE":
            self.handler(msg['data'])
        # send everything else to handler
    else:
        self.handler(data)


    def on_error(self, ws, error):
        self.running = False
        print error

    def on_close(self, ws):
        print "### closed ###"
        self.connect()

    def on_open(self, ws):
        self.running = True;
        def run(*args):
            #ping loop
            while 1:
                if not self.running == True:
                    break
                time.sleep(180)
                self.send_ping(ws)
            ws.close()
            print "thread terminating..."
        thread.start_new_thread(run, ())

    def generate_nonce(self, length=8):
        """Generate pseudorandom number."""
        return ''.join([str(random.randint(0, 9)) for i in range(length)])

    def connect(self):
        ws = websocket.WebSocketApp("wss://pubsub-edge.twitch.tv",
                                  on_message = self.on_message,
                                  on_error = self.on_error,
                                  on_close = self.on_close)
        ws.on_open = self.on_open
        ws.run_forever()

    def register(self):
        data = {}
        data['topics'] = self.topics
        data['auth_token'] = config.access_token
        message = {}
        message['type'] = "LISTEN"
        message['nonce'] = self.generate_nonce()
        message['data'] = data

    def send_ping(self, ws):
        ws.send('{"type":"PING"}')

    def handle_pong(self, data):
        # do some checking here to make sure we are still connected...
        pass

    def reconnect(self, ws):
        ws.close()
        self.connect()
