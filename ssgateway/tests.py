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

    def test_assert_session(self):
        from sqlalchemy.orm.session import Session
        session = self.session
        self.assertIsInstance(session, Session)

    def test_log_creation(self):
        from ssgateway.models import Log
        log = Log(datetime.now())
        self.assertIsInstance(log, Log)
        self.session.add(log)
        self.session.commit()

    def test_job_creation(self):
        from ssgateway.models import Job
        j1 = Job(datetime.now(), self.get_circuit(), True)
        self.session.add(j1)
        self.session.commit()
        j2 = self.session.query(Job).first()
        self.assertEqual(j1, j2)

    def get_message(self):
        from ssgateway.models import Message
        return Message(datetime.now(), u'This is a test message', 18182124554)

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
        return m1

    def test_circuit_creation(self):
        c1 = self.get_circuit()
        self.session.add(c1)

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
