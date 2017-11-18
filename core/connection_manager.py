import logging
import socket
import re
import thread

from config.config import config
from config.strings import strings

import modules.overlay.overlay as overlay
import utils.db_utils as db
import utils.twitch_utils as twitch

class ConnectionManager():

    def __init__(self, grog, channel):
        self.grog = grog
        self.HOST = "irc.chat.twitch.tv"
        self.PORT = 6667
        self.CHAN = "#" + channel
        self.sock = None
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
        logging.info("Checking for Subscribers!")

        subs = twitch.get_latest_subscribers(100)
        sublist = subs['1000'] + subs['2000'] + subs['3000']

        print sublist
        self.update_subcount()

        new_subs = []
        if sublist:
            for user in sublist:
                logging.debug("Processing: " + user)
                if not self.grog.charMgr.subbed(user):
                    char = self.grog.charMgr.load_character(user)
                    logging.info("[NEW SUBSCRIBER] " + char['name'])
                    overlay.alert_sub(char['name'])
                    new_subs.append(char['name'])
                    self.grog.charMgr.give_booty(50, [user])
                    self.grog.charMgr.subbed(user, force_check=True)
        if new_subs:
            self.grog.connMgr.send_message(strings['SUB_WELCOME'].format(names=", ".join(new_subs)))
            stat = db.add_stat('sessionSubs', len(new_subs))
            overlay.update_stat('subs', stat)
        logging.info("Subscriber check done!")

    def update_subcount(self):
        count = twitch.get_sub_points()
        db.clear_stat('subCount')
        stat = db.add_stat('subCount', int(count))
        logging.debug("New SubCount: " + str(stat))
        overlay.update_stat('subcount', stat)


# -----[ IRC message functions ]------------------------------------------------

    def _connect(self):
        self.sock = socket.socket()
        self.sock.connect((config['irc']['HOST'], config['irc']['PORT']))
        self.sock.send('PASS %s\r\n' % config['irc']['PASS'])
        self.sock.send('NICK %s\r\n' % config['irc']['NICK'])
        self.sock.send('JOIN %s\r\n' % self.CHAN)

        logging.info("Connected!")

    def _request_capabilities(self):
        # Request capabilities
        self.sock.send('CAP REQ :twitch.tv/membership\r\n')
        self.sock.send('CAP REQ :twitch.tv/tags\r\n')
        self.sock.send('CAP REQ :twitch.tv/commands\r\n')

    def _send_pong(self, msg):
        self.sock.send('PONG %s\r\n' % msg)

    def _send_message(self, msg, chan=None):
        if not chan:
            chan = self.CHAN
        logging.debug('PRIVMSG %s :%s\r\n' % (chan, msg))
        self.sock.send('PRIVMSG %s :%s\r\n' % (chan, msg))

    def _send_emote(self, msg, chan=None):
        if not chan:
            chan = self.CHAN
        emote = '\001ACTION ' + msg + '\001'
        self._send_message(emote, chan)

    def _send_names(self, chan=None):
        if not chan:
            chan = self.CHAN
        logging.info("Sending NAMES command")
        self.sock.send('NAMES %s\r\n' % chan)

    def _part_channel(self, chan=None):
        if not chan:
            chan = self.CHAN
        self.sock.send('PART %s\r\n' % chan)

    def _set_color(self):
        #self._send_message('Ahoy Mateys! capnHi I heard you needed a bot! capnYarr capnHype')
        self._send_message('.color BlueViolet')

#-------------------------------------------------------------------------------

# -----[ Handle Joins/Parts/Modes ]---------------------------------------------

    def _handle_join(self, user):
        char = self.grog.charMgr.load_character(user)
        if char['subscriber']:
            if char['ship'] > 0:
                ship = char['ship']
            else:
                ship = char['sub_count']
            overlay.ship("join", user, ship)

    def _handle_part(self, user):
        char = self.grog.charMgr.load_character(user)
        if char['subscriber']:
            if char['ship'] > 0:
                ship = char['ship']
            else:
                ship = char['sub_count']
            overlay.ship("leave", user, ship)

    def _handle_mode(self, user):
        logging.debug(user + " is a mod!")

    def _handle_notify(self, msg):
        pass

    def _handle_usernotice(self, msg):
        '''
        @badges=<badges>;color=<color>;display-name=<display-name>;emotes=<emotes>;id=<id-of-msg>;login=<user>;mod=<mod>;msg-id=<msg-id>;room-id=<room-id>;subscriber=<subscriber>;system-msg=<system-msg>;tmi-sent-ts=<timestamp>;turbo=<turbo>;user-id=<user-id>;user-type=<user-type> :tmi.twitch.tv USERNOTICE #<channel> :<message>
        '''
        print "USERNOTICE!!!"
        if msg['tags']['msg-id'] == 'ritual':
            # A "Ritual" message, like new person's first message.
            pass
        elif msg['tags']['msg-id'] == 'raid': # A raid
            pass
        elif msg['tags']['msg-id'] in ['sub','resub']: #Subscription
            ''' Chilly613 gifted a $4.99 sub to Sgt_Cracker! '''
            logging.debug("SUB/RESUB Usernotice!")
            sysmsg = msg['tags']['system-msg'].split()
            if sysmsg[1] == 'gifted': # Gift Sub!
                sender = sysmsg[0]
                name = sysmsg[6]
                sub_type = msg['tags']['msg-param-sub-plan']
                count = msg['tags']['msg-param-months']
                self.grog.charMgr.add_sub(name, sub_type, 0, count)

                if msg['tags']['msg-id'] == "sub":
                    self.grog.connMgr.send_message("Welcome to the inner circle, Pirate {0}!!!".format(name))
                    if sub_type in ["1000","Prime"]:
                        overlay.update_timer(10)
                    elif sub_type == "2000":
                        overlay.update_timer(20)
                    elif sub_type == "3000":
                        overlay.update_timer(50)
                else:
                    self.grog.connMgr.send_message("Welcome back {0}, {1} months at sea! YARRR!!!".format(name, count))
                    if sub_type in ["1000","Prime"]:
                        overlay.update_timer(5)
                    elif sub_type == "2000":
                        overlay.update_timer(10)
                    elif sub_type == "3000":
                        overlay.update_timer(25)

                self.grog.charMgr.give_booty(50, [name,sender])
                overlay.ship("sub", name, count)
                overlay.alert_sub(name, sub_type, count, msg['tags']['msg-id'], msg['text'])
                self.update_subcount()
        pass
# ------------------------------------------------------------------------------

# -----[ IRC Utility Functions ]------------------------------------------------

    def _parse_message(self, message):
        msg = {}

        msg["sender"] = re.match(':(.*)!', message[1]).group(1).encode('utf-8')
        msg["text"] = " ".join(message[4:]).lstrip(":")
        msg['channel'] = message[3]
        msg['tags'] = self._get_tags(message[0])
        msg['emotes'] = self._get_emotes(msg['tags'])
        msg['perms'] = self._get_perms(msg['tags'])

        if msg['sender'] == 'capn_flint':
            msg['perms']['mod'] = True

        return msg

    def _get_sender(self, msg):
        result = ""
        for char in msg:
            if char == "!":
                break
            if char != ":":
                result += char
        result = result.encode('utf-8')
        return result

    def _get_tags(self, data):
        data = data.split(';')
        tagmap = {}
        for d in data:
            (key, val) = d.split('=')
            tagmap[key] = val;
        return tagmap

    def _get_perms(self, tags):
        '''
        '@color=#5F9EA0;display-name=mr_5ka;emotes=81530:0-7,9-16,18-25;mod=0;room-id=91580306;subscriber=1;turbo=0;user-id=69442368;user-type='
        '''

        perm = {}
        perm['mod'] = bool(int(tags['mod']))
        perm['sub'] = bool(int(tags['subscriber']))

        return perm

    def _get_emotes(self, tags):
        '''
        '@color=#5F9EA0;display-name=mr_5ka;emotes=81530:0-7,9-16,18-25;mod=0;room-id=91580306;subscriber=1;turbo=0;user-id=69442368;user-type='
        data[3] = emotes

        link: https://static-cdn.jtvnw.net/emoticons/v1/81530/2.0

        TODO: Make this more generic (search for the mod and subscriber parameters)
        '''

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
        self._connect()
        self._request_capabilities()

        self._set_color()

        logging.info("Connected...")

        #logging.debug("Sub Points: " + str(twitch.get_sub_points()))

        # Check for offline subscribers
        #thread.start_new_thread(self.subscribers, ())

        data = ""

        self.running = True

        try:
            while self.running:
                try:
                    data = data + self.sock.recv(1024)
                    data_split = re.split("[\r\n]+", data)
                    data = data_split.pop()

                    for line in data_split:
                        line = str.rstrip(line)
                        line = str.split(line)

                        if len(line) >= 1:
                            if line[0] == 'PING':
                                self._send_pong(line[1])

                            elif line[2] == 'PRIVMSG':
                                msg = self._parse_message(line)

                                if msg['emotes']:
                                    emoteList = []
                                    for emote in msg['emotes'].keys():
                                        for i in range(msg['emotes'][emote]):
                                            emoteList.append(emote)

                                    overlay.send_emotes(msg['sender'], emoteList)

                                if False and msg['channel'] == self.CHAN:
                                    if msg['text'].startswith('!'):
                                        self.grog.msgProc.parse_command(msg)
                                    else:
                                        self.grog.msgProc.parse_message(msg)
                                else:
                                    pass
                                    #self.grog.msgProc.parse_raid_message(message, msg['sender'])

                            elif line[2] == 'USERNOTICE':
                                print "USERNOTICE: " + " ".join(line)

                            elif line[1] == 'JOIN':
                                self._handle_join(self._get_sender(line[0]))

                            elif line[1] == 'PART':
                                self._handle_part(self._get_sender(line[0]))

                            elif line[1] == 'MODE':
                                self._handle_mode(line[4])

                            else:
                                logging.warning(" ".join(["Unhandled:"]+line))

                except socket.error:
                    logging.error("Socket died")

                except socket.timeout:
                    logging.error("Socket timeout")
        except Exception as e:
            logging.error("Unhandled Error: " + str(e))
        # Clean up
        self._part_channel(self.CHAN)
