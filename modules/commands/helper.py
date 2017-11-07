from collections import defaultdict
import utils.db_utils as db

command_dict = dict()
command_perm = defaultdict(list)
opsListDic = defaultdict(list)

PERM_NONE = 0
PERM_MOD = 1
PERM_ADMIN = 2
PERM_FOLLOWS = 3
PERM_SUBSCRIBER = 4

def check_permission(data, level):
    access = db.get_access(data['sender'])

    if level == PERM_MOD:
        if data['perm']['mod']:
            return True
    elif level == PERM_SUBSCRIBER:
        if data['perm']['sub']:
            return True
    else:
        if access >= level:
            return True

    return False

def get_commands():
    global command_dict
    return command_dict

def processes(command, perm=PERM_NONE):
    global command_dict
    def wrap(func):
        # do pre-wrap
        print "Registering command: " + command
        def wrapped(self, data):
            if check_permission(data, perm):
                func(self, data)
            else:
                self.connMgr.send_message('No permissions for that!')
        command_dict[command] = wrapped
        command_perm[perm].append(command)
        return wrapped
        # do post-wrap
    return wrap
