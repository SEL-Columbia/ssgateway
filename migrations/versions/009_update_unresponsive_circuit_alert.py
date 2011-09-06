from sqlalchemy import *
from migrate import *

meta = MetaData()
alert = Table('unresponsive_circuit', meta, Column('last_heard_from', Float))


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    last = alert.c['last_heard_from']
    last.alter(Column('last_heard_from', DateTime(timezone=False)))


def downgrade(migrate_engine):
    meta.bind = migratte_engine
    last = alert.c['last_heard_from']
    last.alter(Column('last_heard_from', Float))
