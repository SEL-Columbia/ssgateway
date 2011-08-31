from sqlalchemy import *
from migrate import *

meta = MetaData()
table = Table('circuits', meta,
              Column('uuid', Unicode),
              Column('date', DateTime))

def upgrade(migrate_engine):
    meta.bind = migrate_engine
    # drop the uuid table because we are no longer using it.
    uuid = table.c['uuid']
    uuid.drop()
    # alter the table name because its missing leading.
    date = table.c['date']
    date.alter(name='date_added')

def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pass
