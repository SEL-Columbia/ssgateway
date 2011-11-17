from datetime import datetime
from datetime import timedelta

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Float
from sqlalchemy import Boolean
from sqlalchemy import Unicode
from sqlalchemy import Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relation
from sqlalchemy import create_engine
from zope.sqlalchemy import ZopeTransactionExtension
import hashlib
import random

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(100), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '#<Group %s>' % self.name


class User(Base):
    """
    Users are authorized to log into the Gateway UI
    There are two different groupd, viewers and admins.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(100), unique=True)
    password = Column(Unicode(100))
    email = Column(Unicode(100))
    group_id = Column(
        Integer,
        ForeignKey('groups.id'))

    group = relation(
        Group,
        primaryjoin=group_id == Group.id)

    def __init__(self,
                 name,
                 password,
                 email,
                 group):
        self.name = name
        if password is not None:
            hash = hashlib.md5(password).hexdigest()
        self.password = hash
        self.email = email
        self.group = group

    def __repr__(self):
        return '#<User %s>' % self.name


class Device(Base):
    """ Devices are Android tablets that can request tokens from the Gateway"""
    __tablename__ = 'devices'
    id = Column(Integer, primary_key=True)
    device_id = Column(Unicode(100), unique=True)
    password = Column(Unicode(100), )

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
    zone = Column(Unicode(256))

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
                 time_zone,
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
        self.time_zone = time_zone

    def __repr__(self):
        return '#<Meter %s>' % self.name

    def get_circuits(self):
        session = DBSession()
        return session.query(Circuit)\
            .filter_by(meter=self).order_by(Circuit.ip_address)

    def get_main_circuit(self):
        session = DBSession()
        return session.query(Circuit).filter_by(meter=self)\
            .filter_by(ip_address='192.168.1.200').first()

    def find_meter_uptime(self):
        """
        cs = # of circuits
        actual = number messages it did receive
        possible = Number of messages it should have receive in the last week
        -> 48 * cs * 7
        (* (/ actual possible) 100)
        """
        now = datetime.now()
        days = 7
        last_week = now - timedelta(days=days)
        session = DBSession()
        log_count = session.query(PrimaryLog)\
            .filter_by(circuit=self.get_main_circuit())\
            .filter(PrimaryLog.meter_time < now)\
            .filter(PrimaryLog.meter_time > last_week).count()
        return int((log_count / (48.0 * days)) * 100)


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

    def get_last_log(self):
        session = DBSession()
        return session.query(PrimaryLog)\
            .filter_by(circuit=self)\
            .order_by(PrimaryLog.meter_time.desc()).first()

    def __repr__(self):
        return '#<Circuit %s>' % self.id


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


class TokenBatch(Base):
    """
    A class that groups tokens based on when they are created
    """
    __tablename__ = "tokenbatch"
    id = Column(Integer, primary_key=True)
    created = Column(DateTime)  # change to date_added

    def __init__(self, created):
        self.created = created

    def __repr__(self):
        return "#<Token Batch %s>" % self.id


class Token(Base):
    """
    """
    __tablename__ = "token"

    id = Column(Integer, primary_key=True)
    created = Column(DateTime)
    token = Column(Numeric)
    value = Column(Numeric)
    state = Column(Unicode)
    batch_id = Column(Integer, ForeignKey('tokenbatch.id'))
    batch = relation(TokenBatch,
                      primaryjoin=batch_id == TokenBatch.id)

    def __init__(self, created, token, batch, value, state):
        self.created = created
        self.token = token
        self.value = value
        self.state = state
        self.batch = batch

    @staticmethod
    def get_random():
        r = int(random.random() * 10 ** 11)
        if r > 10 ** 10: return r
        else: return Token.get_random()


class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True)
    _type = Column('type', Unicode(50))
    __mapper_args__ = {'polymorphic_on': _type}

    start = Column(DateTime)
    end = Column(DateTime)
    state = Column(Boolean)
    circuit_id = Column(Integer, ForeignKey('circuits.id'))
    circuit = relation(Circuit,
                       primaryjoin=circuit_id == Circuit.id)

    def __init__(self, start, circuit, state):
        self.start = start
        self.circuit = circuit
        self.state = state


class Alert(Base):
    """
    Base class for all alerts in the Gateway
    """

    __tablename__ = 'alerts'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    _type = Column('type', Unicode(50))
    __mapper_args__ = {'polymorphic_on': _type}

    meter_id = Column(Integer, ForeignKey('meters.id'))
    meter = relation(Meter, primaryjoin=meter_id == Meter.id)

    circuit_id = Column(Integer, ForeignKey('circuits.id'))
    circuit = relation(Circuit, primaryjoin=circuit_id == Circuit.id)

    origin_message_id = Column(Integer, ForeignKey('message.id'))
    origin_message = relation(Message,
                              primaryjoin=origin_message_id == Message.id)

    consumer_message_id = Column(Integer, ForeignKey('message.id'))
    consumer_message = relation(Message,
                                primaryjoin=consumer_message_id == Message.id)

    def __init__(self, date, meter, circuit, origin_message, consumer_message):
        self.date = date
        self.meter = meter
        self.circuit = circuit
        self.origin_message = origin_message
        self.consumer_message = consumer_message


class UnresponsiveCircuit(Alert):
    """
    An alert that is sent when a circuit fails to report for
    more than 2 hours. Sends an email to the gateway admins and logs
    the event in the UI.
    """
    id = Column(Integer, ForeignKey('alerts.id'), primary_key=True)
    __tablename__ = 'unresponsive_circuit'
    __mapper_args__ = {'polymorphic_identity': 'unresponsive_circuit'}

    last_heard_from = Column(Float)

    def __init__(self, date, meter, circuit, last_head_from):
        Alert.__init__(self,
                       date,
                       meter,
                       circuit=circuit,
                       origin_message=None,
                       consumer_message=None)
        self.last_heard_from = last_head_from


class PowerMax(Alert):
    """
    An alert that gets sent from the meter when a consumer uses to much
    power. A SMS message is sent to the consumer. The event it logged
    in the Gateway UI.
    """
    id = Column(Integer, ForeignKey('alerts.id'), primary_key=True)
    __tablename__ = 'power_max'
    __mapper_args__ = {'polymorphic_identity': 'power_max'}

    def __init__(self, date, meter, circuit, origin_message, consumer_message):
        Alert.__init__(self, date, meter, circuit=circuit,
                       origin_message=origin_message,
                       consumer_message=consumer_message)


class EnergyMax(Alert):
    """
    An alert that is sent when a consumer uses over their daily max.
    A SMS message it sent to the consumer and the event in logged in
    the Gateway UI.
    """
    id = Column(Integer, ForeignKey('alerts.id'), primary_key=True)
    __tablename__ = 'energy_max'
    __mapper_args__ = {'polymorphic_identity': 'energy_max'}

    def __init__(self, date, meter, circuit, origin_message, consumer_message):
        Alert.__init__(self, date, meter, circuit=circuit,
                       origin_message=origin_message,
                       consumer_message=consumer_message)


class LowCredit(Alert):
    """
    An alert when the consumer is running low on credit. A SMS is sent
    to the consumer.
    """
    id = Column(Integer, ForeignKey('alerts.id'), primary_key=True)
    __tablename__ = 'low_credit'
    __mapper_args__ = {'polymorphic_identity': 'low_credit'}

    def __init__(self, date, meter, circuit, origin_message, consumer_message):
        Alert.__init__(self, date, meter, circuit=circuit,
                       origin_message=origin_message,
                       consumer_message=consumer_message)


class NoCredit(Alert):
    """
    """
    id = Column(Integer, ForeignKey('alerts.id'), primary_key=True)
    __tablename__ = 'no_credit'
    __mapper_args__ = {'polymorphic_identity': 'no_credit'}

    def __init__(self, date, meter, circuit, origin_message, consumer_message):
        Alert.__init__(self, date, meter, circuit=circuit,
                       origin_message=origin_message,
                       consumer_message=consumer_message)


class UnresponsiveJob(Alert):
    """
    """
    id = Column(Integer, ForeignKey('alerts.id'), primary_key=True)
    __tablename__ = 'unresponsive_job'
    __mapper_args__ = {'polymorphic_identity': 'unresponsive_job'}

    job_id = Column(Integer, ForeignKey('jobs.id'))
    job = relation(Job, primaryjoin=job_id == Job.id)

    def __init__(self, date, meter, circuit, job):
        Alert.__init__(self,
                       date,
                       meter,
                       circuit=circuit,
                       origin_message=None,
                       consumer_message=None)
        self.job = job


class PowerOn(Alert):
    """
    """
    id = Column(Integer, ForeignKey('alerts.id'), primary_key=True)
    __tablename__ = 'power_on'
    __mapper_args__ = {'polymorphic_identity': 'power_on'}

    def __init__(self, date, meter, origin_message):
        Alert.__init__(self, date, meter, origin_message=origin_message)


class Log(Base):
    """
    Base class for all logs in the gateway.
    """
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True)
    meter_time = Column(DateTime)
    _type = Column('type', Unicode(50))
    __mapper_args__ = {'polymorphic_on': _type}

    def __init__(self, meter_time):
        self.meter_time = meter_time


class PCULog(Log):
    """
    (pcu#<ts>#
    <cumltve-kwh-sol>,
    <cumltve-kwh-bat-charge>,
    <cumltve-kwh-discharge>,
    <BatteryV(V)>,
    <Bat charge>,
    <Bat discharge>,
    <Sol A(A)>,
    <SolarVolt>
    """
    __tablename__ = 'pcu_log'
    __mapper_args__ = {'polymorphic_identity': 'pcu_log'}
    id = Column(Integer, ForeignKey('logs.id'), primary_key=True)
    timestamp = Column(DateTime)  # meter time
    cumulative_khw_solar = Column(Float)
    cumulative_kwh_battery_charge = Column(Float)
    cumulative_kwh_discharge = Column(Float)
    battery_volts = Column(Float)
    battery_charge = Column(Float)
    battery_discharge = Column(Float)
    solar_amps = Column(Float)
    solar_volts = Column(Float)
    meter_id = Column(Integer, ForeignKey('meters.id'))
    meter = relation(Meter, primaryjoin=meter_id == Meter.id)

    def __init__(self,
                 gateway_time,
                 meter_time,
                 cumulative_khw_solar,
                 cumulative_kwh_battery_charge,
                 cumulative_kwh_discharge,
                 battery_volts,
                 battery_charge,
                 battery_discharge,
                 solar_amps,
                 solar_volts,
                 meter):
        Log.__init__(self, gateway_time)
        self.timestamp = meter_time
        self.cumulative_khw_solar = cumulative_khw_solar
        self.cumulative_kwh_battery_charge = cumulative_kwh_battery_charge
        self.cumulative_kwh_discharge = cumulative_kwh_discharge
        self.battery_volts = battery_volts
        self.battery_charge = battery_charge
        self.battery_discharge = battery_discharge
        self.solar_amps = solar_amps
        self.solar_volts = solar_volts
        self.meter = meter


class PrimaryLog(Log):
    __tablename__ = 'primary_log'
    __mapper_args__ = {'polymorphic_identity': 'primary_log'}
    id = Column(Integer, ForeignKey('logs.id'), primary_key=True)
    watthours = Column(Float)
    use_time = Column(Float)
    status = Column(Integer)
    gateway_time = Column(DateTime)
    credit = Column(Float, nullable=True)
    circuit_id = Column(Integer, ForeignKey('circuits.id'))
    circuit = relation(Circuit,
                       primaryjoin=circuit_id == Circuit.id)

    def __init__(self,
                 circuit,
                 gateway_time,
                 meter_time,
                 watthours,
                 use_time,
                 status,
                 credit):

        Log.__init__(self, gateway_time)
        self.circuit = circuit
        self.watthours = watthours
        self.use_time = use_time
        self.credit = credit
        self.meter_time = meter_time
        self.status = status
        self.circuit = circuit


class AddCredit(Job):
    __tablename__ = 'addcredit'
    __mapper_args__ = {'polymorphic_identity': 'addcredit'}

    id = Column(Integer, ForeignKey('jobs.id'), primary_key=True)
    credit = Column(Integer)
    token_id = Column(Integer, ForeignKey('token.id'))
    token = relation(Token, primaryjoin=token_id == Token.id)

    def __init__(self, date, circuit, state, credit, token):
        Job.__init__(self, date, circuit, state)
        self.credit = credit
        self.token = token

    def __repr__(self):
        return '(job=cr&jobid=%s&cid=%s&amt=%s)' \
            % (self.id, self.circuit.ip_address, float(self.credit))


class TurnOff(Job):
    __tablename__ = 'turnoff'
    __mapper_args__ = {'polymorphic_identity': 'turnoff'}

    id = Column(Integer, ForeignKey('jobs.id'), primary_key=True)

    def __init__(self, date, circuit, state):
        Job.__init__(self, date, circuit, state)

    def __repr__(self):
        return '(job=coff&jobid=%s&cid=%s)' \
            % (self.id, self.circuit.ip_address)


class TurnOn(Job):
    __tablename__ = 'turnon'
    __mapper_args__ = {'polymorphic_identity': 'turnon'}

    id = Column(Integer, ForeignKey('jobs.id'), primary_key=True)

    def __init__(self, date, circuit, state):
        Job.__init__(self, date, circuit, state)

    def __repr__(self):
        return '(job=con&jobid=%s&cid=%s)' % (self.id, self.circuit.ip_address)


class Mping(Job):
    """ Job that allows the admin to 'ping' a meter"""
    __tablename__ = 'mping'
    __mapper_args__ = {'polymorphic_identity': 'mping'}

    id = Column(Integer, ForeignKey('jobs.id'), primary_key=True)

    def __init__(self, date, meter, state):
        Job.__init__(self, date, self.getMain(meter), state)

    def getMain(self, meter):
        return meter.get_circuits()[0]

    def __repr__(self):
        return '(job=mping&jobid=%s)' % self.id


class Cping(Job):
    """ Job that allows the admin to 'ping' a meter"""
    __tablename__ = 'cping'
    __mapper_args__ = {'polymorphic_identity': 'cping'}

    id = Column(Integer, ForeignKey('jobs.id'), primary_key=True)

    def __init__(self, date, circuit, state):
        Job.__init__(self, date, circuit, state)

    def __repr__(self):
        return '(job=cping&jobid=%s&cid=%s)' % (self.id,
                                               self.circuit.ip_address)


class JobMessage(Message):
    """
    A class that repsents the text message for a job.
    """
    __tablename__ = 'job_message'
    __mapper_args__ = {'polymorphic_identity': 'job_message'}
    id = Column(Integer,
                ForeignKey('message.id'), primary_key=True)
    job_id = Column(Integer, ForeignKey('jobs.id'))
    job = relation(Job,
                   primaryjoin=job_id == Job.id)
    incoming = Column(Unicode)
    text = Column(Unicode)

    def __init__(self, job, incoming=None):
        Message.__init__(self, job.circuit.meter.phone)
        self.job = job
        self.incoming = incoming
        self.text = job.__str__()


def initialize_sql(settings, echo=False):
    engine = create_engine(settings, echo=echo)
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    return engine


def load_testing_sql(settings, echo=False):
    engine = create_engine(settings, echo=echo)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)
