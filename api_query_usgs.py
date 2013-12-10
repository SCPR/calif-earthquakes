# -*- coding: utf-8 -*-
import os, logging, requests
from sqlite3 import dbapi2 as sqlite3
from contextlib import closing
from concurrent import futures
import config

logging.basicConfig(format='\033[1;36m%(levelname)s:\033[0;37m %(message)s', level=logging.DEBUG)

class a_single_earthquake():
    ''' describes and gives structure to a single earthquake '''
    def __init__(self, id, mag, place, title, time, updated, tz, url, felt, cdi, mmi, alert, status, tsunami, sig, type, latitude, longitude, depth):
        self.primary_id = id
        self.mag = mag
        self.place = place
        self.title = title
        self.time = time
        self.updated = updated
        self.tz = tz
        self.url = url
        self.felt = felt
        self.cdi = cdi
        self.mmi = mmi
        self.alert = alert
        self.status = status
        self.tsunami = tsunami
        self.sig = sig
        self.type = type
        self.latitude = latitude
        self.longitude = longitude
        self.depth = depth

class usgs_api_query():
    @staticmethod
    def make_request_to_api(target_url):
        ''' performs request on earthquake api url and returns the data '''
        usgs_query_api = requests.get(target_url, headers=config.config_settings['headers'])
        usgs_api_data = usgs_query_api.json()
        list_of_details_urls = []
        for item in usgs_api_data['features']:
            if 'Oklahoma' in item['properties']['place']:
                usgs_details_link = str(item['properties']['detail'])
                list_of_details_urls.append(usgs_details_link)
            else:
                pass
        usgs_api_query.retrieve_details_from(list_of_details_urls)

    @staticmethod
    def retrieve_details_from(list_of_details_urls):
        ''' performs request on local earthquake details url and returns the data '''
        list_of_details_data = []
        for detail_url in list_of_details_urls:
            usgs_query_details = requests.get(detail_url, headers=config.config_settings['headers'])
            usgs_api_details = usgs_query_details.json()
            list_of_details_data.append(usgs_api_details)
        process_this_data = process_usgs_api_data()
        process_this_data.create_earthquake_classes_from(list_of_details_data)

class process_usgs_api_data():
    @staticmethod
    def create_earthquake_classes_from(list_of_details_data):
        ''' take data and create a list of class instances '''
        list_of_earthquake_instances = []
        for index, item in enumerate(list_of_details_data):
            this_earthquake = a_single_earthquake(
                index,
                item['properties']['mag'],
                item['properties']['place'],
                item['properties']['title'],
                item['properties']['time'],
                item['properties']['updated'],
                item['properties']['tz'],
                item['properties']['url'],
                item['properties']['felt'],
                item['properties']['cdi'],
                item['properties']['mmi'],
                item['properties']['alert'],
                item['properties']['status'],
                item['properties']['tsunami'],
                item['properties']['sig'],
                item['properties']['type'],
                item['geometry']['coordinates'][1],
                item['geometry']['coordinates'][0],
                item['geometry']['coordinates'][2],
            )
            list_of_earthquake_instances.append(this_earthquake)
        process_usgs_api_data.write(list_of_earthquake_instances, 'earthquake.db')

    @staticmethod
    def write(list_of_earthquake_instances, database):
        ''' write class instances to the database '''
        connection = None
        connection = sqlite3.connect(database)
        with connection:
            cursor = connection.cursor()
            for item in list_of_earthquake_instances:
                cursor.execute("INSERT INTO Earthquakes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (item.primary_id, item.mag, item.place, item.title, item.time, item.updated, item.tz, item.url, item.felt, item.cdi, item.mmi, item.alert, item.status, item.tsunami, item.sig, item.type, item.latitude, item.longitude, item.depth))
                connection.commit()
        connection.close()

if __name__ == '__main__':
    new_api_query = usgs_api_query()
    data_to_process = new_api_query.make_request_to_api(config.config_settings['month_sig'])