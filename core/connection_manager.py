import config.twitch_config as config
import socket
import re

import modules.overlay.overlay as overlay
import utils.db_utils as db
import utils.twitch_utils as twitch

class ConnectionManager():

    def __init__(self, grog, channel):
        self.grog = grog
        self.HOST = "irc.chat.twitch.tv"
        self.PORT = 6667
        self.CHAN = "#" + channel
        self.NICK = config.nickname
        self.PASS = config.stream_key
        self.conn = None
        self.running = False

# -----[ Initialization Functions ]---------------------------------------------

# -----[ Message Function ]-----------------------------------------------------

    def send_message(self, msg, priority=3, chat=True, screen=False):
        if chat:
            self._send_emote(msg)
        if screen:
            overlay.alert(priority, msg)

# -----[ Utility Functions ]----------------------------------------------------

    def subscribers(self):
        print "Checking for Subscribers!"

        subs = twitch.get_latest_subscribers(25)
        self.update_subcount()

        new = []
        if subs:
            for user in subs:
                print "Processing: " + user
                if not self.grog.charMgr.subbed(user):
                    char = self.grog.charMgr.load_character(user)
                    print "[NEW SUBSCRIBER] " + char['name']
                    overlay.alert_sub(char['name'])
                    new.append(char['name'])
                    self.grog.charMgr.give_booty(50, [user])
                    self.grog.charMgr.subbed(user, force_check=True)
        if new:
            self.grog.connMgr.send_message("Welcome new Subs and Resubs: " + ", ".join(new) +"! Have some capnBooty ! R)")
            stat = db.add_stat('sessionSubs', len(new))
            overlay.update_stat('subs', stat)

    def update_subcount(self):
        count = twitch.get_sub_count()
        db.clear_stat('subCount')
        stat = db.add_stat('subCount', int(count))
        print "stat: " + str(stat)
        overlay.update_stat('subcount', stat)


# -----[ IRC message functions ]------------------------------------------------

    def _send_pong(self, msg):
        self.con.send('PONG %s\r\n' % msg)

    def _send_message(self, msg, chan=None):
        if not chan:
            chan = self.CHAN
        print 'PRIVMSG %s :%s\r\n' % (chan, msg)
        self.con.send('PRIVMSG %s :%s\r\n' % (chan, msg))

    def _send_emote(self, msg, chan=None):
        if not chan:
            chan = self.CHAN
        emote = '\001ACTION ' + msg + '\001'
        self._send_message(emote, chan)

    def _send_names(self, chan=None):
        if not chan:
            chan = self.CHAN
        print "Sending NAMES command"
        self.con.send('NAMES %s\r\n' % chan)

    def _send_nick(self, nick):
        self.con.send('NICK %s\r\n' % nick)

    def _send_pass(self, password):
        self.con.send('PASS %s\r\n' % password)

    def _join_channel(self, chan=None):
        if not chan:
            chan = self.CHAN
        self.con.send('JOIN %s\r\n' % chan)

    def _part_channel(self, chan=None):
        if not chan:
            chan = self.CHAN
        self.con.send('PART %s\r\n' % chan)

    def _register_membership(self):
        self.con.send('CAP REQ :twitch.tv/membership\r\n')

    def _register_tags(self):
        self.con.send('CAP REQ :twitch.tv/tags\r\n')

    def _register_commands(self):
        #TODO: See if this actually works...
        self.con.send('CAP REQ :twitch.tv/commands\r\n')

    def _set_color(self):
        self._send_message('Ahoy Mateys! capnHi I heard you needed a bot! capnYarr capnHype')
        self._send_message('.color BlueViolet')

#-------------------------------------------------------------------------------

# -----[ Handle Joins/Parts/Modes ]---------------------------------------------

    def _handle_join(self, sender):
        if self.grog.charMgr.subbed(sender, force_check = True):
            char = self.grog.charMgr.load_character(sender)
            if char['ship'] > 0:
                ship = char['ship']
            else:
                ship = char['sub_count']
            overlay.ship("join", sender, ship)

    def _handle_part(self, sender):
        char = self.grog.charMgr.load_character(sender)
        if char['subscriber']:
            if char['ship'] > 0:
                ship = char['ship']
            else:
                ship = char['sub_count']
            overlay.ship("leave", sender, ship)

    def _handle_mode(self, sender):
        print sender + " is a mod!"

    def _handle_notify(self, msg):
        '''
        WhiterRice subscribed for 2 months in a row!
        '''
        data = msg.split(" ")
        if data[2] == "subscribed!" or data[1] == "subscribed":
            name = data[0]

            # This makes sure the character exists
            self.grog.charMgr.load_character(name)

            self.grog.charMgr.add_sub(name)
            if len(data) > 4:
                # this is a resub
                dur = data[3]

                self.grog.connMgr.send_message("Welcome back {0}, {1} months at sea! YARRR!!!".format(name, dur))
                self.grog.charMgr.give_booty(50, [name])
                overlay.ship("sub", name, dur)
                overlay.alert_resub(name, dur)
                overlay.update_timer(10)
            else:
                # this is a new sub
                self.grog.connMgr.send_message("Welcome to the inner circle, Pirate {0}!!!".format(name))
                self.grog.charMgr.give_booty(50, [name])
                overlay.ship("sub", name, 1)
                overlay.alert_sub(name)
                overlay.update_timer(20)
            self.update_subcount()
            stat = db.add_stat('sessionSubs', 1)
            overlay.update_stat('subs', stat)

        else:
            print "NOTIFY: " + str(data)

    def _handle_usernotice(self, tags):
        resub = self._get_resub_info(tags)
        self.grog.charMgr.load_character(resub['name'])

        self.grog.charMgr.add_sub(resub['name'])
        self.grog.connMgr.send_message("Welcome back {0}, {1} months at sea matey! YARRR!!!".format(resub['name'], resub['length']))
        self.grog.charMgr.give_booty(50, [resub['name']])
        overlay.ship("sub", resub['name'], resub['length'])
        overlay.alert_resub(resub['name'], resub['length'])
        overlay.update_timer(10)
        self.update_subcount()
        stat = db.add_stat('sessionSubs', 1)
        overlay.update_stat('subs', stat)
        pass
# ------------------------------------------------------------------------------

# -----[ IRC Utility Functions ]------------------------------------------------

    def _get_sender(self, msg):
        result = ""
        for char in msg:
            if char == "!":
                break
            if char != ":":
                result += char
        return result

    def _get_message(self, msg):
        result = ""
        i = 0
        length = len(msg)
        while i < length:
            result += msg[i] + " "
            i += 1
        result = result.lstrip(':')
        return result

    def _get_channel(self, msg):
        result = msg[3]
        return result

    def _get_tag_map(self, data):
        data = data.split(';')
        tagmap = {}
        for d in data:
            (key, val) = d.split('=')
            tagmap[key] = val;
        return tagmap

    def _get_perms(self, data):
        '''
        '@color=#5F9EA0;display-name=mr_5ka;emotes=81530:0-7,9-16,18-25;mod=0;room-id=91580306;subscriber=1;turbo=0;user-id=69442368;user-type='
        data[4] = mod
        data[6] = subscriber

        TODO: Make this more generic (search for the mod and subscriber parameters)
        '''
        tags = self._get_tag_map(data)

        perm = {}
        perm['mod'] = bool(int(tags['mod']))
        perm['sub'] = bool(int(tags['subscriber']))
        return perm

    def _get_resub_info(self, data):
        tags = self._get_tag_map(data)
        resub = {}
        if tags['msg-id'] and tags['msg-id'] == 'resub':
            resub['name'] = tags['login']
            resub['length'] = tags['msg-param-months']
            if tags['system-msg']:
                resub['message'] = tags['system-msg']
            else:
                resub['message'] = ''
        return resub

    def _get_emotes(self, data):
        '''
        '@color=#5F9EA0;display-name=mr_5ka;emotes=81530:0-7,9-16,18-25;mod=0;room-id=91580306;subscriber=1;turbo=0;user-id=69442368;user-type='
        data[3] = emotes

        link: https://static-cdn.jtvnw.net/emoticons/v1/81530/2.0

        TODO: Make this more generic (search for the mod and subscriber parameters)
        '''
        tags = self._get_tag_map(data)
        emotes = {}
        emotelist = tags['emotes']
        if emotelist:
            data = emotelist.split('/')
            for block in data:
                tmp = block.split(':')
                em_id = tmp[0]
                em_cnt = len(tmp[1].split(','))
                emotes[em_id] = em_cnt

            print emotes
        return emotes

# ------------------------------------------------------------------------------

    def connect(self):
        self.con = socket.socket()
        self.con.connect((self.HOST, self.PORT))

        self._send_pass(self.PASS)
        self._send_nick(self.NICK)
        self._join_channel(self.CHAN)
        self._register_membership()
        self._register_tags()
        self._register_commands()
        self._set_color()

        print "INFO: Connected..."

        # Check for offline subscribers
        self.subscribers()
        print "Subscriber check done!"

        data = ""

        self.running = True

        try:
            while self.running:
                try:
                    data = data + self.con.recv(1024)
                    data_split = re.split("[\r\n]+", data)
                    data = data_split.pop()

                    for line in data_split:
                        line = str.rstrip(line)
                        line = str.split(line)

                        if len(line) >= 1:
                            if line[0] == 'PING':
                                self._send_pong(line[1])


                            elif line[2] == 'USERNOTICE':
                                self._handle_usernotice(line[0])

                            elif line[1] == 'PRIVMSG':
                                sender = self._get_sender(line[0])
                                if sender == 'twitchnotify':
                                    self._handle_notify(self._get_message(line[3:]))


                            elif line[2] == 'PRIVMSG':
                                sender = self._get_sender(line[1])
                                message = self._get_message(line[4:])
                                channel = self._get_channel(line)
                                perms = self._get_perms(line[0])
                                emotes = self._get_emotes(line[0])

                                if channel == self.CHAN:
                                    if message.startswith('!'):
                                        self.grog.msgProc.parse_command(message, sender, perms)
                                    else:
                                        self.grog.msgProc.parse_message(message, sender, perms, emotes)
                                else:
                                    self.grog.msgProc.parse_raid_message(message, sender)

                            elif line[1] == 'JOIN':
                                self._handle_join(self._get_sender(line[0]))

                            elif line[1] == 'PART':
                                self._handle_part(self._get_sender(line[0]))

                            elif line[1] == 'MODE':
                                self._handle_mode(line[4])

                            else:
                                print ["!!!!!!!!!!"]+line

                except socket.error:
                    print("ERROR: Socket died")

                except socket.timeout:
                    print("ERROR: Socket timeout")
        except Exception as e:
            print "ERROR: Unhandled Error: " + str(e)
        # Clean up
        self._part_channel(self.CHAN)
