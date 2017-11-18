import MySQLdb as mdb

import utils.twitch_utils as twitch

from config.config import config

def fix_id(name, uid):
    print name + " : " + uid
    try:
        con = mdb.connect(config['db']['host'], config['db']['user'], config['db']['pass'], config['db']['db'])

        with con:
            cur = con.cursor()
            #cur.execute("UPDATE characters SET user_id=%s where name=%s", uid, name)
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

def remove_character(name):
    print "Deleting: " + name
    try:
        con = mdb.connect(config['db']['host'], config['db']['user'], config['db']['pass'], config['db']['db'])

        with con:
            cur = con.cursor()
            cur.execute("DELETE FROM characters where name=%s", name)
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])

    finally:
        if con:
            con.close()

def update_ids():
    names = get_names()
    while len(names) > 0:
        block = names[:50]
        names = names[50:]

        ids = twitch.get_ids(names)

        for name in ids.keys():
            fix_id(name, ids[name])
