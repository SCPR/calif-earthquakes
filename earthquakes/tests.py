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





    '''
    "mimics django's get or create function"
    def get_or_create(self, session, model, **kwargs):
        instance = session.query(model).filter_by(**kwargs).first()
        if instance:
            return instance
        else:
            instance = model(**kwargs)
            session.add(instance)
            session.commit()
            return instance

    "tests writing dates to the database"
    def run(self):

        # terminal shows datetime object as local time
        # via http://www.epochconverter.com/ - 2013-12-07 6:10:23.060000
        # local: 2013-12-07 10:10:23.060000

        # the date/time from the api is a unix timestamp
        date_time = 1386439823060

        # the timezone from the api offset from UTC in minutes at the event epicenter
        tz = -360

        # convert the unix timestamp to utc datetime object
        test = datetime.datetime.utcfromtimestamp(date_time/1e3)
        logging.debug(test)

        thisDate = self.get_or_create(db.session, Experiment,
            id = None,
            name = 'test',
            date_time = test
        )

    "mimics django's get or create function"
    def run(self):
        comparison_slug = 'what-slug'
        comparison_name = 'new name'
        instance = Experiment.query.filter_by(slug=comparison_slug).first()
        if instance is None:
            logging.debug('record doesnt exist')
            thisRecord = Experiment(
                id = None,
                slug = comparison_slug,
                name = comparison_name,
                date_time = datetime.datetime.utcfromtimestamp(1386439823060/1e3)
            )
            db.session.add(thisRecord)
        else:
            logging.debug('record exists so im comparing')
            if instance.name == comparison_name:
                logging.debug('record exists and doesnt need to be updated')
                pass
            else:
                logging.debug('record exists and will be updated')
                instance.name = 'new name'
        db.session.commit()

    def run(self):

        city = NearestCity(
            id = None,
            distance = 46,
            direction = "SSE",
            name = "Lone Pine, California",
            latitude = 36.60604,
            longitude = -118.06287,
            population = 2035,
            earthquake_id = None
        )

        quake = Earthquake(
            id = None,
            primary_slug = 'test',
            mag = 4.5,
            place = '11km NNW of Jones, Oklahoma',
            title = 'M4.5  - 11km NNW of Jones, Oklahoma',
            date_time = datetime.datetime.utcfromtimestamp(1386439823060/1e3),
            date_time_raw = 1386439823060,
            updated = datetime.datetime.utcfromtimestamp(1386710939478/1e3),
            updated_raw = 1386710939478,
            tz = -360,
            url = 'http://earthquake.usgs.gov/earthquakes/eventpage/usb000ldeh',
            felt = 3638,
            cdi = 5.7,
            mmi = 4.47,
            alert = 'green',
            status = 'reviewed',
            tsunami = None,
            sig = 882,
            resource_type = 'earthquake',
            latitude = 35.6627,
            longitude = -97.3261,
            depth = 5,
            net = None,
            code = None,
            ids = None,
            sources = None,
            nst = None,
            dmin = None,
            rms = None,
            gap = None,
            magType = None,
            instance_type = None,
            nearest_cities_url = 'http://earthquake.usgs.gov/product/nearby-cities/ci11410562/us/1388963699219/nearby-cities.json',
            nearest_cities=[city]
        )

        db.session.add(quake)
        db.session.add(city)
        db.session.commit()
    '''





if __name__ == '__main__':
    unittest.main()