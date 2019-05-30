import logging
import MySQLdb as mdb

from config.config import config
import utils.twitch_utils as twitch


class Character():

    def __init__(self, uid, mgr):
        # Might need to load by either uid or name...
        self.charData = {}
        self.alive = True
        self.mgr = mgr
        self._load(uid)

    def __str__(self):
        return "%s is a %s" % (self.charData['name'], self.charData['rank']) #TODO: Actually make this value (rank) a thing

    def _load(self, uid):
        user = None
        if uid:
            try:
                con = mdb.connect(config['db']['host'], config['db']['user'], config['db']['pass'], config['db']['db'], use_unicode=True, charset="utf8")
                with con:
                    cur = con.cursor(mdb.cursors.DictCursor)
                    cur.execute("SELECT * from chars where user_id = %s", (uid,))
                    user = cur.fetchone()
            except mdb.Error, e:

                logging.error("DB Error %d: %s" % (e.args[0], e.args[1]))
                user = None

            finally:

                if con:
                    con.close()
            if not user:
                user = self._create(uid)
            if user:
                self.charData = user
            else:
                logging.error("Unable to load character: " + uid)
        else:
            logging.error("Invalid UID specified")

    def _save(self):
        try:
            con = mdb.connect(config['db']['host'], config['db']['user'], config['db']['pass'], config['db']['db'], use_unicode=True, charset="utf8")

            with con:
                cur = con.cursor()
                char = self.charData
                cur.execute("REPLACE INTO chars ({}) VALUES ({})".format(",".join(self.charData.keys())),\
                      (char['user_id'], char['name'], char['level'], char['exp'], char['booty'], char['access'], char['follows'], char['checked_follow'], char['subscriber'], char['sub_date'], char['sub_max'], char['sub_count'], char['sub_type'], char['ship']))
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

    def _create(self, uid):
        # create a character sheet for a new player
        name = twitch.get_user(uid)['display_name']
        # Get name for uid
        if name:
            try:
                logging.info("Creating " + name)
                char = {
                    "level":1,
                    "exp":0,
                    "booty":5,
                    "user_id":"",
                    "name":name,
                    "access":0,
                    "follows":0,
                    "checked_follow":0,
                    "subscriber":0,
                    "checked_sub":0,
                    "sub_date":"",
                    "sub_count":0,
                    "sub_max":0,
                    "sub_type":0,
                    "ship":0
                }
                return char
            except:
                logging.warning("Failed creating " + name)
                return None

        else:
            logging.error("No user found for id: " + uid)
            return None

    def level_up(self, amount, levelups):
        self.charData['exp'] = int(self.charData['exp']) + amount
        # Catch for brand new users losing exp
        if self.charData['exp'] < 0:
            self.charData['exp'] = 0

        new_level = self.mgr.compute_level(self.charData['exp'])
        if new_level > self.charData['level']:
            self.charData['level'] = new_level
            if (new_level - 1) % self.mgr.ranks_per_level == 0:
                logging.debug("level up " + self.charData['name'])
                levelups[new_level].append(self.charData['name'])

    def get_data(self, key):
        logging.debug("Retrieving value of {0} for character {1}".format(key, self.charData['name']))
        if key in self.charData.keys():
            return self.charData[key]
        else:
            logging.error("get_data: Character object does not contain key: " + key)
            return None

    def set_data(self, key, value):
        logging.debug("Setting value of {0} to {1} from character {2}".format(key, value, self.charData['name']))
        if key in self.charData.keys():
            self.charData[key] = value
            self._save()
        else:
            logging.error("set_data: Character object does not contain key: " + key)

    def save(self):
        logging.debug("Save called for character: " + self.charData['name'])
        self._save()