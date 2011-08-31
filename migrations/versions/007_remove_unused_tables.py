from sqlalchemy import *
from migrate import *

meta = MetaData()

k_i_msg = Table('kannel_incoming__message', meta)
k_o_msg = Table('kannel_outgoing_message', meta)
k_job_msg = Table('kannel_job_message', meta)
meter_msg = Table('meter_messages', meta)
meter_changeset = Table('meterchangeset', meta)
test_msg = Table('test_message', meta)
e_max = Table('energy_max', meta)
alert = Table('alert', meta)
meterconfigkey = Table('meterconfigkey', meta)
sys_logs = Table('system_log', meta)

def upgrade(migrate_engine):
    meta.bind = migrate_engine
    k_i_msg.drop()
    k_o_msg.drop()
    k_job_msg.drop()
    meter_msg.drop()
    meter_changeset.drop()
    test_msg.drop()
    e_max.drop()
    alert.drop()
    meterconfigkey.drop()
    sys_logs.drop()

def downgrade(migrate_engine):
    meta.bind = migrate_engine
    
