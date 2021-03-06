# *****************************************************************************
#   Copyright 2004-2008 Steve Menard
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#          http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# *****************************************************************************
from jpype import JException, java, JProxy, JPackage
import traceback
import common


def throwIOException():
    raise java.io.IOException("Test throw")


def throwByJavaException():
    JPackage('jpype').exc.ExceptionTest.throwIOException()


class ExceptionTestCase(common.JPypeTestCase):
    def testExceptionThrown(self):
        try:
            self.jpype.exc.ExceptionTest.throwRuntime()
            self.fail()
        except JException as ex:
            self.assertIs(type(ex), java.lang.RuntimeException)
            self.assertEqual('Foo', ex.message())
            trace = ex.stacktrace()
            self.assertTrue(str(trace).startswith(
                'java.lang.RuntimeException: Foo'))

    def testExceptionByJavaClass(self):
        try:
            self.jpype.exc.ExceptionTest.throwRuntime()
            self.fail()
        except JException(java.lang.RuntimeException) as ex:
            self.assertIs(type(ex), java.lang.RuntimeException)
            self.assertEqual('Foo', ex.message())
            trace = ex.stacktrace()
            self.assertTrue(str(trace).startswith(
                'java.lang.RuntimeException: Foo'))

    def testThrowException(self):
        d = {"throwIOException": throwIOException, }
        p = JProxy(self.jpype.exc.ExceptionThrower, dict=d)
        self.assertTrue(self.jpype.exc.ExceptionTest.delegateThrow(p))

    def testThrowException3(self):
        d = {"throwIOException": throwByJavaException, }
        p = JProxy(self.jpype.exc.ExceptionThrower, dict=d)

        self.assertTrue(self.jpype.exc.ExceptionTest.delegateThrow(p))

    def testExceptionPYEXCName(self):
        e = self.jpype.exc.ChildTestException()
        name = "jpype.exc.ChildTestException"
        self.assertEqual(name, e.__name__)

    def testExceptionInstanceof(self):
        e = self.jpype.exc.ChildTestException()
        self.assertIsInstance(e, self.jpype.exc.ParentTestException)

    def testExceptionPYEXCInstanceof(self):
        e = self.jpype.exc.ChildTestException
        self.assertTrue(issubclass(e, self.jpype.exc.ParentTestException))

    def testThrowChildExceptionFromCatchJExceptionParentClass(self):
        try:
            self.jpype.exc.ExceptionTest.throwChildTestException()
            self.fail()
        except JException(self.jpype.exc.ParentTestException) as ex:
            self.assertIsInstance(ex, self.jpype.exc.ChildTestException)
