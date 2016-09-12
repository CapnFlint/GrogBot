from helper import *
import random

temp_store = 0;
total = 0

@processes('!ecorp')
def command_ecorp(self, sender, args):
    global temp_store
    if args and check_permission(sender, PERM_MOD):
            command = args[0]
            data = args[1:]

            valid_commands = ["add", "remove", "store", "clear", "claim", "total"]

            if command in valid_commands:
                if command == "add":
                    if data:
                        try:
                            value = int(data[0])
                        except:
                            value = 0
                        if value > 0:
                            update_rpUEC(value)
                    else:
                        self.connMgr.send_message("Must specify an amount to Add")

                if command == "remove":
                    if data:
                        try:
                            value = int(data[0])
                        except:
                            value = 0
                        if value > 0:
                            update_rpUEC(-value)
                    else:
                        self.connMgr.send_message("Must specify an ammount to Remove")

                if command == "store":
                    # store funds in the temp storage
                    if data:
                        try:
                            value = int(data[0])
                        except:
                            value = 0
                        if value > 0:
                            temp_store = temp_store + value
                        else:
                            self.connMgr.send_message("Invalid amount specified")

                if command == "clear":
                    temp_store = 0
                    self.connMgr.send_message("Cargo cleared!")

                if command == "claim":
                    # transfer funds from the storage to the total
                    if temp_store > 0:
                        update_rpUEC(temp_store)
                        self.connMgr.send_message(str(temp_store) + " rpUEC Claimed!")
                        temp_store = 0
                    else:
                        self.connMgr.send_message("Nothing to claim!")

                if command == "total":
                    get_total(self)
    else:
        self.connMgr.send_message("To see the rules for Eco-RP go here! http://bit.ly/1WHQX5y")

def update_rpUEC(modifier):
    total = db.eco_get_total() + modifier
    if total < 0:
        total = 0
    db.eco_set_total(total)

def get_total(self):
    total = db.eco_get_total()
    self.connMgr.send_message("Capn currently has: " + str(total) + " rpUEC")
