import MySQLdb as mdb

import utils.twitch_utils as twitch

from config.config import config

def fix_id(name, uid):
    try:
        con = mdb.connect(config['db']['host'], config['db']['user'], config['db']['pass'], config['db']['db'])

        with con:
            cur = con.cursor()
            cur.execute("UPDATE chars SET user_id=%s where name=%s", (uid, name))
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
            cur.execute("SELECT name FROM chars where user_id=''")
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
            cur.execute("DELETE FROM chars where name=%s", name)
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])

    finally:
        if con:
            con.close()

def update_ids():
    count = 0
    amount = 10
    names = get_names()
    total = len(names)
    skipped = []
    for name in names:
        cname = name.lower().strip()

        print "Processing: " + cname

        ids = twitch.get_ids([cname])

        print ids

        if ids:
            count += 1
            fix_id(name, ids[cname])
        else:
            print "Skipped " + cname
            skipped.append(cname)

    print "Total fixed: " + str(count) + "/" + str(total)
    print "Skipped: " + str(skipped)
