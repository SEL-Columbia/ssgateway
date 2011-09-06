"""
Script to compare the WIFI FTP repots to the data base log.
"""
from datetime import datetime
import argparse
from pyramid.paster import bootstrap

from ssgateway.models import initialize_sql
from ssgateway.models import DBSession


def compare_logs(day_str, env):
    """
    Function to compare csv file format to the actually Gateway database.

    Arguments:
        day: a string repersentation of a date object
           YYYY-MM-DD
           2011-08-02
    Values:
        returns the difference between the numnber of messages sent to the gateway and the amount in the database.
    Purpose:
    To give a better understand of the precent update provided by Airtel/WIFI
    """
    sql_settings = env['registry'].settings['sqlalchemy.url']
    #  initialze the database and bind the models to the connection.
    #  bad things happen if we don't call this.
    initialize_sql(sql_settings)
    session = DBSession()
    try:
        query_date = datetime.strptime(day_str, '%Y-%m-%d')
    except:
        raise NameError('You must provided the time object in YYYY-MM-DD')

    print query_date


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='A script to compare \
the WIFI ftps logs to the gateway databsae')

    parser.add_argument('config', type=str, help='config file')
    parser.add_argument('day', type=str, help='str repr of day')

    args = parser.parse_args()
    env = bootstrap(args.config)
    compare_logs(args.day, env)
