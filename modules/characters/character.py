import logging
import MySQLdb as mdb

from config.config import config


class Character():

    def __init__(self, name):
        self.charData = {}
        self.alive = True
        self._load_character(name)

    def _load_character(name):
        user = None
        if name:
            try:
                con = mdb.connect(config['db']['host'], config['db']['user'], config['db']['pass'], config['db']['db'], use_unicode=True, charset="utf8");
                with con:
                    cur = con.cursor(mdb.cursors.DictCursor)
                    cur.execute("SELECT * from chars where name = %s", (name,))
                    user = cur.fetchone()
            except mdb.Error, e:

                logging.error("DB Error %d: %s" % (e.args[0], e.args[1]))

            finally:

                if con:
                    con.close()
            if not user:
                user = self._create_character(name)
            self.charData = user
        else:
            logging.error("Unable to load character - " + name)

    def _save_character(name):
        try:
            con = mdb.connect(config['db']['host'], config['db']['user'], config['db']['pass'], config['db']['db'], use_unicode=True, charset="utf8");

            with con:
                cur = con.cursor()
                cur.execute("REPLACE INTO chars ({}) VALUES ({})".format(",".join(self.charData.keys())),\
                      (char['user_id'], char['name'], char['level'], char['exp'], char['booty'], char['access'], char['follows'], char['checked_follow'], char['subscriber'], char['sub_date'], char['sub_max'], char['sub_count'], char['sub_type'], char['ship']))
                con.commit()
            return 1
        except mdb.Error, e:

            if con:
                con.rollback()

            logging("DB Error %d: %s" % (e.args[0],e.args[1]))
            return 0

        finally:

            if con:
                con.close()

    def _create_character(self, name):
        # create a character sheet for a new player
        #name = utils.get_display_name(name)
        if name and name not in self.skip_names:
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
                self.save_character(char)
                return char
            except:
                logging.warning("Failed creating " + name)
                self.skip_names.append(name)
                return None

        else:
            return None



    def get_data(self, data):
        if data in self.charData.keys():
            return self.charData(data)
        else:
            logging.error("get_data: Character object does not contain data: " + data)
            return None

    def set_data(self, data, value):
        if data in self.charData.keys():
            self.charData(data) = value
        else:
            logging.error("set_data: Character object does not contain data: " + data)
