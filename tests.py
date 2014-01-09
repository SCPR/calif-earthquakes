# -*- coding: utf-8 -*-
import os, logging, requests, time, datetime, calendar
import pytz
from pytz import timezone
from datetime import tzinfo, date
from earthquakes import app, db
from earthquakes import settings_development
from earthquakes.models import Earthquake, NearestCity
import unittest, tempfile, types

logging.basicConfig(format='\033[1;36m%(levelname)s:\033[0;37m %(message)s', level=logging.DEBUG)

# Tests
#Request to API returns 200 status.
#Data response contains actual data/is not null.
#Desired keys are present and have values.
#Data that will be written to database are in the expected data types.
#Table exists in the database.

test_url = settings_development.config_settings['GT_2.5_PAST_DAY']
details_url = 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/detail/nc72138821.geojson'
nearest_cities_url = 'http://earthquake.usgs.gov/product/nearby-cities/nc72138821/us/1389226110774/nearby-cities.json'

class TestCase(unittest.TestCase):

    def setUp(self):
        ''' creates a new test client '''
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_index_page(self):
        ''' retrieve index page '''
        test_response = self.app.get('/')
        assert test_response

    def test_usgs_api_response(self):
        ''' test response from usgs api '''
        test_response = requests.get(test_url)
        self.assertEqual(200, test_response.status_code)

        test_json_data = test_response.json()
        self.assertIsNotNone(test_json_data)

        for item in test_json_data['features']:
            details_link = item['properties']['detail']
            self.assertIsNotNone(details_link)

    def test_usgs_details_url(self):
        ''' test response from usgs api for details json '''
        test_response = requests.get(details_url)
        self.assertEqual(200, test_response.status_code)

        test_json_data = test_response.json()
        self.assertIsNotNone(test_json_data)

        nearest_cities_url = test_json_data['properties']['products']['nearby-cities'][0]['contents']['nearby-cities.json']['url']
        self.assertIsNotNone(nearest_cities_url)

    def test_usgs_nearest_cities_url(self):
        ''' test response from usgs api for details json '''
        test_response = requests.get(nearest_cities_url)
        self.assertEqual(200, test_response.status_code)

        test_json_data = test_response.json()
        self.assertIsNotNone(test_json_data)

    def test_append_city_to_list(self):
        ''' test_append_city_to_list '''
        list_of_nearest_cities = [
            {u'distance': 31, u'direction': u'NE', u'name': u'Soledad, California', u'longitude': -121.32632, u'latitude': 36.42469, u'population': 25738},
            {u'distance': 36, u'direction': u'NNE', u'name': u'Greenfield, California', u'longitude': -121.24381, u'latitude': 36.3208, u'population': 16330},
            {u'distance': 39, u'direction': u'SE', u'name': u'Hollister, California', u'longitude': -121.4016, u'latitude': 36.85245, u'population': 34928},
            {u'distance': 45, u'direction': u'N', u'name': u'King City, California', u'longitude': -121.12603, u'latitude': 36.21274, u'population': 12874},
            {u'distance': 221, u'direction': u'S', u'name': u'Sacramento, California', u'longitude': -121.4944, u'latitude': 38.58157, u'population': 466488}
        ]
        self.assertIsNotNone(list_of_nearest_cities)
        container_list = []
        for nearby_city in list_of_nearest_cities:
            city = NearestCity(
                id = None,
                distance = nearby_city['distance'],
                direction = nearby_city['direction'],
                name = nearby_city['name'],
                latitude = nearby_city['latitude'],
                longitude = nearby_city['longitude'],
                population = nearby_city['population'],
                earthquake_id = None
            )
            self.assertIsNotNone(city)
            container_list.append(city)
        self.assertIsNotNone(container_list)

    def test_parsing_for_desired_string(self):
        ''' test_parsing_for_desired_string '''
        list_of_places = [
            '35km N of Road Town, British Virgin Islands',
            '11km NNW of Jones, Oklahoma',
            '10km WNW of Cobb, California'
        ]
        for place in list_of_places:
            if 'California' in place:
                test_data = True
                self.assertTrue(test_data)
            else:
                test_data = False
                self.assertFalse(test_data)

    def test_for_date_formatting(self):
        ''' test_for_date_formatting '''
        # terminal shows datetime object as local time
        # via http://www.epochconverter.com/ - 2013-12-07 6:10:23.060000
        # local: 2013-12-07 10:10:23.060000

        # the date/time from the api is a unix timestamp
        date_time = 1386439823060

        # the timezone from the api offset from UTC in minutes at the event epicenter
        tz = -360

        # convert the unix timestamp to utc datetime object
        test_data = isinstance(datetime.datetime.utcfromtimestamp(date_time/1e3), datetime.datetime)
        self.assertTrue(test_data)

    '''
    def test_comparison_against_db(self):
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
    '''

    '''
    def test write to db(self):
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