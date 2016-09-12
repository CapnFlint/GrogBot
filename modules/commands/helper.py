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

def check_permission(user, level):
    access = db.get_access(user)

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
        def wrapped(self, sender, args):
            if check_permission(sender, perm):
                func(self, sender, args)
            else:
                self.connMgr.send_message('No permissions for that!')
        command_dict[command] = wrapped
        command_perm[perm].append(command)
        return wrapped
        # do post-wrap
    return wrap

"""
def permission(perm):
    def wrap(func):
        def wrapped(self, sender, args):
            if check_permission(sender, perm):
                func(self,sender,args)
            else:
                self.connMgr.send_message('No permissions for that!')
        wrapped.__name__ = func.__name__
        opsListDic[perm].append("!" + func.__name__.split('_')[1])
        return wrapped
    return wrap
"""
