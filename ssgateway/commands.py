import argparse
from pyramid.paster import bootstrap
from ssgateway.models import Base
from ssgateway.models import initialize_sql


def initialize_command(parser):
    """ Stuff we need to do for every command"""
    parser.add_argument('--config', dest='config',
                        help='the pyramid config file')
    args = parser.parse_args()
    assert args.config,\
        'You must have a --config config.ini, or we can\'t run the command'
    # load the pyramid config env
    env = bootstrap(args.config)
    # load the database
    initialize_sql(
        env['registry'].settings.get('sqlalchemy.url'))
    # return the args and the pyramid env for later use
    return args, env


def _find_table(name):
    """ Function to look up a table"""
    tables = Base.metadata.tables
    table = tables.get(name, None)
    if table is not None:
        return table
    else:
        raise NameError('Unable to locate table: %s' % name)


def export_table():
    """ Function to export a table to a yaml file """

    from yaml import dump
    parser = argparse.ArgumentParser(
        description='export a table to a yaml file')
    parser.add_argument('--table', dest='table',
                        help='the table to export')
    args, env = initialize_command(parser)

    table = _find_table(args.table)
    columns = table.c.keys()
    data = []
    # iter through the table
    for row in table.select().execute():
        c = {}
        assert len(columns) == len(row),\
            'The number of columns should match the length of the row'
        for i in range(len(columns)):
            column = table.c[columns[i]]
            cell = row[i]
            c[column.name] = cell
        data.append(c)
    print dump(data)

    # close the env
    env['closer']()


def import_table():
    from yaml import load
    parser = argparse.ArgumentParser(
        description='export a table to a yaml file')
    parser.add_argument('--table', dest='table',
                        help='the table to export')

    parser.add_argument('--file', dest='file',
                        help='the yaml file to load from')
    args, env = initialize_command(parser)
    # load the fixtures file
    rows = load(open(args.file, 'r'))
    table = _find_table(args.table)
    print 'Loading data for table: %s' % table
    for row in rows:
        # slow but easy to understand way to insert data into the
        # table
        table.insert().execute(row)
    env['closer']()


def run_message():
    """
    Command that allows a user to run the message against the gateway
    """
    import simplejson
    from ssgateway.message import main
    from yaml import load
    parser = argparse.ArgumentParser(
        description='export a table to a yaml file')
    parser.add_argument('--message', dest='message',
                        help='the message to run')
    args, env = initialize_command(parser)

    message = simplejson.loads(args.message)
    route_config = env['registry'].settings.get('routes')
    message_router = main(load(open(route_config)))
    message_router(message)

    env['closer']()
