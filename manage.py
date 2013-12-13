#!/usr/bin/env python

import os, logging, requests
from earthquakes import app_config
from flask.ext.script import Manager, Command
from earthquakes import app
from earthquakes.database import init_db, db_session
from earthquakes.models import User, Earthquake

logging.basicConfig(format='\033[1;36m%(levelname)s:\033[0;37m %(message)s', level=logging.DEBUG)

manager = Manager(app)

class a_single_earthquake():
    ''' describes and gives structure to a single earthquake '''
    def __init__(self, id, mag, place, title, date_time, updated, tz, url, felt, cdi, mmi, alert, status, tsunami, sig, resource_type, latitude, longitude, depth):
        self.primary_id = id
        self.mag = mag
        self.place = place
        self.title = title
        self.date_time = date_time
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
        self.resource_type = resource_type
        self.latitude = latitude
        self.longitude = longitude
        self.depth = depth

class UsgsApiQuery(Command):
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

    "performs request on earthquake api url and returns the data"
    def run(self):
        usgs_query_api = requests.get(app_config.config_settings['month_sig'], headers=app_config.config_settings['headers'])
        usgs_api_data = usgs_query_api.json()
        list_of_details_urls = []
        for item in usgs_api_data['features']:
            if 'Indonesia' in item['properties']['place']:
                usgs_details_link = str(item['properties']['detail'])
                list_of_details_urls.append(usgs_details_link)
            else:
                pass
        self.retrieve_details_from(list_of_details_urls)

    "performs request on local earthquake details url and returns the data"
    def retrieve_details_from(self, list_of_details_urls):
        logging.debug(list_of_details_urls)
        list_of_details_data = []
        for detail_url in list_of_details_urls:
            usgs_query_details = requests.get(detail_url, headers=app_config.config_settings['headers'])
            usgs_api_details = usgs_query_details.json()
            list_of_details_data.append(usgs_api_details)
        self.create_earthquake_classes_from(list_of_details_data)

    "take data and create a list of class instances"
    def create_earthquake_classes_from(self, list_of_details_data):
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
        self.write(list_of_earthquake_instances)

    "write class instances to the database"
    def write(self, list_of_earthquake_instances):
        for item in list_of_earthquake_instances:
            thisQuake = self.get_or_create(db_session, Earthquake,
                primary_id = item.primary_id,
                mag = item.mag,
                place = item.place,
                title = item.title,
                date_time = item.date_time,
                updated = item.updated,
                tz = item.tz,
                url = item.url,
                felt = item.felt,
                cdi = item.cdi,
                mmi = item.mmi,
                alert = item.alert,
                status = item.status,
                tsunami = item.tsunami,
                sig = item.sig,
                resource_type = item.resource_type,
                latitude = item.latitude,
                longitude = item.longitude,
                depth = item.depth
            )

class InitDb(Command):
    "sets up the database based on models"
    def run(self):
        init_db()

class Testing(Command):
    "prints that the test command is working"
    def run(self):
        print "The Test Command Is Working"

manager.add_command('initdb', InitDb())
manager.add_command('query', UsgsApiQuery())
manager.add_command('test', Testing())

if __name__ == "__main__":
    manager.run()