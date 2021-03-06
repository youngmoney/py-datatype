import unittest

import datatype


class TestOption(unittest.TestCase):
    class Opt(metaclass=datatype.Option):
        opt1 = 0
        opt2 = 1
        optstring = "hello"

    def test_parse(self):
        self.assertEqual(self.Opt(self.Opt.opt1), self.Opt.opt1)
        self.assertEqual(self.Opt("opt1"), self.Opt.opt1)
        self.assertEqual(self.Opt("OPT1"), self.Opt.opt1)
        self.assertEqual(self.Opt(0), self.Opt.opt1)
        self.assertEqual(self.Opt(self.Opt(self.Opt.opt1)), self.Opt.opt1)

    def test_equal(self):
        self.assertEqual(self.Opt.opt1, 0)
        self.assertEqual(self.Opt.opt1, "OPT1")
        self.assertEqual(self.Opt.opt1, "opt1")

        self.assertEqual(self.Opt.opt2, 1)
        self.assertEqual(self.Opt.opt2, "OPT2")
        self.assertEqual(self.Opt.opt2, "opt2")

        self.assertNotEqual(self.Opt.opt1, self.Opt.opt2)
        self.assertNotEqual(self.Opt.opt1, 1)
        self.assertNotEqual(self.Opt.opt1, "opt2")
        self.assertNotEqual(self.Opt.opt1, "OPT2")

    def test_definition(self):
        self.assertEqual(self.Opt.opt1.definition(), 0)
        self.assertEqual(self.Opt.opt2.definition(), 1)
        self.assertEqual(self.Opt.optstring.definition(), "hello")


class TestObject(unittest.TestCase):
    class Obj(metaclass=datatype.Object):
        datatype_a = int
        datatype_b = str
        datatype_c = [int]
        datatype_d = {str: int}
        datatype_recurse = {str: datatype.Object.Self}

        def __init__(self, b="hello", c=[1, 2]):
            if self.a is not None:
                self.a += 1

    class SimpleObj(metaclass=datatype.Object):
        datatype_a = int

    def test_a(self):
        o = self.Obj({"a": 1})
        self.assertEqual(o.a, 2)
        self.assertEqual(o.b, "hello")
        self.assertEqual(o.c, [1, 2])
        self.assertEqual(o.d, None)
        self.assertEqual(o.recurse, None)

    def test_a_cast(self):
        o = self.Obj({"a": "1"})
        self.assertEqual(o.a, 2)
        self.assertEqual(o.b, "hello")
        self.assertEqual(o.c, [1, 2])
        self.assertEqual(o.d, None)
        self.assertEqual(o.recurse, None)

    def test_b(self):
        o = self.Obj({"b": 1})
        self.assertEqual(o.a, None)
        self.assertEqual(o.b, "1")
        self.assertEqual(o.c, [1, 2])
        self.assertEqual(o.d, None)
        self.assertEqual(o.recurse, None)

    def test_c_item_cast(self):
        o = self.Obj({"c": ["1"]})
        self.assertEqual(o.a, None)
        self.assertEqual(o.b, "hello")
        self.assertEqual(o.c, [1])
        self.assertEqual(o.d, None)
        self.assertEqual(o.recurse, None)

    def test_d(self):
        o = self.Obj({"d": {"1": 1}})
        self.assertEqual(o.a, None)
        self.assertEqual(o.b, "hello")
        self.assertEqual(o.c, [1, 2])
        self.assertEqual(o.d, {"1": 1})
        self.assertEqual(o.recurse, None)

    def test_d_cast(self):
        o = self.Obj({"d": {1: "1"}})
        self.assertEqual(o.a, None)
        self.assertEqual(o.b, "hello")
        self.assertEqual(o.c, [1, 2])
        self.assertEqual(o.d, {"1": 1})
        self.assertEqual(o.recurse, None)

    def test_recurse(self):
        o = self.Obj({"recurse": {"this": {"a": 10}}})
        self.assertEqual(o.a, None)
        self.assertEqual(o.b, "hello")
        self.assertEqual(o.c, [1, 2])
        self.assertEqual(o.d, None)
        self.assertNotEqual(o.recurse, None)

        self.assertEqual(o.recurse["this"].a, 11)
        self.assertEqual(o.recurse["this"].b, "hello")
        self.assertEqual(o.recurse["this"].c, [1, 2])
        self.assertEqual(o.recurse["this"].d, None)
        self.assertEqual(o.recurse["this"].recurse, None)

    def test_equality(self):
        o = self.Obj({"d": {1: "1"}, "b": 2, "recurse": {"this": {"a": 10}}})
        same = self.Obj({"d": {1: "1"}, "b": 2, "recurse": {"this": {"a": 10}}})
        different = self.Obj({"d": {1: "1"}, "b": 2})
        self.assertEqual(o, same)
        self.assertNotEqual(o, different)

    def test_equality_different_class(self):
        simple = self.Obj(a=0, b=None, c=None)
        different_type = self.SimpleObj(a=1)
        self.assertEqual(simple, different_type)
        self.assertEqual(simple, different_type.datatype_Object())


class TestWrapper(unittest.TestCase):
    class Obj(metaclass=datatype.Object):
        class IntWrapper(metaclass=datatype.Wrapper):
            value_type = int

            def __init__(self, s):
                self._value = int(s)

            def __repr__(self):
                return str(self._value)

        datatype_a = IntWrapper

    def test_from_string(self):
        o = self.Obj()
        o.a = "10"
        self.assertEqual(o.a, 10)

    def test_from_object(self):
        o = self.Obj()
        o.a = self.Obj.IntWrapper(10)
        self.assertEqual(o.a, 10)

    def test_from_value(self):
        o = self.Obj()
        o.a = 10
        self.assertEqual(o.a, 10)

    def test_to_dict(self):
        o = self.Obj(a=10)
        self.assertEqual(o.datatype_Object(), {"a": "10"})

    def test_eq(self):
        o = self.Obj(a=10)
        self.assertEqual(self.Obj.IntWrapper("10"), 10)
        self.assertEqual(self.Obj(o.datatype_Object()).a, o.a)
