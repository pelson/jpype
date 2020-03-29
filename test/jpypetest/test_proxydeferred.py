import jpype
from jpype.types import *
from jpype import JImplements, JOverride
import common
import subrun
import os
import sys
import unittest

@subrun.TestCase(individual=True)
class ProxyDeferredCase(unittest.TestCase):
    def setUp(self):
        self.jvmpath = jpype.getDefaultJVMPath()

    def testCorrect(self):
        @JImplements("java.lang.Comparable", deferred=True)
        class MyComparison(object):
            @JOverride
            def compareTo(self, a):
                return 0
        jpype.startJVM(convertStrings=False)
        mc = MyComparison()
        jo = JObject(mc)
        self.assertEqual(jo.compareTo(JString("a")), 0)

    def testBadOverride(self):
        @JImplements("java.lang.Comparable", deferred=True)
        class MyComparison(object):
            def compareTo(self, a):
                return 0
        jpype.startJVM(convertStrings=False)
        with self.assertRaises(NotImplementedError):
            mc = MyComparison()

    def testBadInterface(self):
        @JImplements("java.lang.Comparible", deferred=True)
        class MyComparison(object):
            @JOverride
            def compareTo(self, a):
                return 0
        jpype.startJVM(convertStrings=False)
        with self.assertRaises(TypeError):
            mc = MyComparison()

    def testNotDeferred(self):
        with self.assertRaises(RuntimeError):
            @JImplements("java.lang.Comparable")
            class MyComparison(object):
                def compareTo(self, a):
                    return 0


