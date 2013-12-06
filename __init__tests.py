import os, logging
import __init__
import unittest
import tempfile

logging.basicConfig(level=logging.DEBUG)

class TestCase(unittest.TestCase):
    def setUp(self):
        ''' creates a new test client '''
        __init__.app.config['TESTING'] = True
        self.app = __init__.app.test_client()

    def test_index_page(self):
        ''' retrieve index page '''
        test_response = self.app.get('/')
        assert test_response

if __name__ == '__main__':
    unittest.main()