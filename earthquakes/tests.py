# -*- coding: utf-8 -*-
import os, logging
import __init__
import unittest
import tempfile
import config
import requests
import types

logging.basicConfig(level=logging.DEBUG)

# Tests
#Request to API returns 200 status.
#Data response contains actual data/is not null.
#Desired keys are present and have values.
#Data that will be written to database are in the expected data types.
#Table exists in the database.

test_url = config.config_settings['month_sig']

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
        test_response = requests.get(test_url)
        self.assertEqual(200, test_response.status_code)

    def test_usgs_api_response_length(self):
        ''' test that data returned is not none '''
        test_response = requests.get(test_url)
        self.assertIsNotNone(test_response.text)

    def test_for_usgs_api_details_link(self):
        ''' test that data returned is not none '''
        test_response = requests.get(test_url)
        test_response = test_response.json()
        for item in test_response['features']:
            usgs_details_link = item['properties']['detail']
            self.assertIsNotNone(usgs_details_link)

    def test_for_desired_string(self):
        ''' test that data returned is not none '''
        test_response = '11km NNW of Jones, Oklahoma'
        if 'Oklahoma' in test_response:
            assert test_response
        else:
            raise Exception

if __name__ == '__main__':
    unittest.main()