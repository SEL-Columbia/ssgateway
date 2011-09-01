"""
"""
import argparse
from datetime import datetime
from datetime import timedelta
from logging import getLogger
from logging import Formatter
from logging import StreamHandler
from logging import DEBUG

from pyramid.paster import bootstrap

from ssgateway.models import Meter
from ssgateway.models import DBSession
from ssgateway.models import UnresponsiveCircuit
from ssgateway.models import initialize_sql

log = getLogger('process.check_meters')
log.setLevel(DEBUG)
formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = StreamHandler()
handler.setFormatter(formatter)
log.addHandler(handler)


def check_meters(env):
    """
    Function to check the state of a meter. Run via the command line

      python process_check_meters.py config.ini

    or via a cron job.
    """
    sql_settings = env['registry'].settings['sqlalchemy.url']
    #  initialze the database and bind the models to the connection.
    #  bad things happen if we don't call this.
    initialize_sql(sql_settings)
    session = DBSession()
    meters = session.query(Meter).all()

    for meter in meters:
        time_difference = datetime.now() - timedelta(hours=1)
        log.info('Check meter %s' % meter)
        for c in meter.get_circuits():
            log.info('--> Check for circuit %s ' % c)
            last_log = c.get_last_log()
            # if we have a log
            # often circuits are configured and we never hear from them.
            if last_log is not None:
                if time_difference > last_log.gateway_time:
                    alert = UnresponsiveCircuit(
                        datetime.now(), meter, c, last_log.gateway_time)
                    session.add(alert)
            else:
                log.info('We have not heard from circuit %s' % c.id)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Process SharedSolar Messages')
    parser.add_argument('config', type=str, help='config file')
    args = parser.parse_args()
    env = bootstrap(args.config)

    check_meters(env)
