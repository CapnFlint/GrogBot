import oauth2
import json
from config.config import config

def oauth_req(url, key, secret, http_method="GET", post_body="", http_headers=None):
    consumer = oauth2.Consumer(key=config['twitter']['consumer_key'], secret=config['twitter']['consumer_secret'])
    token = oauth2.Token(key=key, secret=secret)
    client = oauth2.Client(consumer, token)
    resp, content = client.request( url, method=http_method, body=post_body, headers=http_headers )
    return content

def get_latest_mentions(count):
    mentions_timeline = oauth_req( 'https://api.twitter.com/1.1/statuses/mentions_timeline.json?include_entities=false&count=' + str(count), config['twitter']['api_key'], config['twitter']['api_secret'] )
    mentions = json.loads(mentions_timeline)
    result = []
    for mention in mentions:
        m = {}
        m['id'] = mention['id']
        m['user'] = mention['user']['screen_name']
        m['name'] = mention['user']['name']
        m['image'] = mention['user']['profile_image_url']
        m['text'] = mention['text']
        result.append(m)
    return result

def get_latest_retweets(count):
    mentions_timeline = oauth_req( 'https://api.twitter.com/1.1/statuses/retweets_of_me.json?include_entities=false&count=' + str(count), config['twitter']['api_key'], config['twitter']['api_secret'] )
    mentions = json.loads(mentions_timeline)
    result = []
    for mention in mentions:
        m = {}
        m['id'] = mention['id']
        m['user'] = mention['user']['screen_name']
        m['name'] = mention['user']['name']
        m['image'] = mention['user']['profile_image_url']
        result.append(m)
    return result

def get_latest_tweet(name=config['twitter']['handle']):
    user_timeline = oauth_req( 'https://api.twitter.com/1.1/statuses/user_timeline.json?include_entities=false&include_rts=false&exclude_replies=true&screen_name=' + name + '&count=1', config['twitter']['api_key'], config['twitter']['api_secret'] )
    tweets = json.loads(user_timeline)
    result = ""
    for tweet in tweets:
        result = "https://twitter.com/{0}/status/{1}".format(name, str(tweet['id']))
    return result
