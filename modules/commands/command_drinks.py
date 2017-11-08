from helper import *

def buy_drink(self, name):
    char = self.charMgr.load_character(name)
    if char['booty'] >= 3:
        char['booty'] -= 3
        self.connMgr.send_message('hands ' + name + ' a fine frothy brew.')
        self.charMgr.save_character(char)
    else:
        self.connMgr.send_message("Sorry " + name + ", but you don't have enough booty to buy a drink.")

@processes('!ale')
@processes('!beer')
@processes('!rum')
@processes('!grog')
def command_buydrink(self, data):
    buy_drink(self, data['sender'])

@processes('!onthehouse', PERM_MOD)
def command_onthehouse(self, data):
    self.connMgr.send_message(data['sender'] + ' buys everyone a drink! Cheers!')
