from helper import *
import utils.twitch_utils as twitch
import time

@processes('!rank')
@processes('!level')
def command_level(self, data):
    name = data['sender']
    if check_permission(data, PERM_MOD):
        if data['args']:
            if self.charMgr.char_exists(data['args'][0]):
                name = data['args'][0]
            else:
                self.connMgr.send_message("Character " + data['args'][0] + " doesn't exist!")
                return

    try:
        self.lastRank
    except AttributeError:
        self.lastRank = 0

    now = time.time()
    print "DEBUG: elapsed = " + str(now - self.lastRank)
    if (now - self.lastRank) < 5:
        print "buffering command!!!"
        self.cmdBuffer.buffer_command(buffered_rank, name)
    else:
        print "not buffered :("
        char = self.charMgr.load_character(name)
        if char['name'] == 'Capn_Flint':
            rankstr = char['name'] + " is the Captain of course!"
        elif char['access'] > 0:
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
    for name in chars:
        char = self.charMgr.load_character(name)
        rank = self.charMgr.get_rank(char, False, False)
        if not rank in ranks.keys():
            ranks[rank] = []
        ranks[rank].append(name)
    for rank in ranks.keys():
        output += " | " + rank + " - " + ", ".join(ranks[rank])
    self.connMgr.send_message(output)
