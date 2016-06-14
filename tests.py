# -*- coding: utf-8 -*-
from earthquakes import app, db
# from earthquakes import settings_production
from earthquakes.models import Earthquake, NearestCity
import os
import logging
import time
import datetime
import calendar
import pytz
from pytz import timezone
from datetime import tzinfo, date
import unittest
import tempfile
import types
import requests
# from requests.packages.urllib3.util.retry import Retry
# from requests.adapters import HTTPAdapter

logger = logging.getLogger("root")
logging.basicConfig(
    format="\033[1;36m%(levelname)s: %(filename)s (def %(funcName)s %(lineno)s): \033[1;37m %(message)s",
    level=logging.DEBUG
)

logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

class TestCase(unittest.TestCase):

    request_url = "http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson"
    details_url = "http://earthquake.usgs.gov/earthquakes/feed/v1.0/detail/nc72138821.geojson"
    cities_url = "http://earthquake.usgs.gov/product/nearby-cities/nc72138821/us/1389226110774/nearby-cities.json"

    def setUp(self):
        """
        creates a new test client
        """
        app.config["TESTING"] = True
        self.app = app.test_client()

    def test_a_download_chain(self):
        """
        initiate a series of functions
        """
        self.Test_get_usgs_api_response(self.request_url)
        self.Test_usgs_details_url_present(self.request_url)
        self.Test_usgs_cities_url_present(self.request_url)

    def Test_get_usgs_api_response(self, request_url):
        """
        test response from usgs api
        """
        response = requests.get(request_url)
        response.raise_for_status()
        self.assertEqual(200, response.status_code)
        response_data = response.json()
        self.assertIsNotNone(response_data)

    def Test_usgs_details_url_present(self, request_url):
        """
        test response from usgs api for details json
        """
        response = requests.get(request_url)
        response.raise_for_status()
        self.assertEqual(200, response.status_code)
        response_data = response.json()
        self.assertIsNotNone(response_data)
        for item in response_data["features"]:
            details = item["properties"]["detail"]
            self.assertIsNotNone(details)

    def Test_usgs_cities_url_present(self, request_url):
        """
        test response from usgs api for details json
        """
        response = requests.get(request_url)
        response.raise_for_status()
        self.assertEqual(200, response.status_code)
        response_data = response.json()
        self.assertIsNotNone(response_data)
        for item in response_data["features"]:
            details_url = item["properties"]["detail"]
            self.assertIsNotNone(details_url)
            details = requests.get(details_url)
            details.raise_for_status()
            self.assertEqual(200, details.status_code)
            details_data = details.json()
            self.assertIsNotNone(details_data)
            nearest_cities_url = details_data["properties"]["products"][
                "nearby-cities"][0]["contents"]["nearby-cities.json"]["url"]
            self.assertIsNotNone(nearest_cities_url)

    def test_append_city_to_list(self):
        """
        test_append_city_to_list
        """
        list_of_nearest_cities = [
            {u"distance": 31, u"direction": u"NE", u"name": u"Soledad, California",
                u"longitude": -121.32632, u"latitude": 36.42469, u"population": 25738},
            {u"distance": 36, u"direction": u"NNE", u"name": u"Greenfield, California",
                u"longitude": -121.24381, u"latitude": 36.3208, u"population": 16330},
            {u"distance": 39, u"direction": u"SE", u"name": u"Hollister, California",
                u"longitude": -121.4016, u"latitude": 36.85245, u"population": 34928},
            {u"distance": 45, u"direction": u"N", u"name": u"King City, California",
                u"longitude": -121.12603, u"latitude": 36.21274, u"population": 12874},
            {u"distance": 221, u"direction": u"S", u"name": u"Sacramento, California",
                u"longitude": -121.4944, u"latitude": 38.58157, u"population": 466488}
        ]
        self.assertIsNotNone(list_of_nearest_cities)
        container_list = []
        for nearby_city in list_of_nearest_cities:
            city = NearestCity(
                id=None,
                distance=nearby_city["distance"],
                direction=nearby_city["direction"],
                name=nearby_city["name"],
                latitude=nearby_city["latitude"],
                longitude=nearby_city["longitude"],
                population=nearby_city["population"],
                earthquake_id=None
            )
            self.assertIsNotNone(city)
            container_list.append(city)
        self.assertIsNotNone(container_list)

    def test_parsing_for_desired_string(self):
        """
        test_parsing_for_desired_string
        """
        list_of_places = [
            "35km N of Road Town, British Virgin Islands",
            "11km NNW of Jones, Oklahoma",
            "10km WNW of Cobb, California",
            "110km NW of Ensenada, Baja California",
        ]
        for place in list_of_places:
            if "Baja California" in place:
                test_data = False
                self.assertFalse(test_data)
            elif "California" in place:
                test_data = True
                self.assertTrue(test_data)
            else:
                test_data = False
                self.assertFalse(test_data)

    def test_for_date_formatting(self):
        """
        test_for_date_formatting
        """
        # terminal shows datetime object as local time
        # via http://www.epochconverter.com/ - 2013-12-07 6:10:23.060000
        # local: 2013-12-07 10:10:23.060000

        # the date/time from the api is a unix timestamp
        date_time = 1386439823060

        # the timezone from the api offset from UTC in minutes at the event
        # epicenter
        tz = -360

        # convert the unix timestamp to utc datetime object
        test_data = isinstance(datetime.datetime.utcfromtimestamp(date_time / 1e3), datetime.datetime)
        self.assertTrue(test_data)

    # test views
    def test_index_page(self):
        """
        retrieve index page view
        """
        test_response = self.app.get("/")
        self.assertEqual(200, test_response.status_code)


if __name__ == "__main__":
    unittest.main()
