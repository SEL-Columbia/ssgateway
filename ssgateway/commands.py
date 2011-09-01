from paste.script.command import Command
from pyramid.paster import bootstrap


class RunMessage(Command):
    """
    """

    summary = 'Command to test and message'
    parser = Command.standard_parser()
    parser.add_option('--message',
                      dest='message',
                      help='String repr of a message to test')

    def command(self):
        from ssgateway.message import main
        from yaml import load
        config_uri = self.args[0]
        env = bootstrap(config_uri)
        route_config = env['registry'].settings.get('routes')
        message_router = main(load(open(route_config)))
        message_router(self.args[1])
        env['closer']()

class PrintRoutes(Command):
    """
    """
    summary = 'Prints all of the message routes currently configured'

    parser = Command.standard_parser()

    def command(self):
        from yaml import load
        config_uri = self.args[0]
        env = bootstrap(config_uri)
        route_config = env['registry'].settings.get('routes')
        print load(open(route_config))
        env['closer']()
