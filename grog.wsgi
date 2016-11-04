import thread
from cgi import parse_qs, escape

import GrogBot

bot = None
bot_thread = None

def grog_thread(channel):
	global bot

	bot = GrogBot.GrogBot(channel)
	bot.run()

# format: {'status':'1','channel':'capn_flint','error':''}

def application(environ, start_response):
	global bot, bot_thread
	qs = parse_qs(environ['QUERY_STRING'])

	channel = "capn_flint"
	action = qs.get('action', [''])[0]

	if not bot:
		if action == 'start':
			bot_thread = thread.start_new_thread(grog_thread, (channel,))
			output = "GrogBot Started in channel: "+channel+"!"
			output = '{"status":-1,"channel":"'+channel+'","error":""}'
		else:
			output = "GrogBot Not Running."
			output = '{"status":0,"channel":"'+channel+'","error":""}'
	else:
		if action == 'stop':
			if environ['mod_wsgi.process_group'] != '':
				import signal, os
				os.kill(os.getpid(), signal.SIGINT)
			output = "Grogbot Stopped"
			output = '{"status":-1,"channel":"'+channel+'","error":""}'
		else:
			output = "GrogBot Running in channel: "+channel+"!"
			output = '{"status":1,"channel":"'+channel+'","error":""}'

	status = '200 OK'
	response_headers = [('Content-type', 'application/JSON'),
								('Content-Length', str(len(output)))]
	start_response(status, response_headers)

	return [output]
