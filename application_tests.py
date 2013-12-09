# -*- coding: utf-8 -*-
import os, logging
import __init__
import unittest
import tempfile
import config
import requests
import types

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

    def test_usgs_api_response(self):
        ''' test response from usgs api '''
        test_response = requests.get(config.config_settings['seven_days_m4.5'])
        self.assertEqual(200, test_response.status_code)

    def test_usgs_api_list(self):
        ''' test response from usgs api '''
        test_response = requests.get(config.config_settings['seven_days_m4.5'])
        test_data = test_response.json()
        test_earthquakes = test_data['features']
        assert test_earthquakes

if __name__ == '__main__':
    unittest.main()