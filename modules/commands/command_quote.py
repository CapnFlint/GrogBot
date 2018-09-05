from helper import *
import utils.twitch_utils as twitch

"""
quoteid int not null primary key auto_increment
quote varchar(512) not null
date varchar(32) not null
name varchar(128) not null
game varchar(128) not null

!quote capn_flint here is a quote

Quote #123: "I like to make quotes!" - Capn_Flint 02-01-2015 (Creative)
"""

@processes("!addquote", PERM_MOD)
def command_addquote(self, data):
    if data['args'] and len(data['args']) > 1:
        name = data['args'][0].lower()
        quote = " ".join(data['args'][1:])
        if self.charMgr.char_exists(name):
            game = twitch.get_game("capn_flint")
            dname = twitch.get_user(twitch.get_ids([name])[name])['display_name']
            db.qu_add_quote(quote, dname, game)
            self.connMgr.send_message("quote successfully added!")
            return
        else:
            self.connMgr.send_message(name + " doesn't exist!")
            return
    self.connMgr.send_message("To add a quote use: !quote <char> <quote>")

# retrieves a quote
@processes("!quote")
def command_quote(self, data):
    quid = 0
    quote = ""
    if data['args']:
        try:
            quid = int(data['args'][0])
        except:
            quid = 0
        logging.debug(quid)
        if quid:
            quote = db.qu_get_quote_id(quid)
        else:
            quote = db.qu_get_quote()
    else:
        quote = db.qu_get_quote()

    if quote:
        self.connMgr.send_message(format_quote(quote))
    else:
        self.connMgr.send_message("No quote found...")

def format_quote(quote):
    #Quote #123: "I like to make quotes!" - Capn_Flint 02-01-2015 (Creative)
    return 'Quote #{0}: "{1}" - {2} {3} ({4})'.format(str(quote['id']), quote['quote'], quote['name'], quote['date'], quote['game'])
