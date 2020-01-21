import urllib2
import urllib
import json
import logging

from config.config import config

def get_ids(names):
    # names is a list of names ['foo','bar','baz']
    url = "https://api.twitch.tv/kraken/users?login=" + ','.join(names)
    try:
        req = urllib2.Request(url)
        req.add_header('Accept', 'application/vnd.twitchtv.v5+json')
        req.add_header('Client-ID', config['api']['client_id'])
        response = urllib2.urlopen(req)
        data = json.load(response)
        if 'error' in data.keys():
            return {}
        results = {}
        for user in data["users"]:
            results[user['name'].encode('ascii')] = user['_id'].encode('ascii')
        return results
    except urllib2.URLError as e:
        logging.error("urllib2 error - get_ids: " + str(e))
        return None
    except Exception as e:
        logging.error("Something else went wrong :( - " + str(e))

def get_viewers(include_mods = True):
    url = "http://tmi.twitch.tv/group/user/{0}/chatters?client_id={1}".format(config['twitch']['channel'].lower(), config['api']['client_id'])
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
    url = "http://tmi.twitch.tv/group/user/{0}/chatters?client_id={1}".format(config['twitch']['channel'].lower(), config['api']['client_id'])
    try:
        response = urllib2.urlopen(url)
        userlist = json.load(response)['chatters']
        users = userlist['moderators']
        return users
    except urllib2.URLError:
        logging.error("get_mods: urllib2 error")
        return {}

def is_mod(uid):
    #TODO: Bad request? Fix it!
    url = "https://api.twitch.tv/kraken/users/{0}/chat/channels/{1}?api_version=5".format(uid, config['twitch']['channel_id'])
    mod = False
    try:
        req = urllib2.Request(url)
        req.add_header('Accept', 'application/vnd.twitchtv.v5+json')
        req.add_header('Client-ID', config['api']['client_id'])
        response = urllib2.urlopen(req)
        data = json.load(response)
        if 'error' in data.keys():
            return mod
        if data['badges']:
            for badge in data['badges']:
                if badge['id'] == "moderator":
                    mod = True
        return mod
    except urllib2.URLError as e:
        logging.error("urllib2 error - is_mod: " + e.reason)
    finally:
        return mod

def get_user(uid):
    url = "https://api.twitch.tv/kraken/users/{0}".format(uid)
    try:
        req = urllib2.Request(url)
        req.add_header('Accept', 'application/vnd.twitchtv.v5+json')
        req.add_header('Client-ID', config['api']['client_id'])
        response = urllib2.urlopen(req)
        data = json.load(response)
        if 'error' in data.keys():
            return {}
        return data
    except urllib2.URLError:
        logging.error("get_user: urllib2 error")
        return {}

def get_game(name):
    name = name.lower()
    if name == "capn_flint":
        channel_id = config['twitch']['channel_id']
    else:
        channel_id = get_ids([name])[name.lower()]
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
    channel_id = get_ids([name])[name.lower()]
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

def check_follower(user_id):
    url = "https://api.twitch.tv/kraken/users/{0}/follows/channels/{1}".format(user_id, config['twitch']['channel_id'])
    if user_id == config['twitch']['channel_id']:
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
    user_id = get_ids([name])[name.lower()]
    url = "https://api.twitch.tv/kraken/channels/{0}/subscriptions/{1}".format(config['twitch']['channel_id'], user_id)

    try:
        req = urllib2.Request(url)
        req.add_header('Accept', 'application/vnd.twitchtv.v5+json')
        req.add_header('Client-ID', config['api']['client_id'])
        req.add_header('Authorization', 'OAuth '+config['api']['access_token'])
        response = urllib2.urlopen(req)
        data = json.load(response)
        if 'error' in data.keys():
            return ""
        return data['created_at']
    except urllib2.HTTPError, e:
        logging.info(name + " is not subscribed!")
        return ""
    except urllib2.URLError, e:
        logging.error("urllib2 error - check_subscriber")
        return ""

def get_subscription(user_id):
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
        logging.error("urllib2 error - get_subscription")
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
            users.append(item['user']['display_name'].rstrip().replace(" ", "")) 
        return users
    except urllib2.URLError:
        logging.error("urllib2 error - get_latest_follows")
        return {}

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
        logging.info("Total Subscribers: " + str(count))
        return count
    except urllib2.URLError:
        logging.error("urllib2 error - get_sub_count")
        return 0

def get_sub_points(subs={}):
    points = 0
    if not subs:
        subs = get_subscribers()
    print subs
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
    logging.debug("Retrieving subs " + str(offset) + " to " + str(offset + limit))

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

        logging.info("TOTAL: " + str(total))

        for item in userlist:
            subs[item['sub_plan']].append(item['user']['_id'])
        if iterate and (offset + limit) < total:
            subs = get_subscribers(offset=offset + limit, subs=subs)

        # grogbot = 91953864, Capn_Flint = 91580306
        if '91580306' in subs['1000']:
            subs['1000'].remove('91580306')
        if '91953864' in subs['1000']:
            subs['1000'].remove('91953864')
        if '91580306' in subs['3000']:
            subs['3000'].remove('91580306')

        return subs
    except urllib2.URLError as e:
        logging.error("urllib2 error - get_subscribers: " + e.reason)
        return {}

def get_emotes():
    # Get a list of my current emotes for the raid game!
    channel_id = config['twitch']['channel_id']
    url = "https://api.twitchemotes.com/api/v4/channels/" + channel_id

    logging.info("Getting list of current Emotes...")
    try:
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        data = json.load(response)
        emotes = []
        for emote in data['emotes']:
            emotes.append(str(emote['id']))
        return emotes
        logging.debug("Emotes retrieved: " + ", ".join(emotes))
    except urllib2.URLError as e:
        logging.error("urllib2 error - get_emotes: " + e.reason)
        return []
    except:
        logging.error("Cannot retrieve emotes...")
        return []
