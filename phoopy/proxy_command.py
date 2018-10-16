from cleo import Command


class ProxyCommand(Command):
    def __init__(self, command_class, service_key, container):
        self.__doc__ = command_class.__doc__
        super(ProxyCommand, self).__init__()
        self.__service_key = service_key
        self.__container = container

    def handle(self):
        command = self.__container[self.__service_key]
        command.input = self.input
        command.output = self.output
        return command.handle()

    def interact(self, input_, output_):
        # If needed implement here
        pass
