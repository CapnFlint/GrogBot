from helper import *

def hello_hook(self, msg):
    # capnHi = 81912

    #hi_reg = '(^|\s)capnHi(\s)+'
    if msg['perms']['sub'] == True:
        if '81912' in msg['emotes'].keys():
            if msg['sender_id'] not in self.hellos:
                self.hellos.append(msg['sender_id'])
                overlay.alert_hello(msg['sender'])
    logging.debug('[MSG] ' + msg['sender'] + ": " + msg['text'])

self.register_hook(hello_hook)
