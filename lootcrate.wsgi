from cgi import parse_qs, escape
from websocket import create_connection
import json
import MySQLdb as mdb
import config.db_config as config

# format: {'status':'1','channel':'capn_flint','error':''}

def add_stat(count):
	try:
		con = mdb.connect(config.db_host, config.db_user, config.db_pass, config.db_db);
		value = 0
		with con:
			cur = con.cursor(mdb.cursors.DictCursor)
			cur.execute("SELECT value from stats where stat = 'lootcrate'", (name))
			stat = cur.fetchone()

			if stat:
				value = int(stat['value']) + int(count)
				cur.execute("UPDATE stats SET value = %s WHERE stat = 'lootcrate'", (value, name))
	except mdb.Error, e:
		print "Error %d: %s" % (e.args[0],e.args[1])
		return 0

	finally:
		if con:
			con.close()
	return value

def send_message(handler, data):
	message = {}
	message['handler'] = handler
	message['data'] = data

	ws = create_connection("ws://capnflint.com:9001")
	ws.send(json.dumps(message))
	ws.recv()
	ws.close()

def send_alert(text):
	data = {}
	data['priority'] = 3
	data['text'] = text
	data['audio'] = [{"file": "sounds/narwhals.mp3", "volume": 40}]
	send_message("alert", data)

def update_stat(value):
	data = {}
	data['stat'] = 'lootcrate'
	data['value'] = value
	send_message("stats", data)

def application(environ, start_response):
	global bot, bot_thread
	qs = parse_qs(environ['QUERY_STRING'])

	items = qs.get('items', [''])[0]
	items = ','.split(items)

	for item in items:
		send_alert("Someone has snagged some Booty! A [HL]Loot Crate[/HL] is on it's way!")

	count = add_stat(len(items))
	update_stat(count)

	output = "Success!"

	status = '200 OK'
	response_headers = [('Content-type', 'application/JSON'),
								('Content-Length', str(len(output)))]
	start_response(status, response_headers)

	return [output]
