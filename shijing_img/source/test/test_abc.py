__author__ = 'wenjusun'

import os
import sys
# print "----------%s" % type(os.path.pardir(os.path.pardir(os.path.abspath(__file__))))
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import unittest

class TestStringMethods(unittest.TestCase):

    def setUp(self):
        print "I am setup."

    def tearDown(self):
        print "I am tear down."

    # @unittest.skip()
    def test_upper(self):
        print "1"
        self.assertEquals('A','a'.upper())

    def test_strip(self):
        print "2"
        self.assertEqual('A',' A '.strip())
        # foo.meow()


if __name__ == '__main__':
    print
    # unittest.main()

    suite = unittest.TestLoader().loadTestsFromTestCase(TestStringMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
