from helper import *
import random

@processes('!ask')
def command_ask(self, data):
    options = [
        "Signs point to Aye.",
        "Aye.",
        "The seas be stormy, try again.",
        "No doubt matey.",
        "I 'eard nay matey",
        "As I see it, Aye",
        "You can count on it.",
        "Think 'arder and ask again.",
        "Outlook's bleak matey.",
        "I reckon so.",
        "Better not tell you now.",
        "It be doubtful.",
        "Aye - definitely.",
        "It be certain.",
        "Can't be guessin' now.",
        "Most likely.",
        "Ask again later.",
        "I say no matey.",
        "Outlook good.",
        "Wouldn't count on it matey.",
        "Aye, in due time.",
        "Definitely nay.",
        "Aye.",
        "Ya gotta wait.",
        "I 'ave me doubts.",
        "Outlook's so so.",
        "Looks good to me matey!",
        "Who knows?",
        "It's lookin' good!",
        "Probably.",
        "Are ye kiddin'?",
        "Go fer it!",
        "Don't bet yer life on it.",
        "Ferget 'bout it"
    ]
    picked = random.choice(options)
    self.connMgr.send_message(data['sender'] + ", " + picked)
