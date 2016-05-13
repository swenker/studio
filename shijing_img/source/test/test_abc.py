__author__ = 'wenjusun'

import os
import sys
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print project_root
sys.path.append(project_root)


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
        import wshelper
        print wshelper.config

    def test_strip(self):
        print "2"
        self.assertEqual('A',' A '.strip())

        # foo.meow()


if __name__ == '__main__':
    # unittest.main()

    suite = unittest.TestLoader().loadTestsFromTestCase(TestStringMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
