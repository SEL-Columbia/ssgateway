
from datetime import datetime
from datetime import timedelta
import argparse
from pyramid.paster import bootstrap

from ssgateway.models import initialize_sql
from ssgateway.models import DBSession
from ssgateway.models import PrimaryLog
from ssgateway.models import Circuit

time_format = '%Y-%m-%d'
time_error_msg = 'You must provided the time object in YYYY-MM-DD'


def find_message_gaps(env, start_time_str, end_time_str):
    """
    Arguments:
          start_time_str: YYYY-MM-DD
          end_time_str:   YYYY-MM-DD
          env: Pyramid context

    Values: returns None

    Purpose:

    """
    sql_settings = env['registry'].settings['sqlalchemy.url']
    #  initialze the database and bind the models to the connection.
    #  bad things happen if we don't call this.
    initialize_sql(sql_settings)
    session = DBSession()

    try:
        start_date = datetime.strptime(start_time_str, time_format)
    except:
        raise NameError(time_error_msg)

    try:
        end_date = datetime.strptime(end_time_str, time_format)
    except:
        raise NameError(time_error_msg)

    if start_date >= end_date:
        raise NameError('start must be before end')

    time_diff = end_date - start_date
    time_diff_hours = ((time_diff.total_seconds() / 60) / 60)
    print 'Find gaps for %s ' % time_diff_hours

    logs = session.query(PrimaryLog)\
        .filter(PrimaryLog.meter_time >= start_date)\
        .filter(PrimaryLog.meter_time < end_date)

    print 'Total number of logs %s ' % logs.count()
    excepted = len(session.query(Circuit).all()) * time_diff_hours * 2 
    print (logs.count() / excepted)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='A script to \
compare the WIFI ftps logs to the gateway databsae')

    parser.add_argument('config', type=str, help='config file')
    parser.add_argument('start', type=str, help='str repr of day')
    parser.add_argument('end', type=str, help='str repr of day')

    args = parser.parse_args()
    env = bootstrap(args.config)
    find_message_gaps(env, args.start, args.end)
