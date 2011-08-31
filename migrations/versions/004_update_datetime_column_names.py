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
    date.alter(name='gateway_time')


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    date = table.c['gateway_time']
    date.alert(name='date')
