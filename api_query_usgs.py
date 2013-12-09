# -*- coding: utf-8 -*-
import os, logging, requests
from sqlite3 import dbapi2 as sqlite3
from contextlib import closing
from concurrent import futures
import config

logging.basicConfig(level=logging.DEBUG)

class a_single_earthquake():
    ''' describes and gives structure to a single earthquake '''
    def __init__(self, data_id, data_type):
        self.data_id = data_id
        self.data_type = data_type

def query_usgs_api(target_url):
    #usgs_api_query = requests.get(TARGET_URL, headers=config.config_settings['headers'])
    usgs_api_query = requests.get(config.config_settings['seven_days_m4.5'])
    usgs_api_data = usgs_api_query.json()
    usgs_earthquakes = usgs_api_data['features']
    list_of_earthquakes = []
    for index, item in enumerate(usgs_earthquakes):
        this_earthquake = a_single_earthquake(
            index,
            item['type']
        )
        list_of_earthquakes.append(this_earthquake)
    write_data_to(list_of_earthquakes)

def write_data_to(list_of_data):
    logging.debug(list_of_data)

    connection = None
    connection = sqlite3.connect('earthquake.db')
    with connection:
        cursor = connection.cursor()
        for item in list_of_data:
            logging.debug(item.data_type)
            cursor.execute("INSERT INTO Earthquakes VALUES (%s, %s)", (item.data_id, item.data_type))
        connection.commit()
        if connection:
            connection.close()

def retrieve_data_from(database):
    connection = sqlite3.connect(database)
    with connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM Earthquakes')
        rows = cursor.fetchall()
        for row in rows:
            logging.debug('fetching row')
            print '%s %s' % (row['id'], row['type'])

if __name__ == '__main__':
    query_usgs_api(config.config_settings['seven_days_m4.5'])
    #retrieve_data_from('earthquake.db')