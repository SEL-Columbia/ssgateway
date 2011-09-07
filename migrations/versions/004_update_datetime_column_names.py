from sqlalchemy import *
from migrate import *

meta = MetaData()

table = Table('logs',
               meta,
               Column('date', DateTime))


def upgrade(migrate_engine):
    """
    """
    meta.bind = migrate_engine
    date = table.c['date']
    date.alter(name='meter_time')


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    date = table.c['meter_time']
    date.alter(name='date')
