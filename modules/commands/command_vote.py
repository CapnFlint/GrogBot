import thread
import time

from helper import *

#@processes('!runvote', PERM_MOD)
def command_runvote(self, sender, args):
    self.vote_entries = defaultdict(list)
    self.vote_options = args[:6]
    vote_len = 120
    if len(self.vote_options) > 1:
        self.connMgr.send_message('A vote has started!')

        def command_vote(self, sender, args):
            if check_permission(sender, PERM_NONE):
                register_vote(self, sender, args)

        self.add_command('!vote', command_vote)
        option_text = "Your choices are:"
        for option in self.vote_options:
            option_text += " " + option + ","

        option_text = option_text.rstrip(', ')
        self.connMgr.send_message(option_text)
        self.connMgr.send_message('To vote type "!vote option". You have ' + str(vote_len) + 's, so get voting!')

        def vote_thread(self, countdown):
            time.sleep(countdown)
            self.remove_command('!vote')
            self.connMgr.send_message('Vote has ended!')
            winner = get_top_vote(self)
            percent = get_vote_percent(self,winner)
            self.connMgr.send_message('And the winner is... ' + winner + ' with ' + str(percent) + '% of the vote!')
            pass
        thread.start_new_thread(vote_thread, (self, vote_len,))
    else:
        self.connMgr.send_message("To run a vote type: !runvote <options list>")

def register_vote(self, user, args):
    choice = args[0]
    if choice in self.vote_options:
        if user not in self.vote_entries[choice]:
            self.vote_entries[choice].append(user)

def get_top_vote(self):
    top = ''
    topCount = 0
    print self.vote_entries
    if self.vote_entries:
        for key in self.vote_entries.keys():
            if not top:
                print "Top set to: " + key + "(" + str(len(self.vote_entries[key])) + ")"
                top = key
                topCount = len(self.vote_entries[key])
            else:
                print str(len(self.vote_entries[key])) + "::" + str(topCount)
                if len(self.vote_entries[key]) > topCount:
                    print "Top set to: " + key + "(" + str(len(self.vote_entries[key])) + ")"
                    top = key
                    topCount = len(self.vote_entries[key])
        return top
    else:
        return None

def get_vote_percent(self, option):
    option_count = 0.0
    total_count = 0.0
    for key in self.vote_entries:
        if key == option:
            option_count = float(len(self.vote_entries[key]))
        total_count += len(self.vote_entries[key])

    print str(total_count) + " total votes"
    print str(option_count) + " votes for winner"
    percent = (option_count / total_count) * 100
    print "winning percentage: " + str(percent) + "%"
    return int(percent)
