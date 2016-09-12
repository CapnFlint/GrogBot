
'''
Event Types
1 - First respondant is Selected
2 - All respondants are Selected
3 - Random respondant is Selected
4 - Choice event
5 - Gambling event. One wins, rest lose
6 - Everyone except respondants is Selected
7 - Selected Viewer event


Adding Events
-------------
Events are added by calling: add_event(event, rarity)
Rarity is the relative rarity of the event, ranging from 1 (most rare) to
5 (most common)

Event Template
--------------
<event name> = {
    'type':0,
    'text':'Some <Text>',      # <> denotes command keywords
    'timer':60,                # timeout in seconds before event is failed
    'options':[
        {
        'option':'!text',      # The command to trigger on
        'text':"Some text for if this option is selected.",
        'next':[],           # A link to the next event if this is a chain
        'exp':0,
        'booty':0
        },
        {                      # Add as many options as needed (limited by type)
        'option':"",
        'text':"",
        'next':[],
        'exp':0,
        'booty':0
        }
    ],
    'fail':{                   # failure case, should the event time out
        'text':'mumbles something about leaving him hanging and preferring to drink alone anyway, before shuffling off to the corner with his grog.',
        'next':None,
        'exp':-1,
        'booty':0
    }
}
'''

eventList = []

def add_event(event, rarity):
    for i in range(rarity):
        eventList.append(event)

# -----[ Exp for all! ]---------------------------------------------------------

exp_for_all = {
    'type':1,
    'text':'',
    'timer':0,
    'options':[],
    'fail':{
        'text':'Well played pirates! Bounty for ALL!',
        'next':None,
        'exp':5,
        'booty':1
    }
}

# -----[ Cheers! ]--------------------------------------------------------------

cheers = {
    'type':2,
    'text':'That deserves a drink! [cheers]!',
    'timer':60,
    'options':[
        {
        'option':'!cheers',
        'text':"downs his grog, spilling most of it down his beard...",
        'next':None,
        'exp':5,
        'booty':0
        }
    ],
    'fail':{
        'text':'mumbles something about leaving him hanging and preferring to drink alone anyway, before shuffling off to the corner with his grog.',
        'next':None,
        'exp':-1,
        'booty':0
    }
}

# -----[ Kraken Attack ]--------------------------------------------------------

kraken_attack_2 = {
    'type':3,
    'text':'You must act fast to hit the Kraken\'s weak spot! Who\'s [attack] will succeed?!',
    'timer':60,
    'options':[
        {
        'option':'!attack',
        'text':"{0}'s attack succeeds! The Kraken is repelled!",
        'next':[cheers],
        'exp':15,
        'booty':0
        }
    ],
    'fail':{
        'text':"No-one attacks the Kraken, leaving it to attack with impunity, devestating the ship and knocking everyone overboard! Let's hope you can swim!",
        'next':None,
        'exp':-15,
        'booty':-15
    }
}

kraken_attack = {
    'type':4,
    'text':'The kraken attacks the ship! Do you [defend] the ship, or do you [hide]?',
    'timer':60,
    'options':[
        {
        'option':'!defend',
        'text':'You try to defend the ship! Good show!',
        'exp':5,
        'booty':0,
        'next':[kraken_attack_2]
        },
        {
        'option':'!hide',
        'text':'You all hid! What kind of pirates are you?! Luckily, the kraken decides to go elsewhere for some food...',
        'next':None,
        'exp':5,
        'booty':0,
        'next':[]
        }
    ],
    'fail':{
        'text':"Everyone ignores the Kraken, leaving it to attack with impunity, devestating the ship and knocking everyone overboard! Let's hope you can swim!",
        'next':None,
        'exp':-15,
        'booty':-15
    }
}

vanduul_attack_2 = {
    'type':3,
    'text':'You must act fast to take down the Vanduul ship! Who\'s [attack] will succeed?!',
    'timer':60,
    'options':[
        {
        'option':'!attack',
        'text':"{0}'s attack succeeds! The Vanduul are repelled!",
        'next':[cheers],
        'exp':15,
        'booty':0
        }
    ],
    'fail':{
        'text':"Everyone ignores the Vanduul, leaving them to attack with impunity, devestating the ship and vending everyone into space! Let's hope you're wearing your pressure suit!",
        'next':None,
        'exp':-15,
        'booty':-15
    }
}

vanduul_attack = {
    'type':4,
    'text':'The Vanduul attack the ship! Do you [defend] the ship, or do you !hide ?',
    'timer':60,
    'options':[
        {
        'option':'!defend',
        'text':'You try to defend the ship! Good show!',
        'exp':5,
        'booty':0,
        'next':[vanduul_attack_2]
        },
        {
        'option':'!hide',
        'text':'You all hid! What kind of crew are you?! Luckily, the Vanduul decide to go elsewhere for plunder...',
        'next':None,
        'exp':5,
        'booty':0
        }
    ],
    'fail':{
        'text':"Everyone ignores the Vanduul, leaving it to attack with impunity, devestating the ship and vending everyone into space! Let's hope you're wearing your pressure suit!",
        'next':None,
        'exp':-15,
        'booty':-15
    }
}


# -----[ Kraken Release ]-------------------------------------------------------

kraken_release = {
    'type':1,
    'text':'Release the [kraken]!',
    'timer':60,
    'options':[
        {
        'option':'!kraken',
        'text':'{0}, the capnKraken eats you. You die.',
        'exp':-15,
        'next':[None,kraken_attack],
        'booty':-15
        }
    ],
    'fail':{
        'text':'The Kraken will not be released this day...',
        'exp':0,
        'next':[cheers],
        'booty':0
    }
}

# -----[ Man Overboard! ]-------------------------------------------------------

man_overboard = {
    'type':2,
    'text':'#rand_user# has fallen overboard! Who will try to [save] them?!',
    'timer':120,
    'options':[
        {
        'option':'!save',
        'text':'The sailor has been saved! Nice work!',
        'exp':5,
        'next':None,
        'booty':0
        }
    ],
    'fail':{
        'text':'The poor sailor has drowned. Shame on you all :(',
        'exp':-1,
        'next':None,
        'booty':0
    }
}

man_overboard_space = {
    'type':2,
    'text':'#rand_user# has fallen out the airlock! Who will try to [save] him?!',
    'timer':120,
    'options':[
        {
        'option':'!save',
        'text':'The crewman has been saved! So say we all!',
        'exp':5,
        'next':None,
        'booty':0
        }
    ],
    'fail':{
        'text':'The poor crewman has drifted out of view, never to be seen again. Shame on you all :(',
        'exp':-1,
        'next':None,
        'booty':0
    }
}

# -----[ Island Encounter ]-----------------------------------------------------

island_bad_booty = {
    'type':4,
    'text':'You have found a treasure chest! Do you [open] it, or [leave] it alone?',      # <> denotes command keywords
    'timer':60,                # timeout in seconds before event is failed
    'options':[
        {
        'option':'!open',      # The command to trigger on
        'text':"Carefully you open the chest to find... Cursed gold! At it's touch, the gold crumbles to dust, and the whole crew contracts scurvy! DOH!",
        'next':None,           # A link to the next event if this is a chain
        'exp':-10,
        'booty':0
        },
        {                      # Add as many options as needed (limited by type)
        'option':"!leave",
        'text':"You leave the chest alone... You sense this was a good ideas.",
        'exp':10,
        'booty':0
        }
    ],
    'fail':{                   # failure case, should the event time out
        'text':'While you debate what to do with the treasure chest, you fail to notice a band of pygmies sneak in and abscond with the treasure!',
        'next':None,
        'exp':-5,
        'booty':-5
    }
}

island_booty = {
    'type':4,
    'text':'You have found a treasure chest! Do you [open] it, or [leave] it alone?',      # <> denotes command keywords
    'timer':60,                # timeout in seconds before event is failed
    'options':[
        {
        'option':'!open',      # The command to trigger on
        'text':"Carefully you open the chest to find... a pile of booty! YARRR! R)",
        'next':None,           # A link to the next event if this is a chain
        'exp':10,
        'booty':5
        },
        {                      # Add as many options as needed (limited by type)
        'option':"!leave",
        'text':"You leave the chest alone... apparently you don't like the booty.",
        'exp':0,
        'booty':0
        }
    ],
    'fail':{                   # failure case, should the event time out
        'text':'While you debate what to do with the treasure chest, you fail to notice a band of pygmies sneak in and abscond with the treasure!',
        'next':None,
        'exp':-5,
        'booty':-5
    }
}

island_deserted = {}

island_bottle = {
    'type':4,
    'text':'You have found a bottle washed up on a secluded beach. Looking inside, you find what looks like a treasure map! Do you wish to [follow] the map, or [leave] it here?',      # <> denotes command keywords
    'timer':60,                # timeout in seconds before event is failed
    'options':[
        {
        'option':'!follow',      # The command to trigger on
        'text':"You open the bottle, and pull out the map. It's a bit faded, but you think you can make out the directions... after several days of sailing, you finally approach an island.",
        'next':[island_deserted],           # A link to the next event if this is a chain
        'exp':5,
        'booty':0
        },
        {                      # Add as many options as needed (limited by type)
        'option':"!leave",
        'text':"You leave the bottle there... it seemed a little fishy anyway.",
        'exp':5,
        'booty':0
        }
    ],
    'fail':{                   # failure case, should the event time out
        'text':'While you debate what to do with the treasure chest, you fail to notice a band of pygmies sneak in and abscond with the treasure!',
        'next':None,
        'exp':-5,
        'booty':-5
    }
}

island_deserted = {
    'type':3,
    'text':"The Island seems to be deserted. Who wants to [search] for anything hidden here.",      # <> denotes command keywords
    'timer':60,                # timeout in seconds before event is failed
    'options':[
        {
        'option':'!search',      # The command to trigger on
        'text':"While digging around under a palm tree, {0} finds something!",
        'next':[island_booty, island_booty, island_booty, island_bad_booty],           # A link to the next event if this is a chain
        'exp':5,
        'booty':0
        }
    ],
    'fail':{                   # failure case, should the event time out
        'text':'Being lazy pirates that you are, you all just laze around on the beach, getting a suntan and drinking grog.',
        'next':None,
        'exp':0,
        'booty':0
    }
}

island = {
    'type':4,
    'text':'Your ship passes an Island. Do you stop and [explore], or [continue] your voyage?',      # <> denotes command keywords
    'timer':90,                # timeout in seconds before event is failed
    'options':[
        {
        'option':'!explore',      # The command to trigger on
        'text':"You anchor your ship in a small cove...",
        'next':[island_deserted],           # A link to the next event if this is a chain
        'exp':0,
        'booty':0
        },
        {                      # Add as many options as needed (limited by type)
        'option':"!continue",
        'text':"You decide to continue your voyage, more booty and plunder lies ahead!",
        'next':None,
        'exp':5,
        'booty':0
        }
    ],
    'fail':{                   # failure case, should the event time out
        'text':'While you are scratching your heads about the island, it slowly slips past and out of view...',
        'next':None,
        'exp':-5,
        'booty':0
    }
}

station_pirate = {
    'type':4,
    'text':'You have found an undamaged storage section, locked down and shielded. Do you [open] it, or [leave] it alone?',      # <> denotes command keywords
    'timer':60,                # timeout in seconds before event is failed
    'options':[
        {
        'option':'!open',      # The command to trigger on
        'text':"Bypassing the security system, the doors slide open, and you find... a pirate hideaway! They fight you off, and you escape, but not before suffering some minor injuries.",
        'next':None,           # A link to the next event if this is a chain
        'exp':-10,
        'booty':0
        },
        {                      # Add as many options as needed (limited by type)
        'option':"!leave",
        'text':"You leave the section alone... You had a bad feeling about it anyway.",
        'exp':10,
        'booty':0
        }
    ],
    'fail':{                   # failure case, should the event time out
        'text':'While you debate what to do with storage section, that section of the station suffers a catastrophic breach, and you are forced to retreat back to the ship.',
        'next':None,
        'exp':-5,
        'booty':0
    }
}

station_salvage = {
    'type':4,
    'text':'You have found an undamaged storage section, locked down and shielded. Do you !open it, or [leave] it alone?',      # <> denotes command keywords
    'timer':60,                # timeout in seconds before event is failed
    'options':[
        {
        'option':'!open',      # The command to trigger on
        'text':"Bypassing the security system, the doors slide open, and you find... a stockpile of valuable supplies! So say we all!!!",
        'next':None,           # A link to the next event if this is a chain
        'exp':10,
        'booty':5
        },
        {                      # Add as many options as needed (limited by type)
        'option':"!leave",
        'text':"You leave the section alone... apparently you have no sense of adventure.",
        'exp':0,
        'booty':0
        }
    ],
    'fail':{                   # failure case, should the event time out
        'text':'While you debate what to do with storage section, that section of the station suffers a catastrophic breach, and you are forced to retreat back to the ship.',
        'next':None,
        'exp':-5,
        'booty':0
    }
}

station_deserted = {
    'type':3,
    'text':"The station seems to be deserted. Who wants to [scan] for anything hidden here.",      # <> denotes command keywords
    'timer':60,                # timeout in seconds before event is failed
    'options':[
        {
        'option':'!scan',      # The command to trigger on
        'text':"While performing a spectral analysis, {0} spots an anomoly!",
        'next':[station_salvage, station_salvage, station_salvage, station_pirate],           # A link to the next event if this is a chain
        'exp':5,
        'booty':0
        }
    ],
    'fail':{                   # failure case, should the event time out
        'text':'Being lazy crew that you are, you all just laze around in the lounge, drinking and playing cards.',
        'next':None,
        'exp':0,
        'booty':0
    }
}

station = {
    'type':4,
    'text':'Your ship passes a remote space station. Do you stop and !explore, or [continue] your voyage?',      # <> denotes command keywords
    'timer':90,                # timeout in seconds before event is failed
    'options':[
        {
        'option':'!explore',      # The command to trigger on
        'text':"You draw your ship in for a closer look...",
        'next':[station_deserted],           # A link to the next event if this is a chain
        'exp':0,
        'booty':0
        },
        {                      # Add as many options as needed (limited by type)
        'option':"!continue",
        'text':"You decide to continue your voyage, more adventures lie ahead!",
        'next':None,
        'exp':5,
        'booty':0
        }
    ],
    'fail':{                   # failure case, should the event time out
        'text':'While you are scratching your heads about the station, it slowly slips past and out of view...',
        'next':None,
        'exp':-5,
        'booty':0
    }
}

# -----[ Gamble Event ]---------------------------------------------------------

cup_game = {
    'type':5,
    'text':'slides the three cups around the table rapidly, before stopping and asking: [left] [middle] or [right]?',      # <> denotes command keywords
    'timer':60,                # timeout in seconds before event is failed
    'options':[
        {
        'option':'!left',      # The command to trigger on
        'text':"The left cup held the ball!",
        'next':None,           # A link to the next event if this is a chain
        'exp':0,
        'booty':5
        },
        {                      # Add as many options as needed (limited by type)
        'option':"!middle",
        'text':"The middle cup held the ball!",
        'next':None,
        'exp':0,
        'booty':5
        },
        {                      # Add as many options as needed (limited by type)
        'option':"!right",
        'text':"The right cup held the ball!",
        'next':None,
        'exp':0,
        'booty':5
        }
    ],
    'fail':{                   # failure case, should the event time out
        'text':'No-one picked anything :(',
        'next':None,
        'exp':-1,
        'booty':0
    }
}


# ------------------------------------------------------------------------------

ship_merchant_coward = {
    'type':4,
    'text':'',      # <> denotes command keywords
    'timer':0,                # timeout in seconds before event is failed
    'options':[
    ],
    'fail':{                   # failure case, should the event time out
        'text':'The merchants are terrified, panic, and jump overboard... the score is yours!',
        'next':None,
        'exp':5,
        'booty':5
    }
}

fight_good = {
    'type':4,
    'text':'',      # <> denotes command keywords
    'timer':0,                # timeout in seconds before event is failed
    'options':[
    ],
    'fail':{                   # failure case, should the event time out
        'text':'You win the fight, and take barely any injuries! The haul is great :D',
        'next':None,
        'exp':5,
        'booty':15
    }
}

fight_bad = {
    'type':4,
    'text':'',      # <> denotes command keywords
    'timer':0,                # timeout in seconds before event is failed
    'options':[
    ],
    'fail':{                   # failure case, should the event time out
        'text':'You manage to escape with your lives... barely. The ship keeps most of the plunder',
        'next':None,
        'exp':-5,
        'booty':5
    }
}

ship_merchant_armed = {
    'type':3,
    'text':'This is a heavily armed vessel, they must be carrying something valuable! The fight is long and bloody... who will [fight]?',      # <> denotes command keywords
    'timer':60,                # timeout in seconds before event is failed
    'options':[
        {
        'option':'!fight',      # The command to trigger on
        'text':"You fight as hard as you can! {0} manages to capture their captain and end the fight!",
        'next':[fight_good, fight_bad],           # A link to the next event if this is a chain
        'exp':10,
        'booty':0
        },
        {
        'option':'!leave',      # The command to trigger on
        'text':"The crew chooses to leave it running. It didn't look like it was carrying much anyway...",
        'next':[],           # A link to the next event if this is a chain
        'exp':5,
        'booty':0
        },
    ],
    'fail':{                   # failure case, should the event time out
        'text':'While you debate, the ship slips out of view, and is gone forever!',
        'next':None,
        'exp':-1,
        'booty':0
    }
}

ship_merchant = {
    'type':4,
    'text':'You gain on the ship, and see that it is a merchantman! Should we [board] or [leave] her?',      # <> denotes command keywords
    'timer':60,                # timeout in seconds before event is failed
    'options':[
        {
        'option':'!board',      # The command to trigger on
        'text':"The crew chooses to board the ship!",
        'next':[ship_merchant_coward, ship_merchant_armed],           # A link to the next event if this is a chain
        'exp':1,
        'booty':0
        },
        {
        'option':'!leave',      # The command to trigger on
        'text':"The crew chooses to leave it running. It didn't look like it was carrying much anyway...",
        'next':[],           # A link to the next event if this is a chain
        'exp':5,
        'booty':0
        },
    ],
    'fail':{                   # failure case, should the event time out
        'text':'While you debate, the ship slips out of view, and is gone forever!',
        'next':None,
        'exp':-1,
        'booty':0
    }
}

navy_win = {
    'type':4,
    'text':'',      # <> denotes command keywords
    'timer':0,                # timeout in seconds before event is failed
    'options':[
    ],
    'fail':{                   # failure case, should the event time out
        'text':'They put up a rousing fight, but our crew prevails and sinks their vessel!',
        'next':None,
        'exp':15,
        'booty':5
    }
}

navy_escape = {
    'type':3,
    'text':'GrogBot, in chains, looks around with a glint in his eye. So, who wants to lead the [escape]?',      # <> denotes command keywords
    'timer':60,                # timeout in seconds before event is failed
    'options':[
        {
        'option':'!escape',      # The command to trigger on
        'text':"{0} jumps the guard, unties the crew, and releases the narwhal! We get on board, and sneakily sail away into the night...",
        'next':[],           # A link to the next event if this is a chain
        'exp':10,
        'booty':0
        },
    ],
    'fail':{                   # failure case, should the event time out
        'text':'You rot in manacles until they get bored of torturing you, and drop you off on a desert island.',
        'next':None,
        'exp':-5,
        'booty':0
    }
}

navy_lose = {
    'type':4,
    'text':'',      # <> denotes command keywords
    'timer':0,                # timeout in seconds before event is failed
    'options':[
    ],
    'fail':{                   # failure case, should the event time out
        'text':'They put a cannonball through our mast, they have captured the Narwhal!',
        'next':[navy_escape],
        'exp':-10,
        'booty':0
    }
}

ship_navy = {
    'type':4,
    'text':'You gain on the ship, and see that it is a naval ship of the line! It turns about to engage. Do you [fight] or [flee]?',      # <> denotes command keywords
    'timer':60,                # timeout in seconds before event is failed
    'options':[
        {
        'option':'!fight',      # The command to trigger on
        'text':"You steele yourselves, ready for the attack, and come about to present a broadside!",
        'next':[navy_win, navy_lose],           # A link to the next event if this is a chain
        'exp':1,
        'booty':0
        },
        {
        'option':'!flee',      # The command to trigger on
        'text':"Seeing you might be outmatched, you open all the sails, and speed away. Live to fight another day!!!",
        'next':[],           # A link to the next event if this is a chain
        'exp':5,
        'booty':0
        },
    ],
    'fail':{                   # failure case, should the event time out
        'text':'While you debate, the ship rakes you stern to aft, crippling you before sailing off!',
        'next':None,
        'exp':-5,
        'booty':0
    }
}

ship_ghost = {
    'type':4,
    'text':'',      # <> denotes command keywords
    'timer':0,                # timeout in seconds before event is failed
    'options':[
    ],
    'fail':{                   # failure case, should the event time out
        'text':"It's a ghost ship! The wails of the damned grow louder as the Narwhal is sucked into the depths!",
        'next':[],
        'exp':-10,
        'booty':0
    }
}

chase = {
    'type':4,
    'text':'Should we [chase] it down?',      # <> denotes command keywords
    'timer':120,                # timeout in seconds before event is failed
    'options':[
        {
        'option':'!chase',      # The command to trigger on
        'text':"",
        'next':[ship_merchant, ship_navy, ship_merchant, ship_navy, ship_merchant, ship_navy, ship_ghost],           # A link to the next event if this is a chain
        'exp':0,
        'booty':0
        },
    ],
    'fail':{                   # failure case, should the event time out
        'text':'The ship slips out of view, and is gone forever!',
        'next':None,
        'exp':-1,
        'booty':0
    }
}

sails = {
    'type':3,
    'text':'Sails on the horizon! Who will [search]?',      # <> denotes command keywords
    'timer':60,                # timeout in seconds before event is failed
    'options':[
        {
        'option':'!search',      # The command to trigger on
        'text':"{0} spots the ship!",
        'next':[chase],           # A link to the next event if this is a chain
        'exp':5,
        'booty':0
        },
    ],
    'fail':{                   # failure case, should the event time out
        'text':'Whatever it was disappears behind the curve of the waves, lost to view.',
        'next':None,
        'exp':-1,
        'booty':0
    }
}

# ------------------------------------------------------------------------------

add_event(sails, 2)
add_event(kraken_release, 3)
add_event(kraken_attack, 2)
add_event(man_overboard, 3)
add_event(island, 2)
add_event(cup_game, 5)

#add_event(gamble_test,1)
#add_event(station, 2)
#add_event(man_overboard_space, 3)
#add_event(vanduul_attack, 2)
