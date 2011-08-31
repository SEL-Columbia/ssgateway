from sqlalchemy import *
from migrate import *

meta = MetaData()

table = Table('circuit', meta)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind migrate_engine
    # to your metadata
    meta.bind = migrate_engine
    table.rename('circuits')


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here
    meta.bind = migrate_engine
    table.rename('circuit')

