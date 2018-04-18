import json
import logging
import re
import time
import thread
from datetime import datetime, timedelta

from collections import defaultdict
import MySQLdb as mdb

import utils.twitch_utils as twitch
import modules.overlay.overlay as overlay
from config.config import config
from config.strings import strings

from passive_exp import passive_exp

class CharacterManager():

    def __init__(self, owner):
        self.grog = owner
        self.levels = []
        self.ranks = []
        self.ranks_per_level = 5
        self.max_level = 50

        self.load_levels()
        self.load_ranks()
        self.skip_names = []

        self.grog.add_worker(passive_exp(self))


    def load_levels(self):
        try:
            l_file = open('modules/characters/levels.dat', 'r')
            lines = l_file.readlines()

            for line in lines:
                self.levels.append(int(line))

        except IOError:
            pass

    def load_ranks(self):
        try:
            r_file = open('modules/characters/ranks.dat', 'r')
            lines = r_file.readlines()
            print lines

            for line in lines:
                self.ranks.append(line.strip())
        except IOError:
            pass

# -----[ Character Storage Functions ]------------------------------------------

    def create_character(self, name, uid):
        # create a character sheet for a new player
        if name and name not in self.skip_names:
            try:
                logging.info("Creating " + name)
                char = {
                    "id":uid,
                    "level":1,
                    "exp":0,
                    "booty":5,
                    "name":name,
                    "admin":0,
                    "follower":0,
                    "checked_follow":0,
                    "subscriber":0,
                    "checked_sub":0,
                    "sub_date":"",
                    "sub_count":0,
                    "sub_max":0,
                    "sub_type":0,
                    "ship":0
                }
                self.save_character(char)
                return char
            except:
                logging.warning("Failed creating " + name)
                self.skip_names.append(name)
                return None

        else:
            return None

    def char_exists(self, name):
        user = None
        try:
            con = mdb.connect(config['db']['host'], config['db']['user'], config['db']['pass'], config['db']['db']);
            with con:
                cur = con.cursor(mdb.cursors.DictCursor)
                cur.execute("SELECT * from chars where name = %s", (name,))
                user = cur.fetchone()
        except mdb.Error, e:

            logging.error("DB Error %d: %s" % (e.args[0],e.args[1]))

        finally:

            if con:
                con.close()
        if user:
            return True
        else:
            return False

    def load_character(self, uid):
        user = None
        try:
            con = mdb.connect(config['db']['host'], config['db']['user'], config['db']['pass'], config['db']['db'], use_unicode=True, charset="utf8")
            with con:
                cur = con.cursor(mdb.cursors.DictCursor)
                cur.execute("SELECT * from chars where id = %s", (uid,))
                user = cur.fetchone()
        except mdb.Error, e:

            logging.error("DB Error %d: %s" % (e.args[0], e.args[1]))

        finally:

            if con:
                con.close()
        if not user:
            logging.debug("Couldn't load ID: " + uid)
            name = twitch.get_user(uid)['display_name']
            return self.create_character(name, uid)
        else:
            return user

    def load_char_name(self, name):
        uid = twitch.get_ids([name])[name.lower()]
        return self.load_character(uid)

    def save_character(self, char):
        try:
            con = mdb.connect(config['db']['host'], config['db']['user'], config['db']['pass'], config['db']['db'], use_unicode=True, charset="utf8")

            with con:
                cols = sorted(char.keys())
                cur = con.cursor()
                sql = "REPLACE INTO chars (" + ", ".join(cols) + ") VALUES (%(" + ")s, %(".join(cols) + ")s)"
                cur.execute(sql, char)
                con.commit()
            return 1
        except mdb.Error, e:

            if con:
                con.rollback()

            logging.error("DB Error %d: %s" % (e.args[0],e.args[1]))
            return 0

        finally:

            if con:
                con.close()

    def delete_character(self, name):
        try:
            con = mdb.connect(config['db']['host'], config['db']['user'], config['db']['pass'], config['db']['db'], use_unicode=True, charset="utf8");

            with con:
                cur = con.cursor()
                cur.execute("DELETE FROM chars WHERE name = %s", (name,))
                con.commit()
            return 1
        except mdb.Error, e:

            if con:
                con.rollback()

            logging.error("DB Error %d: %s" % (e.args[0],e.args[1]))
            return 0

        finally:

            if con:
                con.close()

# ------------------------------------------------------------------------------

# -----[ Character Utility Functions ]------------------------------------------

    def death_thread(self, name, duration):
        delay = duration * 60
        time.sleep(delay)
        self.revive_character(name)

    def kill_character(self, name, duration=0):
        logging.info("Killing " + name)
        char = self.load_char_name(name)
        if char:
            char['level'] = 0
            self.save_character(char)
            thread.start_new_thread(self.death_thread, (name, duration))

    def revive_character(self, name):
        logging.info("Reviving " + name)
        char = self.load_char_name(name)
        if char:
            if char['level'] > 0:
                return False
            char['level'] = self.compute_level(char['exp'])
            self.save_character(char)
            return True
        else:
            return False

    def is_alive(self, name):
        char = self.load_char_name(name)
        if char and char['level'] > 0:
            return True
        return False

    def compute_level(self, exp):
        level = 1
        for i in range(len(self.levels)):
            if exp > self.levels[i]:
                next
            else:
                level = i
                return level
        level = len(self.levels)
        return level

    def level_up(self, char, amount, levelups):
        char['exp'] = int(char['exp']) + amount
        if char['exp'] < 0:
            char['exp'] = 0
        new_level = self.compute_level(char['exp'])
        if new_level > char['level']:
            char['level'] = new_level
            if (new_level - 1) % self.ranks_per_level == 0:
                print "level up " + char['name']
                levelups[new_level].append(char['name'])


    def get_rank(self, char, include_rank = True, include_exp = True):
        logging.info("Getting character rank.")
        level = char['level']
        if level == 0:
            rankstr = "Corpse... capnRIP"
        else:
            rank = (level - 1) / self.ranks_per_level
            if rank >= len(self.ranks):
                rank = len(self.ranks) - 1
            print self.ranks[rank]
            rankstr = self.ranks[rank]
            if include_rank:
                rankstr += " level " + str(((level - 1) % self.ranks_per_level) + 1)
            if include_exp:
                rankstr += (" (" +str((self.levels[level] - char['exp']) + 1)
                            + " exp until next rank)")
        logging.debug("RANK: " + rankstr)
        return rankstr

    def follows_me(self, uid, force_check=False, skip_check=False):
        char = self.load_character(uid)

        if skip_check:
            return char['follower']
        if char:
            # code to check current followers for unfollows. Done monthly.
            now = int(time.time())
            if not char['follower'] and force_check:
                return twitch.check_follower(char['id'])
            elif char['follower'] and now - char['checked_follow'] > 2592000:
                if not skip_check and twitch.check_follower(char['id']):
                    char['follower'] = 1
                else:
                    char['follower'] = 0
                char['checked_follow'] = now
                self.save_character(char)
            return char['follower']
        else:
            return False


    def update_subscriber(self, char, date, sub_type=None, count=0):
        if char['name'] == "Capn_Flint":
            return
        print "UPDATING SUBSCRIBER: " + char['name']
        char['subscriber'] = 1
        char['sub_date'] = date
        if count:
            char['sub_count'] = count
        else:
            char['sub_count'] = self.guess_sub_count(date)
        if char['sub_max'] < char['sub_count']:
            char['sub_max'] = char['sub_count']
        if sub_type:
            char['sub_type'] = sub_type

    def remove_subscriber(self, char):
        char['subscriber'] = 0
        char['sub_date'] = ""
        char['sub_count'] = 0
        char['sub_type'] = 0

    def unsub_user(self, uid):
        char = self.load_character(uid)
        self.remove_subscriber(char)
        self.save_character(char)

    def sub_user(self, uid, count=0):
        char = self.load_character(uid)
        sub = twitch.get_subscription(char['name'])
        self.update_subscriber(char, sub['created'], sub['sub_plan'])
        self.save_character(char)


    def guess_sub_count(self, date):
        print "computing count"
        now = datetime.now()
        sub_date = datetime.strptime(date,"%Y-%m-%dT%H:%M:%S")
        count = 1
        while (now - sub_date) > (timedelta(days=30) * count):
            count += 1
        print "count = " + str(count)
        return count

    def add_follower(self, name):
        char = self.load_char_name(name)
        if char:
            now = int(time.time())
            char['follower'] = 1
            char['checked_follow'] = now
            self.save_character(char)


    def give_booty(self, amount, users = []):
        if not users:
            users = twitch.get_viewers()
        count = 0
        for user in users:
            count += 1
            char = self.load_char_name(user)
            if char:
                if char['level'] > 0:
                    char['booty'] += amount
                    if char['booty'] < 0:
                        char['booty'] = 0
                self.save_character(char)
        print "INFO: " + str(amount) + " Booty given to " + str(count) + " players"

    def give_exp(self, exp, users = []):
        if not users:
            users = twitch.get_viewers()
        count = 0
        amount = 0
        levelups = defaultdict(list)
        for user in users:
            count += 1
            char = self.load_char_name(user)
            if char:
                # 20% more exp for all subs!
                if char['subscriber']:
                    multi = 1
                    if char['sub_type'] == 1:
                        multi = 1.2
                    if char['sub_type'] == 2:
                        multi = 1.5
                    if char['sub_type'] == 3:
                        multi = 2
                    amount = int(exp * multi)
                else:
                    amount = exp
                if char['level'] > 0: # is_alive
                    self.level_up(char, amount, levelups)
                self.save_character(char)

        for level in levelups.keys():
            rank = (level - 1) / self.ranks_per_level
            if rank >= len(self.ranks):
                rank = len(self.ranks) - 1
            else:
                if (level - 1) % self.ranks_per_level == 0:
                    for name in levelups[level]:
                        overlay.alert_levelup(name, self.ranks[rank])
            sublevel = str(((level - 1) % self.ranks_per_level) + 1)
            self.grog.connMgr.send_message(strings['CHAR_LEVEL_UP'].format(ranktitle=self.ranks[rank] + " level " + sublevel, names=', '.join(levelups[level])))
        print "INFO: " + str(amount) + " Exp granted to " + str(count) + " players"
