from unittest import TestCase

from main import timestamp_to_date


class Test(TestCase):
    def test_timestamp_to_date(self):
        self.assertEqual(timestamp_to_date('1593666000000'), '02-07')
