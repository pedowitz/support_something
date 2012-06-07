import os
import unittest
import tempfile

import supportsomething


class SupportsomethingTestCase(unittest.TestCase):

    def setUp(self):
        
        self.app = supportsomething.create_app('Testing').test_client()
        

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()