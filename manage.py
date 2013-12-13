#!/usr/bin/env python

import os, logging, requests
from earthquakes import app_config
from flask.ext.script import Manager, Command
from earthquakes import app
from earthquakes.database import init_db, db_session
from earthquakes.models import Experiment, Earthquake

logging.basicConfig(format='\033[1;36m%(levelname)s:\033[0;37m %(message)s', level=logging.DEBUG)

manager = Manager(app)

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
        list_of_urls = []
        for item in usgs_api_data['features']:
            if 'Oklahoma' in item['properties']['place']:
                usgs_details_link = str(item['properties']['detail'])
                list_of_urls.append(usgs_details_link)
            else:
                pass
        self.retrieve_details_from(list_of_urls)

    "performs request on local earthquake details url and returns the data"
    def retrieve_details_from(self, list_of_urls):
        logging.debug(list_of_urls)
        list_of_data = []
        for detail_url in list_of_urls:
            usgs_query_details = requests.get(detail_url, headers=app_config.config_settings['headers'])
            usgs_api_details = usgs_query_details.json()
            list_of_data.append(usgs_api_details)
        self.write(list_of_data)

    "write class instances to the database"
    def write(self, list_of_instances):
        for item in list_of_instances:
            thisQuake = self.get_or_create(db_session, Earthquake,
                primary_id = None,
                primary_slug = '%s-%s' % (item['properties']['title'].lower(), item['properties']['time']),
                mag = item['properties']['mag'],
                place = item['properties']['place'],
                title = item['properties']['title'],
                date_time = item['properties']['time'],
                updated = item['properties']['updated'],
                tz = item['properties']['tz'],
                url = item['properties']['url'],
                felt = item['properties']['felt'],
                cdi = item['properties']['cdi'],
                mmi = item['properties']['mmi'],
                alert = item['properties']['alert'],
                status = item['properties']['status'],
                tsunami = item['properties']['tsunami'],
                sig = item['properties']['sig'],
                resource_type = item['properties']['type'],
                latitude = item['geometry']['coordinates'][1],
                longitude = item['geometry']['coordinates'][0],
                depth = item['geometry']['coordinates'][2]
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