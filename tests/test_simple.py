import unittest

import datatype


class TestOption(unittest.TestCase):
    class Opt(metaclass=datatype.Option):
        opt1 = 0
        opt2 = 1

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
