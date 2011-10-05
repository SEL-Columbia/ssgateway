import re
from logging import getLogger
from logging import Formatter
from logging import StreamHandler
from logging import DEBUG


log = getLogger('ssgateway.message.main')
log.setLevel(DEBUG)
formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

handler = StreamHandler()
handler.setFormatter(formatter)

log.addHandler(handler)


def _import_func(func_str):
    import importlib
    # split the func path
    func_path = func_str.split('.')
    module = importlib.import_module('.'.join(func_path[:-1]))
    return getattr(module, func_path[-1])


def log_function(f):
    def wrap(*args):
        #log.info('Calling %s with --> %s' % (f.__name__, args[0]))
        results = apply(f, args)
        #log.info('Returning %s with--> %s' % (f.__name__, results))
        return results
    return wrap


@log_function
def classify(message, config):
    for classifer in config['classifers']:
        if re.match(classifer['classifer'], message['body']):
            message['classification'] = classifer
            return message
    return message


@log_function
def final_parse(message):
    parser_func = _import_func(message['classification']['parser'])
    return parser_func(message)


@log_function
def route_message(message, config):
    for route in config['routes']:
        for command in route['commands']:
            if command == message['command']:
                log.info('Assoc message with route: %s' % route)
                message['route'] = route
                return message
    return message


def invoke_route(message):
    log.info('Invoking message with route')
    route = _import_func(message['route']['name'])
    route(message)


def main(config):
    """
    """
    assert isinstance(config, dict)
    # log.info('Loading message-router with %s config file' % config)

    def call_route(message):
        """
        A message is a python dict object that has two required keys
           phone-number: should be a unicode of a person's number
           body: should be a unicode object of the message body

        """
        log.info(message)
        assert 'phone-number' in message
        assert 'body' in message

        final_message = route_message(
            final_parse(
                classify(message, config)
                ), config)
        invoke_route(final_message)
    return call_route
