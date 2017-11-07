from helper import *
import utils.db_utils as db

import urllib2
import urllib
import json
import urlparse

songrequests_on = False

#@processes("!togglesong", PERM_MOD)
def command_togglesong(self, sender, args):
    global songrequests_on
    songrequests_on = not songrequests_on
    if songrequests_on:
        self.connMgr.send_message("Song requests turned on! Type !requestsong <youtube id> to request a song!")
    else:
        self.connMgr.send_message("Song requests turned off!")

#@processes("!removesong", PERM_MOD)
def command_removesong(self, sender, args):
    if args:
        try:
            songid = int(args[0])
        except:
            songid = 0
        db.sr_remove_song(songid)
    else:
        self.connMgr.send_message("To remove a song use: !removesong <id>")

#@processes("!songrequest")
#@processes("!requestsong")
def command_requestsong(self, sender, args):
    global songrequests_on

    if songrequests_on:
        if  sender != "disco_lando":
            char = self.charMgr.load_character(sender)
            queued = db.sr_song_count(sender)
            maxreq = ((char['level'] - 1) / 5) + char['subscriber']
            if maxreq == 0:
                self.connMgr.send_message("Sorry " + sender + ", but you must be at least rank swabbie to request songs.")
            elif queued < maxreq or char['access'] > 0:
                if args:
                    songid = parse_songrequest(args[0])
                    if songid:
                        add_song(self, songid, sender)
                    else:
                        self.connMgr.send_message("Sorry " + sender + " that isn't a valid song request.")
                else:
                    self.connMgr.send_message("To send a song request, type !requestsong <youtube id>.")
            else:
                self.connMgr.send_message("Sorry " + sender + ", you have requested your maximum number of songs ("+str(maxreq)+"). Please wait for current requests to be played, then request again.")
        else:
            self.connMgr.send_message("Sorry Disco_Lando, your keys aren't here, and neither is your crappy music!")
    else:
        self.connMgr.send_message("Song requests are currently off. Sorry!")

def parse_songrequest(param):
    try:
        parsed = urlparse.urlparse(param)
        if len(parsed.path) == 11:
            return parsed.path
        elif len(parsed.path) == 12:
            return parsed.path.split('/')[-1:][0]
        else:
            v = urlparse.parse_qs(parsed.query)['v']
            return v[0]
    except:
        print "failed!"
        return None


def add_song(self, songid, requestor):
    name_url = "https://www.googleapis.com/youtube/v3/videos?key=AIzaSyCCwowZzE0uLGkTtzKfdJXo0sCw5dmZQkI&part=snippet&id={0}"
    try:
        response = urllib2.urlopen(name_url.format(songid))
        title = json.load(response)['items'][0]['snippet']['title']
        if not title:
            title = "Untitled"
        print "TITLE: " + title
        if db.sr_add_song(songid, title, requestor):
            self.connMgr.send_message(title + " added to the song queue by " + requestor)
    except:
        self.connMgr.send_message("Sorry " + requestor + " that isn't a valid song request.")
