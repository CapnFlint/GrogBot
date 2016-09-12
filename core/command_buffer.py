

class command_buffer():
    '''
    command_buffer is used to buffer command invocations for any given command.
    This can buffer any number of commands, and creates an individual buffer for
    each command buffered.
    '''
    def __init__(self, owner):
        self.commandTimer = 5
        self.commandBuffer = {}
        self.owner = owner
        self.locked = False

    def buffer_command(self, cmd, args):

        if cmd not in self.commandBuffer:
            self.commandBuffer[cmd] = []
        if not args in self.commandBuffer[cmd]:
            self.commandBuffer[cmd].append(args)

    def buffer_manager(self, frequency):
        while 1:
            time.sleep(frequency)
            if self.commandBuffer:
                #self.locked = True
                for command in self.commandBuffer:
                    command(self.owner, self.commandBuffer[command])
                self.commandBuffer = {}
                #self.locked = False


    def start(self):
        thread.start_new_thread(self.buffer_manager, (self.commandTimer,))
