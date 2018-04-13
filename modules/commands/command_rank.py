from helper import *
import utils.twitch_utils as twitch
import time

@processes('!rank')
@processes('!level')
def command_level(self, data):

    try:
        self.lastRank
    except AttributeError:
        self.lastRank = 0

    now = time.time()

    if (now - self.lastRank) < 5:
        print "buffering command!!!"
        self.cmdBuffer.buffer_command(buffered_rank, data['sender_id'])
    else:
        print "not buffered :("
        char = self.charMgr.load_character(data['sender_id'])
        if char['name'] == 'Capn_Flint':
            rankstr = char['name'] + " is the Captain of course!"
        elif data['perms']['mod']:
            rankstr = char['name'] + " is an officer of the good ship Narwhal!"
        elif char['level'] > 50:
            rankstr = char['name'] + " is the Scourge of the Seven Seas! R) YARRR!!! R)"
        else:
            rankstr = char['name'] + " is a " + self.charMgr.get_rank(char)
        self.connMgr.send_message(rankstr)
    self.lastRank = now

def buffered_rank(self, chars):
    ranks = {}
    output = "Ranks"
    for uid in chars:
        char = self.charMgr.load_character(uid)
        rank = self.charMgr.get_rank(char, False, False)
        if not rank in ranks.keys():
            ranks[rank] = []
        ranks[rank].append(char['name'])
    for rank in ranks.keys():
        output += " | " + rank + " - " + ", ".join(ranks[rank])
    self.connMgr.send_message(output)
