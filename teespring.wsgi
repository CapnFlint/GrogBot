from cgi import parse_qs, escape
from websocket import create_connection
import json

# format: {'status':'1','channel':'capn_flint','error':''}

def send_alert(text):
	data = {}
    data['priority'] = 3
    data['text'] = text
    data['audio'] = [{"file": "sounds/narwhals.mp3", "volume": 40}]

    message = {}
    message['handler'] = 'alert'
    message['data'] = data

    ws = create_connection("ws://capnflint.com:9001")
    ws.send(json.dumps(message))
    ws.recv()
    ws.close()

def application(environ, start_response):
	global bot, bot_thread
	qs = parse_qs(environ['QUERY_STRING'])

	items = qs.get('items', [''])[0]
	items = ','.split(items)

	for item in items:
		send_alert("Someone has snagged some Booty! A [HL]Loot Crate[/HL] is on it's way!")


	status = '200 OK'
	response_headers = [('Content-type', 'application/JSON'),
								('Content-Length', str(len(output)))]
	start_response(status, response_headers)

	return [output]
