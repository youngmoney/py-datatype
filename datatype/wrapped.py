from datatype import Wrapper

import datetime


class DateTime(metaclass=Wrapper):
    value_type = datetime.datetime

    def __init__(self, s):
        self._value = datetime.datetime.fromisoformat(s)

    def __repr__(self):
        return self._value.isoformat()
