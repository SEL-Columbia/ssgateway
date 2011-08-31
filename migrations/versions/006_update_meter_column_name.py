from sqlalchemy import *
from migrate import *

meta = MetaData()

table  = Table('meters',
               meta,
               Column('uuid', String),
               Column('battery', Integer),
               Column('slug', String),
               Column('date', DateTime))


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    date = table.c['date']
    # update the to date column name.
    date.alter(name='date_added')
    # remove the slug column because we do not use it
    slug = table.c['slug']
    slug.drop()
    # update the battery column to battery_capacity
    battery = table.c['battery']
    battery.alter(name='battery_capacity')
    # remove the uuid column
    uuid = table.c['uuid']
    uuid.drop()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    date = table.c['date_added']
    date.alter(name='date')
