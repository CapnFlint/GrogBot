import MySQLdb as mdb
import datetime
import random
import time
import logging

from config.config import config

def is_admin(uid):
    admin = 0
    char = None
    con = None
    try:
        con = mdb.connect(config['db']['host'], config['db']['user'], config['db']['pass'], config['db']['db'])


        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("SELECT admin from chars where id = %s", (uid,))
        char = cur.fetchone()

    except mdb.Error, e:
        logging.error("Error %d: %s" % (e.args[0],e.args[1]))
        return 0

    finally:
        if con:
            con.close()

    if char:
        admin = char['admin']

    return admin

def add_message(message):
    now = int(time.time())
    try:
        con = mdb.connect(config['db']['host'], config['db']['user'], config['db']['pass'], config['db']['db'])

        cur = con.cursor()
        cur.execute("INSERT INTO messages (added, priority, type, message) VALUES (%s, %s, %s, %s)", (now, message['priority'], message['type'], message['message']))
        con.commit()

    except mdb.Error, e:
        logging.error("Error %d: %s" % (e.args[0],e.args[1]))
        return 0

    finally:
        if con:
            con.close()

def clear_messages():
    try:
        con = mdb.connect(config['db']['host'], config['db']['user'], config['db']['pass'], config['db']['db'])

        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("DELETE FROM messages")
        con.commit()

    except mdb.Error, e:
        logging.error("Error %d: %s" % (e.args[0],e.args[1]))
        return 0

    finally:
        if con:
            con.close()

def clear_stats():
    try:
        con = mdb.connect(config['db']['host'], config['db']['user'], config['db']['pass'], config['db']['db'])

        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("UPDATE stats SET value=0 where stat like 'session%'")
        con.commit()

    except mdb.Error, e:
        logging.error("Error %d: %s" % (e.args[0],e.args[1]))
        return 0

    finally:
        if con:
            con.close()

def clear_stat(name):
    logging.debug('clearing state: ' + name)
    try:
        con = mdb.connect(config['db']['host'], config['db']['user'], config['db']['pass'], config['db']['db'])

        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("UPDATE stats SET value=0 where stat=%s",(name,))
        con.commit()

    except mdb.Error, e:
        logging.error("Error %d: %s" % (e.args[0],e.args[1]))
        return 0

    finally:
        if con:
            con.close()

def add_stat(name, amount):
    logging.debug('adding stat: ' + name + "(" + str(amount) + ")")
    try:
        con = mdb.connect(config['db']['host'], config['db']['user'], config['db']['pass'], config['db']['db'])
        value = 0

        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("SELECT value from stats where stat = %s", (name,))
        stat = cur.fetchone()


        if stat:
            value = int(stat['value']) + int(amount)
            count = cur.execute("UPDATE stats SET value = %s WHERE stat = %s", (value, name))
            con.commit()

    except mdb.Error, e:
        logging.error("Error %d: %s" % (e.args[0],e.args[1]))
        return 0

    finally:
        if con:
            con.close()
    return value


def get_stat(name):
    value = 0
    try:
        con = mdb.connect(config['db']['host'], config['db']['user'], config['db']['pass'], config['db']['db'])

        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("SELECT value from stats where stat = %s", (name,))
        stat = cur.fetchone()
        value = int(stat['value'])

    except mdb.Error, e:
        logging.error("Error %d: %s" % (e.args[0],e.args[1]))
        return 0

    finally:
        if con:
            con.close()
    return value

def get_custom_commands():
    commands = {}
    try:
        con = mdb.connect(config['db']['host'], config['db']['user'], config['db']['pass'], config['db']['db'])

        cur = con.cursor(mdb.cursors.DictCursor)

        cur.execute("SELECT * from custom_command where custom=1")
        rows = cur.fetchall()

    except mdb.Error, e:
        logging.error("Error %d: %s" % (e.args[0],e.args[1]))
        return 0

    finally:
        if con:
            con.close()

    if rows:
        for row in rows:
            commands[row['command']] = row['message']

    return commands

def del_custom_command(command):
    try:
        logging.debug("deleting custom command: " + command)
        con = mdb.connect(config['db']['host'], config['db']['user'], config['db']['pass'], config['db']['db'])

        cur = con.cursor()
        cur.execute("DELETE from custom_command WHERE command = %s", (command,))

        con.commit()

    except mdb.Error, e:
        logging.error("Error %d: %s" % (e.args[0],e.args[1]))
        return 0

    finally:
        if con:
            con.close()


def add_custom_command(command, message):
    try:
        logging.debug("adding custom command: " + command)
        con = mdb.connect(config['db']['host'], config['db']['user'], config['db']['pass'], config['db']['db'])

        cur = con.cursor()
        cur.execute("REPLACE INTO custom_command (command, message) VALUES (%s, %s)", (command, message))

        con.commit()

    except mdb.Error, e:
        logging.error("Error %d: %s" % (e.args[0],e.args[1]))
        return 0

    finally:
        if con:
            con.close()


def random_sub():
    commands = {}
    try:
        con = mdb.connect(config['db']['host'], config['db']['user'], config['db']['pass'], config['db']['db'])

        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("SELECT name FROM chars WHERE subscriber = 1 ORDER BY rand() limit 1")
        char = cur.fetchone()

    except mdb.Error, e:
        logging.error("Error %d: %s" % (e.args[0],e.args[1]))
        return 0

    finally:
        if con:
            con.close()

    return char['name']

def get_subscribers():
    subs = []
    try:
        con = mdb.connect(config['db']['host'], config['db']['user'], config['db']['pass'], config['db']['db'])

        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("SELECT id FROM chars WHERE subscriber = 1")
        result = cur.fetchall()

        for row in result:
            subs.append(row['id'])

    except mdb.Error, e:
        logging.error("Error %d: %s" % (e.args[0],e.args[1]))
        subs = []

    finally:
        if con:
            con.close()

    return subs


def stats_add_death(game):
    logging.info("adding death")

    con = None
    try:
        con = mdb.connect(config['db']['host'], config['db']['user'], config['db']['pass'], config['db']['db'])

        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("SELECT * from deaths where game = %s", (game,))

        stat = cur.fetchone()

        if stat:
            score = int(stat['count']) + 1
            cur.execute("UPDATE deaths SET count = %s WHERE game = %s", (score, game))
            con.commit()
        else:
            cur.execute("INSERT INTO deaths (game, count) VALUES (%s, %s)", (game, 1))
            con.commit()
        

    except mdb.Error, e:
        logging.error("Error %d: %s" % (e.args[0],e.args[1]))
        return 0

    finally:
        if con:
            con.close()

def stats_remove_death(game):
    logging.info("removing death")

    con = None
    try:
        con = mdb.connect(config['db']['host'], config['db']['user'], config['db']['pass'], config['db']['db'])

        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("SELECT * from deaths where game = %s", (game,))
        stat = cur.fetchone()

        if stat:
            score = int(stat['count']) - 1
            if score < 0:
                score = 0
            cur.execute("UPDATE deaths SET count = %s WHERE game = %s", (score, game))
            con.commit()

    except mdb.Error, e:
        logging.error("Error %d: %s" % (e.args[0],e.args[1]))
        return 0

    finally:
        if con:
            con.close()

def sr_add_song(songid, songname, requestor):
    ret = False
    try:
        con = mdb.connect(config['db']['host'], config['db']['user'], config['db']['pass'], config['db']['db'])

        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("INSERT INTO songrequests (songid, songname, requestor) VALUES (%s, %s, %s)", (songid, songname, requestor))
        con.commit()
        ret = True

    except mdb.Error, e:
        logging.error("Error %d: %s" % (e.args[0],e.args[1]))
        ret = False

    finally:
        if con:
            con.close()

    return ret

def sr_remove_song(songid):
    ret = False
    try:
        con = mdb.connect(config['db']['host'], config['db']['user'], config['db']['pass'], config['db']['db'])

        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("DELETE FROM songrequests WHERE id = %s", (songid,))
        con.commit()
        ret = True

    except mdb.Error, e:
        logging.error("Error %d: %s" % (e.args[0],e.args[1]))
        ret = False

    finally:
        if con:
            con.close()

    return ret

def sr_song_count(user):
    count = 0
    try:
        con = mdb.connect(config['db']['host'], config['db']['user'], config['db']['pass'], config['db']['db'])

        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("SELECT count(*) as count from songrequests where requestor = %s", (user,))
        char = cur.fetchone()

        if char:
            count = int(char['count'])
        else:
            count = 0

    except mdb.Error, e:
        logging.error("Error %d: %s" % (e.args[0],e.args[1]))
        count = 0

    finally:
        if con:
            con.close()

    return count

def qu_add_quote(quote, name, game):

    date = datetime.date.today()

    try:
        con = mdb.connect(config['db']['host'], config['db']['user'], config['db']['pass'], config['db']['db'])
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("INSERT INTO quotes (quote, date, name, game) VALUES (%s, %s, %s, %s)", (quote, date, name, game))
        con.commit()

    except mdb.Error, e:
        logging.error("Error %d: %s" % (e.args[0],e.args[1]))

    finally:
        if con:
            con.close()

def qu_get_quote():
    logging.info("Getting random quote")
    quote = []
    con = None
    try:
        con = mdb.connect(config['db']['host'], config['db']['user'], config['db']['pass'], config['db']['db']);

        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("SELECT count(id) as count from quotes")
        count = cur.fetchone()['count']

        pick = random.choice(range(count))+1
        cur.execute("SELECT * from quotes where id = %s", (pick,))
        quote = cur.fetchone()

    except mdb.Error, e:
        logging.error("Error %d: %s" % (e.args[0],e.args[1]))

    finally:
        if con:
            con.close()

    return quote

def qu_get_quote_id(quid):
    logging.info("Getting quote by id " + str(quid))
    quote = []
    con = None
    try:
        con = mdb.connect(config['db']['host'], config['db']['user'], config['db']['pass'], config['db']['db'])

        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("SELECT * from quotes where id = %s", (quid,))
        quote = cur.fetchone()

    except mdb.Error, e:
        logging.error("Error %d: %s" % (e.args[0],e.args[1]))

    finally:
        if con:
            con.close()

    return quote

def mq_add_message(mtype, priority, message, sound):
    now = int(time.time())
    ret = False
    con = None
    try:
        con = mdb.connect(config['db']['host'], config['db']['user'], config['db']['pass'], config['db']['db'])

        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("INSERT INTO messages (added, priority, type, message, sound) VALUES (%s, %s, %s, %s, %s)", (now, priority, mtype, message, sound))
        con.commit()

    except mdb.Error, e:
        logging.error("Error %d: %s" % (e.args[0],e.args[1]))
        ret = False

    finally:
        if con:
            con.close()

    return ret

def getEvent():
    event = None
    try:
        con = mdb.connect(config['db']['host'], config['db']['user'], config['db']['pass'], "events")

        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("select * from event_events where start = 1 order by rand() limit 1")
        event = cur.fetchone()

    except mdb.Error, e:
        logging.error("Error %d: %s" % (e.args[0], e.args[1]))

    finally:
        if con:
            con.close()
    return event

def getEventById(evtid):
    event = None
    try:
        con = mdb.connect(config['db']['host'], config['db']['user'], config['db']['pass'], "events")

        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("select * from event_events WHERE eventID=%s", (evtid,))
        event = cur.fetchone()


    except mdb.Error, e:
        logging.error("Error %d: %s" % (e.args[0], e.args[1]))

    finally:
        if con:
            con.close()
    return event

def getEventCommands(event):
    commands = None
    try:
        con = mdb.connect(config['db']['host'], config['db']['user'], config['db']['pass'], "events")

        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("select * from event_commands where eventID = %s", (event,))
        commands = cur.fetchall()

    except mdb.Error, e:
        logging.error("Error %d: %s" % (e.args[0], e.args[1]))

    finally:
        if con:
            con.close()

    return commands

def get_message(msg_idx):
    event = None
    try:
        con = mdb.connect(config['db']['host'], config['db']['user'], config['db']['pass'], config['db']['db'])

        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("select * from msg_queue limit %s, 1", (msg_idx,))
        event = cur.fetchone()


    except mdb.Error, e:
        logging.error("Error %d: %s" % (e.args[0], e.args[1]))

    finally:
        if con:
            con.close()
    return event
