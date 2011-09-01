import unittest
from datetime import datetime


class DatabaseTest(unittest.TestCase):

    def setUp(self):
        from ssgateway.models import load_testing_sql
        self.session = load_testing_sql('sqlite:///:memory:')()

    def get_account(self):
        from ssgateway.models import Account
        return Account('ivan willig', 8182124554, 'en')

    def get_meter(self):
        from ssgateway.models import Meter
        return Meter(u'test',
                     123456,
                     u'New York city',
                     True,
                     datetime.now(),
                     100,
                     100)

    def get_circuit(self):
        from ssgateway.models import Circuit
        meter = self.get_meter()
        a = self.get_account()
        return Circuit(meter,
                       a,
                       datetime.now(),
                       Circuit.get_pin(),
                       100,
                       100,
                       u'19.1.2.1',
                       True,
                       100)

    def get_message(self):
        from ssgateway.models import Message
        return Message(datetime.now(), u'This is a test message', 18182124554)

    def get_group(self):
        from ssgateway.models import Group
        return Group('admin')

    def test_assert_session(self):
        from sqlalchemy.orm.session import Session
        session = self.session
        self.assertTrue(isinstance(session, Session))

    def test_log_creation(self):
        from ssgateway.models import Log
        log = Log(datetime.now())
        self.assertTrue(isinstance(log, Log))
        self.session.add(log)
        self.session.commit()

    def test_group_creation(self):
        from ssgateway.models import Group
        g1 = self.get_group()
        self.session.add(g1)
        g2 = self.session.query(Group).first()
        self.assertEqual(g1, g2)

    def test_user_creation(self):
        from ssgateway.models import User
        u1 = User('ivan',
                  'password',
                  'iwillig@gmail.com',
                  True,
                  self.get_group())
        self.session.add(u1)
        u2 = self.session.query(User).first()
        self.assertEqual(u1, u2)

    def test_device_creation(self):
        from ssgateway.models import Device
        d1 = Device('id', 'password')
        self.session.add(d1)
        d2 = self.session.query(Device).first()
        self.assertEqual(d1, d2)

    def test_time_zone(self):
        from ssgateway.models import TimeZone
        t1 = TimeZone('EDT')
        self.session.add(t1)
        t2 = self.session.query(TimeZone).first()
        self.assertEqual(t1, t2)

    def test_job_creation(self):
        from ssgateway.models import Job
        j1 = Job(datetime.now(), self.get_circuit(), True)
        self.session.add(j1)
        self.session.commit()
        j2 = self.session.query(Job).first()
        self.assertEqual(j1, j2)

    def test_message_creation(self):
        from ssgateway.models import Message
        m1 = self.get_message()
        self.session.add(m1)
        m2 = self.session.query(Message).first()
        self.assertEqual(m1, m2)

    def test_meter_creation(self):
        from ssgateway.models import Meter
        m1 = self.get_meter()
        self.session.add(m1)
        m2 = self.session.query(Meter).first()
        self.assertEqual(m1, m2)

    def test_account_creation(self):
        from ssgateway.models import Account
        a1 = self.get_account()
        self.session.add(a1)
        a2 = self.session.query(Account).first()
        self.assertEqual(a1, a2)

    def test_circuit_creation(self):
        from ssgateway.models import Circuit
        c1 = self.get_circuit()
        self.session.add(c1)
        c2 = self.session.query(Circuit).first()
        self.assertEqual(c1, c2)

    def test_pcu_log(self):
        from ssgateway.models import PCULog
        m = self.get_meter()
        l1 = PCULog(
            datetime.now(),
            datetime.now(),
            10.00,
            10.00,
            10.00,
            10.00,
            10.00,
            10.00,
            10.00,
            10.00,
            m)
        self.session.add(l1)

    def test_primary_log(self):
        from ssgateway.models import PrimaryLog
        pl = PrimaryLog(
            self.get_circuit(), datetime.now(), datetime.now(),
            10, 10, 10, True)
        self.session.add(pl)

    def test_alert_creation(self):
        from ssgateway.models import Alert
        meter = self.get_meter()
        circuit = self.get_circuit()
        message = self.get_message()
        a1 = Alert(datetime.now(), meter, circuit, message, message)
        self.session.add(a1)
        a2 = self.session.query(Alert).first()
        self.assertEqual(a1, a2)
