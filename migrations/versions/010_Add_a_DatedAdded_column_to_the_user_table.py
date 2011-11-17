from sqlalchemy import *
from migrate import *

meta = MetaData()
users = Table('users', meta)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    meta.bind = migrate_engine
    date_added = Column('date_added', DateTime())
    date_added.create(users)


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta.bind = migrate_engine
    users.c['date_added'].drop()
