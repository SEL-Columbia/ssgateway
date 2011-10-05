"""
"""
from urlparse import parse_qs
from ssgateway.message import log


def parse_consumer(message):
    delimiter = "."
    message['payload'] = message['body'].split(delimiter)
    message['command'] = message['payload'][0]
    return message


def parse_meter_compressed(message):
    return message


def parse_meter_pcu(message):
    return message


def _reduce_values(_dict):
    c = {}
    for key, value in _dict.iteritems():
        c[key] = value[0]
    return c


def _assoc_meter_command(message):
    """
    Function to associate a message with a command in the system.
    TODO, maybe this should be configurable?
    """
    job = message['payload']['job']
    log.info('Looking up command for message: %s' % message)
    # if the job type is alert, the actually action is in the alert
    # key
    if job == 'alert':
        message['command'] = message['payload']['alert']
    # else the action is in the job key
    else:
        message['command'] = job
    log.info('Found command %s' % message['command'])
    return message


def parse_meter(message):
    """
    Function to parse uncompressed meter messages
    args: message dict with at least a body key
    """
    log.info('Parsing meter message : %s' % (message))
    body = message['body']
    # parse the body of the meter message
    payload = parse_qs(body.strip('(').strip(')'))
    # take out extra keys
    message['payload'] = _reduce_values(payload)
    log.info('Data assoc with message ->  %s ' % (message['payload']))
    return _assoc_meter_command(message)
