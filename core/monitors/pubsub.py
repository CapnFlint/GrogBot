

# send PING

# handle PONG

# handle RECONNECT

# send LISTEN
'''
// Request from client to server
{
  "type": "LISTEN",
  "nonce": "44h1k13746815ab1r2",
  "data": {
    "topics": ["channel-bits-events-v1.<chan id>","channel-subscribe-events-v1.<chan id>","whispers.<user id>"],
    "auth_token": "cfabdegwdoklmawdzdo98xt2fo512y"
  }
}
'''

# handle RESPONSE
'''
// Response from server to client
{
  "type": "RESPONSE",
  "nonce": "44h1k13746815ab1r2",
  "error": ""
}
'''

# handle Message
'''
Bits:
{
   "type": "MESSAGE",
   "data": {
      "topic": "channel-bits-events-v1.44322889",
      "message": "{\"data\":{\"user_name\":\"dallasnchains\",\"channel_name\":\"dallas\",\"user_id\":\"129454141\",\"channel_id\":\"44322889\",\"time\":\"2017-02-09T13:23:58.168Z\",\"chat_message\":\"cheer10000 New badge hype!\",\"bits_used\":10000,\"total_bits_used\":25000,\"context\":\"cheer\",\"badge_entitlement\":{\"new_version\":25000,\"previous_version\":10000}},\"version\":\"1.0\",\"message_type\":\"bits_event\",\"message_id\":\"8145728a4-35f0-4cf7-9dc0-f2ef24de1eb6\"}"
   }
}

Subs:
{
   "type": "MESSAGE",
   "data": {
      "topic": "channel-subscribe-events-v1.44322889",
      "message": {
         "user_name": "dallas",
         "display_name": "dallas",
         "channel_name": "twitch",
         "user_id": "44322889",
         "channel_id": "12826",
         "time": "2015-12-19T16:39:57-08:00",
         "sub_plan": "Prime"/"1000"/"2000"/"3000",
         "sub_plan_name": "Mr_Woodchuck - Channel Subscription (mr_woodchuck)",
         "months": 9,
         "context": "sub"/"resub",
         "sub_message": {
            "message": "A Twitch baby is born! KappaHD",
            "emotes": [
            {
               "start": 23,
               "end": 7,
               "id": 2867
            }]
         }
     }
   }
}
'''
