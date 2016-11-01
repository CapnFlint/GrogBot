import urllib2
import urllib
import json
import random

import utils.db_utils as db
import utils.twitch_utils as utils

from websocket import create_connection


def alert(priority, text, sound=[]):
    data = {}
    data['priority'] = priority
    data['text'] = text
    data['audio'] = sound
    _send_message("alert", data)

def sound(filename, volume, priority=3):
    data = {}
    data['priority'] = priority
    data['file'] = filename
    data['volume'] = volume
    _send_message("sound", data)

''' Messages '''

def alert_follow(name, audio=False):
    data = {}
    data['priority'] = 3
    data['text'] = "[HL]{0}[/HL] has boarded the ship! Welcome!".format(name)
    if audio:
        #data['audio'] = [{"file":"sounds/hell.ogg", "volume":40}]
        laughs = ["laugh1.mp3","laugh2.mp3","laugh3.mp3","laugh4.mp3","laugh5.mp3"]
        data['audio'] = [{"file": "sounds/welcome.mp3", "volume": 40},{"file": "sounds/{0}".format(random.choice(laughs)), "volume": 40}]
    _send_message("alert", data)

def alert_event():
    data = {}
    data['priority'] = 2
    data['text'] = "An event has started!"
    data['audio'] = []
    _send_message("alert", data)

def alert_levelup(name, rank):
    data = {}
    data['priority'] = 4
    data['text'] = "[HL]{0}[/HL] is now rank [HL]{1}[/HL]! Congratulations!".format(name, rank)
    data['audio'] = [{"file": "sounds/levelup.wav", "volume": 15}]
    _send_message("alert", data)

def alert_tip(name, amount, message=""):
    data = {}
    data['priority'] = 1
    data['text'] = "[HL]{0}[/HL] has donated [HL]${1}[/HL]! Give them some love!!!".format(name, format(amount, '.2f'))
    if amount > 5.0:
        data['audio'] = []
    else:
        data['audio'] = []
    data['message'] = message
    _send_message("alert", data)

def alert_teespring(count):
    data = {}
    data['audio'] = [{"file": "sounds/narwhals.mp3", "volume": 40}]
    data['count'] = count
    _send_message("teespring", data)

def alert_hello(sender):
    data = {}
    data['priority'] = 3
    data['text'] = "Ahoy there [HL]{0}[/HL]!".format(sender)
    data['audio'] = []
    _send_message("alert", data)

def alert_sub(sender):
    data = {}
    data['priority'] = 1
    data['text'] = "[HL]{0}[/HL] has just subscribed!!! Welcome to the inner circle!".format(sender)
    data['audio'] = [{"file": "sounds/pirate2.mp3", "volume": 50}]
    _send_message("alert", data)
    #ship("sub", sender, 1)

def alert_resub(sender, count, message):
    data = {}
    data['priority'] = 1
    data['text'] = "[HL]{0}[/HL] subbed for another month, [HL]{1}[/HL] months at sea!!!".format(sender, count)
    data['audio'] = [{"file": "sounds/pirate2.mp3", "volume": 50}]
    data['message'] = message
    _send_message("alert", data)
    #ship("sub", sender, count)

''' Twitter '''

def twitter_mention(mention):
    data = {}
    data['image'] = mention['image']
    data['user'] = mention['user']
    data['name'] = mention['name']
    data['text'] = mention['text']
    data['audio'] = [{"file" : "sounds/tweet.mp3", "volume" : 80}]
    _send_message("twitter",data)

def twitter_retweet(mention):
    data = {}
    data['image'] = mention['image']
    data['user'] = mention['user']
    data['name'] = mention['name']
    data['text'] = "Retweeted the stream! Thank you!!!"
    data['audio'] = [{"file" : "sounds/tweet.mp3", "volume" : 80}]
    _send_message("twitter", data)

''' giveaway '''

def giveaway_start(item):
    data = {}
    data['action'] = "show"
    data['text'] = item
    data['audio'] = [{"file": "sounds/giveaway1.mp3", "volume": "40"}]
    _send_message("giveaway", data)

def giveaway_end():
    data = {}
    data['action'] = "hide"
    _send_message("giveaway", data)

def giveaway_winner(name, entries):
    data = {}
    data['action'] = "winner"
    data['winner'] = name
    data['entries'] = entries
    data['text'] = "[HL]{0}[/HL] has won the giveaway! Congratulations! Be sure to [claim] the prize :)".format(name)
    _send_message("giveaway", data)

''' ships '''

def ship(stype, name, count):
    data = {}
    data['type'] = stype
    data['name'] = name
    data['count'] = count
    _send_message("ships", data)

''' emotes '''

def send_emotes(sender, emotes):
    data = {}
    data['emotes'] = []
    _send_message("emotes", data)

''' stats '''

def update_stat(stat, value):
    data = {}
    data['stat'] = stat
    data['value'] = value
    print data
    _send_message("stats", data)

''' timer '''

def update_timer(minutes):
    data = {}
    data['action'] = "update"
    data['minutes'] = minutes
    _send_message("timer", data)

def fix_timer(minutes):
    data = {}
    data['action'] = "fix"
    data['minutes'] = minutes
    _send_message("timer", data)

''' handler '''

def _send_message(handler, data):
    message = {}
    message['handler'] = handler
    message['data'] = data
    ws = create_connection("ws://capnflint.com:9001")
    ws.send(json.dumps(message))
    ws.recv()
    ws.close()
