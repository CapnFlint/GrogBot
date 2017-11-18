import MySQLdb as mdb

import utils.twitch_utils as twitch

from config.config import config

def fix_name(name, uid):
    try:
        con = mdb.connect(config['db']['host'], config['db']['user'], config['db']['pass'], config['db']['db'])

        with con:
            cur = con.cursor()
            cur.execute("UPDATE characters SET user_id=%s where name=%s", uid, name)
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])

    finally:
        if con:
            con.close()

def get_names():
    names = []

    try:
        con = mdb.connect(config['db']['host'], config['db']['user'], config['db']['pass'], config['db']['db'])

        with con:
            cur = con.cursor(mdb.cursors.DictCursor)
            cur.execute("SELECT name FROM characters where user_id=''")
            rows = cur.fetchall()

            for row in rows:
                names.append(row['name'])

    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])

    finally:
        if con:
            con.close()
        return names

def update_ids():
    names = get_names()
    print names
