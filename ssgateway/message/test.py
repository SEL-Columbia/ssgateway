import unittest
from ssgateway.message import main


class UnitxTests(unittest.TestCase):
    """
    Tests for core functions of switchboar
    """
    def setUp(self):
        """
        """
    def _get_config(self):
        from yaml import load
        return load(open('routes.yaml'))

    def _get_raw_message(self):
        return 'address=18182124554&body=bal.12345'

    def _get_parsed(self):
        from ssgateway.message import initial_parse
        return initial_parse(self._get_raw_message())


    def test_initial_parse(self):
        m = self._get_parsed()
        self.assertTrue(isinstance(m, dict))
        self.assertEqual(m['body'], 'bal.12345')
        self.assertEqual(m['address'], '18182124554')

    def test_classify(self):
        from ssgateway.message import classify
        cm = classify(self._get_parsed(), self._get_config())
        self.assertEqual(cm['classification']['name'],
                         'consummer-message-alphabetical')


if __name__ == '__main__':
    unittest.main()
