#!/usr/bin/env python

from runtest import TestBase
import subprocess as sp

TDIR='xxx'

class TestCase(TestBase):
    def __init__(self):
        TestBase.__init__(self, 'allocfree', """
# DURATION    TID     FUNCTION
            [ 4629] | alloc3() {
   4.671 us [ 4629] |   alloc4();
   4.999 us [ 4629] | } /* alloc3 */
            [ 4629] | free1() {
            [ 4629] |   free2() {
            [ 4629] |     free5() {
   1.057 us [ 4629] |       free();
   1.563 us [ 4629] |     } /* free5 */
   2.323 us [ 4629] |   } /* free2 */
   2.580 us [ 4629] | } /* free1 */
""")

    def pre(self):
        record_cmd = '%s record -d %s %s' % (TestBase.ftrace, TDIR, 't-allocfree')
        sp.call(record_cmd.split())
        return TestBase.TEST_SUCCESS

    def runcmd(self):
        return '%s replay -d %s -F alloc3 -D2 -F "free[15]"' % (TestBase.ftrace, TDIR)

    def post(self, ret):
        sp.call(['rm', '-rf', TDIR])
        return ret

    def sort(self, output):
        """ This function post-processes output of the test to be compared .
            It ignores blank and comment (#) lines and remaining functions.  """
        result = []
        for ln in output.split('\n'):
            # ignore blank lines and comments
            if ln.strip() == '' or ln.startswith('#'):
                continue
            func = ln.split('|', 1)[-1]
            result.append(func)

        return '\n'.join(result)
