import urllib2
import urllib
import json
import logging
import random

import utils.db_utils as db
import utils.twitch_utils as utils

from websocket import create_connection

from config.config import config

farts = False

def get_fart():
    return 'sounds/fart' + str(random.choice(range(1,19))) + '.mp3'

def alert(priority, text, sound=[]):
    global farts
    data = {}
    data['priority'] = priority
    data['text'] = text
    if farts:
        sound = [{"file":get_fart(),"volume":80}]
    data['audio'] = sound
    _send_message("alert", data)

def sound(filename, volume, priority=3):
    global farts
    data = {}
    data['priority'] = priority
    if farts:
        data['file'] = get_fart()
        data['volume'] = 80
    else:
        data['file'] = filename
        data['volume'] = volume
    _send_message("sound", data)

''' Messages '''

def alert_follow(name, audio=False):
    global farts
    data = {}
    data['priority'] = 3
    data['text'] = "[HL]{0}[/HL] has boarded the ship! Welcome!".format(name)
    audio = False
    if audio:
        if farts:
            data['audio'] = [{"file": get_fart(), "volume":80}]
        else:
            #data['audio'] = [{"file":"sounds/hell.ogg", "volume":40}]
            laughs = ["laugh1.mp3","laugh2.mp3","laugh3.mp3","laugh4.mp3","laugh5.mp3"]
            data['audio'] = [{"file": "sounds/welcome.mp3", "volume": 40},{"file": "sounds/{0}".format(random.choice(laughs)), "volume": 40}]
    _send_message("alert", data)

def alert_levelup(name, rank):
    global farts
    if farts:
        sound = get_fart()
        volume = 80
    else:
        sound = "sounds/levelup.wav"
        volume = 15
    data = {}
    data['priority'] = 4
    data['text'] = "[HL]{0}[/HL] is now rank [HL]{1}[/HL]! Congratulations!".format(name, rank)
    data['audio'] = [{"file": sound, "volume": volume}]
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
    if farts:
        audio = {"file":get_fart(), "volume":60}
    else:
        audio = None
    data = {}
    data['priority'] = 3
    data['text'] = "Ahoy there [HL]{0}[/HL]!".format(sender)
    data['audio'] = [audio]
    _send_message("alert", data)

def alert_sub(sender, sub_type="1000", count="1", context="sub", message=""):
    global farts

    data = {}
    data['priority'] = 1

    if farts:
        sound = get_fart()
        volume = 80
        data['audio'] = [{"file": sound, "volume": volume}]
    else:
        if sub_type == "1000":
            #laughs = ["laugh1.mp3","laugh2.mp3","laugh3.mp3","laugh4.mp3","laugh5.mp3"]
            #data['audio'] = [{"file": "sounds/welcome.mp3", "volume": 40},{"file": "sounds/{0}".format(random.choice(laughs)), "volume": 40}]
            sound = "sounds/pirate2.mp3"
            volume = 50
            data['audio'] = [{"file": sound, "volume": volume}]
        if sub_type == "2000":
            sound = "sounds/pirate2.mp3"
            volume = 50
            data['audio'] = [{"file": sound, "volume": volume}]
        if sub_type == "3000":
            sound = "sounds/dubpirate.mp3"
            volume = 50
            data['audio'] = [{"file": sound, "volume": volume}]

    if context == "sub":
        data['text'] = "[HL]{0}[/HL] has just subscribed!!! Welcome to the inner circle!".format(sender)
    else:
        data['text'] = "[HL]{0}[/HL] subbed for another month, [HL]{1}[/HL] months at sea!!!".format(sender, count)

    data['message'] = message
    _send_message("alert", data)


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
    data['emotes'] = emotes
    data['sender'] = sender
    _send_message("emotes", data)

''' raiders! '''

def start_raid(raider, logo, emotes):
    data = {}
    data['action'] = "start"
    data['raider'] = raider
    data['logo'] = logo
    data['crew_emotes'] = emotes
    data['audio'] = [{"file": "sounds/raid_defence.mp3", "volume": "70"}]
    _send_message("raid", data)

''' stats '''

def update_stat(stat, value):
    data = {}
    data['stat'] = stat
    data['value'] = value
    logging.debug(data)
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

def set_timer(minutes):
    data = {}
    data['action'] = "set"
    data['minutes'] = minutes
    _send_message("timer", data)

''' handler '''

def _send_message(handler, data):
    try:
        message = {}
        message['handler'] = handler
        message['data'] = data
        ws = create_connection("wss://localhost:9002/", sslopt={“cert_reqs”: ssl.CERT_NONE})
        #logging.debug("Sending Auth: " + config['websocket']['secret'])
        ws.send("AUTH:" + config['websocket']['secret'])
        #logging.debug("Sending Message: " + json.dumps(message))
        ws.send(json.dumps(message))
        ws.recv()
        ws.close()
    except:
        logging.error("Websocket not available...")
