import urllib2
import urllib
import json
import logging

import config.twitch_config as twitch

def get_viewers(include_mods = True):
    url = "http://tmi.twitch.tv/group/user/{0}/chatters?client_id={1}".format(twitch.twitch_channel, twitch.client_id)
    try:
        response = urllib2.urlopen(url)
        userlist = json.load(response)['chatters']
        users = userlist['viewers']
        if include_mods:
            users = (users + userlist['moderators'] +
                    userlist['global_mods'] +
                    userlist['admins'] +
                    userlist['staff'])
        return users
    except urllib2.URLError:
        logging.error("get_viewers: urllib2 error")
        return {}

def get_mods():
    url = "http://tmi.twitch.tv/group/user/{0}/chatters?client_id={1}".format(twitch.twitch_channel, twitch.client_id)
    try:
        response = urllib2.urlopen(url)
        userlist = json.load(response)['chatters']
        users = userlist['moderators']
        return users
    except urllib2.URLError:
        logging.error("get_mods: urllib2 error")
        return {}

def get_display_name(name):
    url = "https://api.twitch.tv/kraken/users/" + name + "?client_id=" + twitch.client_id
    try:
        response = urllib2.urlopen(url)
        data = json.load(response)
        if 'error' in data.keys():
            return name
        return data['display_name']
    except urllib2.URLError:
        logging.error("get_display_name: urllib2 error")
        return name

def get_game(name):
    url = "https://api.twitch.tv/kraken/channels/" + name + "?client_id=" + twitch.client_id
    try:
        response = urllib2.urlopen(url)
        data = json.load(response)
        if 'error' in data.keys():
            return None
        return data['game']
    except urllib2.URLError:
        logging.error("get_game: urllib2 error")
        return None

def get_viewcount():
    url = "https://api.twitch.tv/kraken/streams/{0}?client_id={1}".format(twitch.twitch_channel, twitch.client_id)
    try:
        response = urllib2.urlopen(url)
        data = json.load(response)
        if data['stream']:
            return data['stream']['viewers']
        else:
            return 0
    except urllib2.URLError:
        logging.error("urllib2 error - get_viewcount")
        return 0

def get_starttime():
    url = "https://api.twitch.tv/kraken/streams/{0}?client_id={1}".format(twitch.twitch_channel, twitch.client_id)
    try:
        response = urllib2.urlopen(url)
        data = json.load(response)
        if data['stream']:
            return data['stream']['created_at']
        else:
            return 0
    except urllib2.URLError:
        logging.error("urllib2 error - get_starttime")
        return 0

def check_streamer(name):
    url = "https://api.twitch.tv/kraken/channels/" + name + "?client_id=" + twitch.client_id
    try:
        response = urllib2.urlopen(url)
        data = json.load(response)
        if 'error' in data.keys():
            return None
        return data
    except urllib2.URLError:
        logging.error("urllib2 error - check_streamer")
        return None

def check_follower(name):
    url = "https://api.twitch.tv/kraken/users/{0}/follows/channels/{1}?api_version=3&client_id={2}".format(name, twitch.twitch_channel, twitch.client_id)
    if name == twitch.twitch_channel:
        return True
    try:
        response = urllib2.urlopen(url)
        data = json.load(response)
        if 'error' in data.keys():
            return False
        return True
    except:
        logging.error("urllib2 error - check_follower")
        return False

def check_subscriber(name, channel):
    url = "https://api.twitch.tv/kraken/channels/{0}/subscriptions/{1}?api_version=3&client_id={2}".format(twitch.twitch_channel, name, twitch.client_id)

    try:
        req = urllib2.Request(url)
        req.add_header('Authorization', 'OAuth '+twitch.access_token)
        response = urllib2.urlopen(req)
        data = json.load(response)
        #print data['created_at']
        if 'error' in data.keys():
            return ""
        return data['created_at']
    except urllib2.HTTPError, e:
        logging.info(name + " is no longer subscribed!")
        return ""
    except urllib2.URLError, e:
        logging.error("urllib2 error - check_subscriber")
        return ""

def get_latest_follows(count):
    url = "https://api.twitch.tv/kraken/channels/{0}/follows?limit={1}&api_version=3&client_id={2}".format(twitch.twitch_channel, str(int(count)), twitch.client_id)
    try:
        response = urllib2.urlopen(url)
        userlist = json.load(response)['follows']
        users = []
        for item in userlist:
            users.append(item['user']['display_name'])
        return users
    except urllib2.URLError:
        logging.error("urllib2 error - get_latest_follows")
        return {}

def get_latest_subscribers(count, offset=0):
    url = "https://api.twitch.tv/kraken/channels/{0}/subscriptions?limit={1}&direction=desc&offset={2}&api_version=3&client_id={3}".format(twitch.twitch_channel, count, offset, twitch.client_id)
    try:
        req = urllib2.Request(url)
        req.add_header('Authorization', 'OAuth '+twitch.access_token)
        response = urllib2.urlopen(req)
        data = json.load(response)
        userlist = data['subscriptions']
        users = []
        for item in userlist:
            users.append(item['user']['name'])
        return users
    except urllib2.URLError:
        logging.error("urllib2 error - get_latest_subscribers")
        return {}

def get_sub_count():
    url = "https://api.twitch.tv/kraken/channels/{0}/subscriptions?limit={1}&direction=desc&offset={2}&api_version=3&client_id={3}".format(twitch.twitch_channel, 1, 0, twitch.client_id)
    try:
        req = urllib2.Request(url)
        req.add_header('Authorization', 'OAuth '+twitch.access_token)
        response = urllib2.urlopen(req)
        data = json.load(response)
        count = int(data['_total']) - 2
        print "Total Subscribers: " + str(count)
        return count
    except urllib2.URLError:
        logging.error("urllib2 error - get_sub_count")
        return 0

def get_subscribers(count=100, offset=0):
    url = "https://api.twitch.tv/kraken/channels/{0}/subscriptions?limit={1}&direction=desc&offset={2}&api_version=3&client_id={3}".format(twitch.twitch_channel, count, offset, twitch.client_id)
    print "Retrieving subs " + str(offset) + " to " + str(offset + count)
    try:
        req = urllib2.Request(url)
        req.add_header('Authorization', 'OAuth '+twitch.access_token)
        response = urllib2.urlopen(req)
        data = json.load(response)
        userlist = data['subscriptions']
        total = int(data['_total']) - 2
        users = []
        for item in userlist:
            users.append(item['user']['name'])
        if (len(users) + offset) < total:
            users = users + get_subscribers(count=100, offset=offset + count)
        return users
    except urllib2.URLError:
        logging.error("urllib2 error - get_subscribers")
        return {}
