from helper import *

@processes('!commands')
def command_commands(self, data):
    self.connMgr.send_message("To see all the available commands, visit: https://www.capnflint.com/commands.php")
    '''perm_lvl = db.get_access(sender)

    cmds_per_line = 50

    commands = []
    for key in command_perm.keys():
        if perm_lvl >= key:
            commands += command_perm[key]
    custom_commands = db.get_custom_commands()
    commands += custom_commands.keys()
    commands = sorted(commands)

    self.connMgr.send_message("The commands available are: ")

    while len(commands):
        cmds = commands[:cmds_per_line]
        commands = commands[cmds_per_line:]
        self.connMgr.send_message(', '.join(cmds))'''
