import urllib2
import urllib
import json
import logging

from config.config import config

def get_ids(names):
    url = "https://api.twitch.tv/kraken/users?login=" + ','.join(names)
    try:
        req = urllib2.Request(url)
        req.add_header('Accept', 'application/vnd.twitchtv.v5+json')
        req.add_header('Client-ID', config['api']['client_id'])
        response = urllib2.urlopen(req)
        data = json.load(response)
        print data
        if 'error' in data.keys():
            return {}
        results = {}
        for user in data["users"]:
            results[user['name']] = user['_id']
        return results
    except urllib2.URLError:
        logging.error("urllib2 error - get_ids")
        return None

def get_viewers(include_mods = True):
    url = "http://tmi.twitch.tv/group/user/{0}/chatters?client_id={1}".format(config['twitch']['channel'], config['api']['client_id'])
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
    url = "http://tmi.twitch.tv/group/user/{0}/chatters?client_id={1}".format(config['twitch']['channel'], config['api']['client_id'])
    try:
        response = urllib2.urlopen(url)
        userlist = json.load(response)['chatters']
        users = userlist['moderators']
        return users
    except urllib2.URLError:
        logging.error("get_mods: urllib2 error")
        return {}

def get_display_name(uid):
    url = "https://api.twitch.tv/kraken/users/" + config['twitch']['channel_id']
    try:
        req = urllib2.Request(url)
        req.add_header('Accept', 'application/vnd.twitchtv.v5+json')
        req.add_header('Client-ID', config['api']['client_id'])
        response = urllib2.urlopen(req)
        data = json.load(response)
        if 'error' in data.keys():
            return name
        return data['display_name']
    except urllib2.URLError:
        logging.error("get_display_name: urllib2 error")
        return name

def get_game(name):
    name = name.lower()
    if name == "capn_flint":
        channel_id = config['twitch']['channel_id']
    else:
        channel_id = get_ids([name])[name]
    url = "https://api.twitch.tv/kraken/channels/" + channel_id
    try:
        req = urllib2.Request(url)
        req.add_header('Accept', 'application/vnd.twitchtv.v5+json')
        req.add_header('Client-ID', config['api']['client_id'])
        response = urllib2.urlopen(req)
        data = json.load(response)
        if 'error' in data.keys():
            return None
        return data['game']
    except urllib2.URLError:
        logging.error("get_game: urllib2 error")
        return None

def get_viewcount():
    url = "https://api.twitch.tv/kraken/streams/{0}".format(config['twitch']['channel_id'])
    try:
        req = urllib2.Request(url)
        req.add_header('Accept', 'application/vnd.twitchtv.v5+json')
        req.add_header('Client-ID', config['api']['client_id'])
        response = urllib2.urlopen(req)
        data = json.load(response)
        if data['stream']:
            return data['stream']['viewers']
        else:
            return 0
    except urllib2.URLError:
        logging.error("urllib2 error - get_viewcount")
        return 0

def get_starttime():
    url = "https://api.twitch.tv/kraken/streams/{0}".format(config['twitch']['channel_id'])
    try:
        req = urllib2.Request(url)
        req.add_header('Accept', 'application/vnd.twitchtv.v5+json')
        req.add_header('Client-ID', config['api']['client_id'])
        response = urllib2.urlopen(req)
        data = json.load(response)
        if data['stream']:
            return data['stream']['created_at']
        else:
            return 0
    except urllib2.URLError:
        logging.error("urllib2 error - get_starttime")
        return 0

def check_streamer(name):
    name = name.lower()
    channel_id = get_ids([name])[name]
    url = "https://api.twitch.tv/kraken/channels/" + channel_id
    try:
        req = urllib2.Request(url)
        req.add_header('Accept', 'application/vnd.twitchtv.v5+json')
        req.add_header('Client-ID', config['api']['client_id'])
        response = urllib2.urlopen(req)
        data = json.load(response)
        if 'error' in data.keys():
            return None
        return data
    except urllib2.URLError:
        logging.error("urllib2 error - check_streamer")
        return None

def check_follower(name):
    name = name.lower()
    user_id = get_ids([name])[name]
    url = "https://api.twitch.tv/kraken/users/{0}/follows/channels/{1}".format(user_id, config['twitch']['channel_id'])
    if name == config['twitch']['channel']:
        return True
    try:
        req = urllib2.Request(url)
        req.add_header('Accept', 'application/vnd.twitchtv.v5+json')
        req.add_header('Client-ID', config['api']['client_id'])
        response = urllib2.urlopen(req)
        data = json.load(response)
        if 'error' in data.keys():
            return False
        return True
    except:
        logging.error("urllib2 error - check_follower")
        return False

def check_subscriber(name, channel):
    name = name.lower()
    user_id = get_ids([name])[name]
    url = "https://api.twitch.tv/kraken/channels/{0}/subscriptions/{1}".format(config['twitch']['channel_id'], user_id)

    try:
        req = urllib2.Request(url)
        req.add_header('Accept', 'application/vnd.twitchtv.v5+json')
        req.add_header('Client-ID', config['api']['client_id'])
        req.add_header('Authorization', 'OAuth '+config['api']['access_token'])
        response = urllib2.urlopen(req)
        data = json.load(response)
        #print data['created_at']
        if 'error' in data.keys():
            return ""
        return data['created_at']
    except urllib2.HTTPError, e:
        logging.info(name + " is not subscribed!")
        return ""
    except urllib2.URLError, e:
        logging.error("urllib2 error - check_subscriber")
        return ""

def get_subscription(name):
    name = name.lower()
    user_id = get_ids([name])[name]
    url = "https://api.twitch.tv/kraken/channels/{0}/subscriptions/{1}".format(config['twitch']['channel_id'], user_id)

    sub = {}

    try:
        req = urllib2.Request(url)
        req.add_header('Accept', 'application/vnd.twitchtv.v5+json')
        req.add_header('Client-ID', config['api']['client_id'])
        req.add_header('Authorization', 'OAuth '+config['api']['access_token'])
        response = urllib2.urlopen(req)
        data = json.load(response)

        if 'error' in data.keys():
            return sub

        sub['created'] = data['created_at']
        sub['sub_plan'] = data['sub_plan']
        sub['name'] = data['user']['display_name']

    except urllib2.HTTPError, e:
        logging.info(name + " is not subscribed!")
    except urllib2.URLError, e:
        logging.error("urllib2 error - check_subscriber")
    finally:
        return sub

def get_latest_follows(count):
    url = "https://api.twitch.tv/kraken/channels/{0}/follows?limit={1}".format(config['twitch']['channel_id'], str(int(count)))
    try:
        req = urllib2.Request(url)
        req.add_header('Accept', 'application/vnd.twitchtv.v5+json')
        req.add_header('Client-ID', config['api']['client_id'])
        response = urllib2.urlopen(req)
        userlist = json.load(response)['follows']
        users = []
        for item in userlist:
            users.append(item['user']['display_name'])
        return users
    except urllib2.URLError:
        logging.error("urllib2 error - get_latest_follows")
        return {}

def get_latest_subscribers(count, offset=0):
    return get_subscribers(count, offset)

def get_sub_count():
    url = "https://api.twitch.tv/kraken/channels/{0}/subscriptions?limit={1}&direction=desc&offset={2}".format(config['twitch']['channel_id'], 1, 0)
    try:
        req = urllib2.Request(url)
        req.add_header('Accept', 'application/vnd.twitchtv.v5+json')
        req.add_header('Client-ID', config['api']['client_id'])
        req.add_header('Authorization', 'OAuth '+ config['api']['access_token'])
        response = urllib2.urlopen(req)
        data = json.load(response)
        count = int(data['_total']) - 2
        print "Total Subscribers: " + str(count)
        return count
    except urllib2.URLError:
        logging.error("urllib2 error - get_sub_count")
        return 0

def get_sub_points():
    points = 0
    subs = get_subscribers()
    points += len(subs['1000'])
    points += len(subs['2000']) * 2
    points += len(subs['3000']) * 6
    return points


def get_subscribers(count=0, offset=0, subs={}):
    if count == 0:
        iterate = True
        limit = 100
    else:
        iterate = False
        limit = count

    url = "https://api.twitch.tv/kraken/channels/{0}/subscriptions?limit={1}&direction=desc&offset={2}".format(config['twitch']['channel_id'], limit, offset)
    print "Retrieving subs " + str(offset) + " to " + str(offset + limit)

    if offset==0:
        subs = {
            '1000':[],
            '2000':[],
            '3000':[]
        }

    try:
        req = urllib2.Request(url)
        req.add_header('Accept', 'application/vnd.twitchtv.v5+json')
        req.add_header('Client-ID', config['api']['client_id'])
        req.add_header('Authorization', 'OAuth '+ config['api']['access_token'])
        response = urllib2.urlopen(req)
        data = json.load(response)
        userlist = data['subscriptions']
        total = int(data['_total'])

        print "TOTAL: " + str(total)

        for item in userlist:
            subs[item['sub_plan']].append(item['user']['name'])
        if iterate and (offset + limit) < total:
            subs = get_subscribers(offset=offset + limit, subs=subs)

        if 'capn_flint' in subs['1000']:
            subs['1000'].remove('capn_flint')
        if 'grogbot' in subs['1000']:
            subs['1000'].remove('grogbot')
        if 'capn_flint' in subs['3000']:
            subs['3000'].remove('capn_flint')

        return subs
    except urllib2.URLError as e:
        logging.error("urllib2 error - get_subscribers: " + e.reason)
        return {}
