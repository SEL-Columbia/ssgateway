from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Float
from sqlalchemy import Boolean
from sqlalchemy import Unicode
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relation
from zope.sqlalchemy import ZopeTransactionExtension
import hashlib
import random

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Groups(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(100))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '#<Group %s>' % self.name


class Users(Base):
    """
    Users are authorized to log into the Gateway UI
    There are two different groupd, viewers and admins.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(100))
    password = Column(Unicode(100))
    email = Column(Unicode(100))
    notify = Column(Boolean)
    group_id = Column(
        Integer,
        ForeignKey('groups.id'))

    group = relation(
        Groups,
        primaryjoin=group_id == Groups.id)

    def __init__(self,
                 name,
                 password,
                 email,
                 notify,
                 group):
        self.name = name
        if password is not None:
            hash = hashlib.md5(password).hexdigest()
        self.password = hash
        self.email = email
        self.notify = notify
        self.group = group

    def __repr_(self):
        return '#<User %s>' % self.name


class Device(Base):
    """ Devices are Android tablets that can request tokens from the Gateway"""
    __tablename__ = 'devices'
    id = Column(Integer, primary_key=True)
    device_id = Column(Unicode(100))
    password = Column(Unicode(100))

    def __init__(self, device_id, password):
        self.device_id = device_id
        self.password = password

    def __str__(self):
        return '#<Device %s>' % self.device_id


class TimeZone(Base):
    """ Class to record and manager time zones.
    This is important for making sense of timestamps"""
    __tablename__ = 'time_zones'
    id = Column(Integer, primary_key=True)
    zone = Column(Unicode(256), unique=True)

    def __init__(self, zone):
        self.zone = zone

    def __repr__(self):
        return '#<TimeZone %s>' % self.zone


class Meter(Base):
    """
    A class that repsents a meter in the gateway.
    """
    __tablename__ = 'meters'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    phone = Column(Unicode)
    location = Column(Unicode)
    status = Column(Boolean)
    date_added = Column(DateTime)
    battery_capacity = Column(Integer)
    panel_capacity = Column(Integer)
    time_zone_id = Column(Integer, ForeignKey('time_zones.id'))
    time_zone = relation(TimeZone, primaryjoin=time_zone_id == TimeZone.id)

    def __init__(self,
                 name,
                 phone,
                 location,
                 status,
                 date_added,
                 battery_capacity,
                 panel_capacity):
        self.name = name
        self.phone = phone
        self.status = status
        self.date_added = date_added
        self.battery_capacity = battery_capacity
        self.panel_capacity = panel_capacity

    def __repr__(self):
        return '#<Meter %s>' % self.name


class Account(Base):
    """
    This class stores information about the customer.
    """
    __tablename__ = 'account'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    phone = Column(Unicode)
    lang = Column(Unicode)

    def __init__(self, name, phone, lang):
        self.name = name
        self.phone = phone
        self.lang = lang

    def __repr__(self):
        return '#<Account %s>' % (self.id, self.phone)


class Circuit(Base):
    """
    This class allows the Gateway to track and
    manage the hardware information about each circuit.
    """
    __tablename__ = 'circuits'

    id = Column(Integer, primary_key=True)
    date_added = Column(DateTime)
    pin = Column(Unicode)
    energy_max = Column(Float)
    power_max = Column(Float)
    status = Column(Integer)
    ip_address = Column(Unicode)
    credit = Column(Float)
    meter_id = Column('meter', ForeignKey('meters.id'))
    meter = relation(Meter,
                     primaryjoin=meter_id == Meter.id)
    account_id = Column(Integer, ForeignKey('account.id'))
    account = relation(Account,
                       primaryjoin=account_id == Account.id)

    def __init__(self,
                 meter,
                 account,
                 date_added,
                 pin,
                 energy_max,
                 power_max,
                 ip_address,
                 status,
                 credit):

        self.date_added = date_added
        self.meter = meter
        self.pin = pin
        self.energy_max = energy_max
        self.power_max = power_max
        self.ip_address = ip_address
        self.status = status
        self.credit = credit
        self.account = account

    @staticmethod
    def get_pin():
        ints = '23456789'
        return ''.join(random.sample(ints, 6))


class Message(Base):
    """
    Abstract class for all messages
    """
    __tablename__ = "message"
    type = Column('type', Unicode(50))
    __mapper_args__ = {'polymorphic_on': type}
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    sent = Column(Boolean)
    number = Column(Unicode)
    uuid = Column(Unicode)

    def __init__(self, date, number, uuid):
        self.date = date
        self.number = number
        self.uuid = uuid


def initialize_sql(engine):
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
