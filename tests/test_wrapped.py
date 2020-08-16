import unittest

from datatype.wrapped import DateTime

from datetime import datetime


class TestDateTime(unittest.TestCase):
    def test_datetime(self):
        dt = datetime.now()
        self.assertEqual(DateTime(dt), dt)
        self.assertEqual(DateTime(dt).value(), dt)

        self.assertEqual(DateTime(dt.isoformat()), dt)

        self.assertEqual(str(DateTime(dt.isoformat())), dt.isoformat())
        self.assertEqual(repr(DateTime(dt.isoformat())), dt.isoformat())

        dtt = DateTime(dt)
        self.assertEqual(DateTime(dtt), dtt)
