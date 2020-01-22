from helper import *

def buy_drink(self, uid):
    char = self.charMgr.load_character(uid)
    if char and char['booty'] >= 3:
        char['booty'] -= 3
        self.connMgr.send_message('hands ' + char['name'] + ' a fine beverage.')
        self.charMgr.save_character(char)
    else:
        self.connMgr.send_message("Sorry " + char['name'] + ", but you don't have enough booty to buy a drink.")

@processes('!ale')
@processes('!beer')
@processes('!rum')
@processes('!grog')
def command_buydrink(self, data):
    buy_drink(self, data['sender_id'])

@processes('!onthehouse', PERM_MOD)
def command_onthehouse(self, data):
    self.connMgr.send_message(data['sender'] + ' buys everyone a drink! Cheers!')
