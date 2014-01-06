#!/usr/bin/env python

import os, logging, requests, time, datetime, calendar
import pytz
from requests_futures.sessions import FuturesSession
from pytz import timezone
from datetime import tzinfo, date
from earthquakes import app_config
from flask.ext.script import Manager, Command
from concurrent import futures
from earthquakes import app, db
from earthquakes.models import Earthquake, Experiment

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
        usgs_query_api = requests.get(app_config.config_settings['seven_days_2.5'], headers=app_config.config_settings['headers'])
        usgs_api_data = usgs_query_api.json()
        list_of_urls = []
        for item in usgs_api_data['features']:
            if 'California' in item['properties']['place']:
                usgs_details_link = str(item['properties']['detail'])
                list_of_urls.append(usgs_details_link)
            else:
                logging.debug('passing this one by')
                pass
        self.retrieve_details_from(list_of_urls)

    "performs request on local earthquake details url and returns the data"
    def retrieve_details_from(self, list_of_urls):
        list_of_data = []
        session = FuturesSession(max_workers=3)
        for detail_url in list_of_urls:
            #time.sleep(5)
            usgs_query_details = session.get(detail_url, headers=app_config.config_settings['headers'])
            usgs_api_details = usgs_query_details.result()
            usgs_api_details = usgs_api_details.json()
            list_of_data.append(usgs_api_details)
        self.write(list_of_data)

    "write class instances to the database"
    def write(self, list_of_instances):
        for item in list_of_instances:
            comparison_slug = '%s-%s' % (item['properties']['title'].lower(), item['properties']['time'])
            comparison_updated_raw = item['properties']['updated']
            instance = Earthquake.query.filter_by(primary_slug=comparison_slug).first()

            try:
                nearest_cities = item['properties']['products']['nearby-cities'][0]['contents']['nearby-cities.json']['url']
            except:
                nearest_cities = None

            if instance is None:
                logging.debug('creating new record')
                quake = Earthquake(
                    primary_id = None,
                    primary_slug = '%s-%s' % (item['properties']['title'].lower(), item['properties']['time']),
                    mag = item['properties']['mag'],
                    place = item['properties']['place'],
                    title = item['properties']['title'],
                    date_time = datetime.datetime.utcfromtimestamp(item['properties']['time']/1e3),
                    updated = datetime.datetime.utcfromtimestamp(item['properties']['updated']/1e3),
                    updated_raw = item['properties']['updated'],
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
                    depth = item['geometry']['coordinates'][2],
                    nearest_cities = nearest_cities
                )

                db.session.add(quake)

            else:
                if instance.updated_raw == comparison_updated_raw:
                    logging.debug('compared and found record exists and doesnt need to be updated')
                    pass
                else:
                    logging.debug('compared and have updated this record')
                    instance.primary_slug = '%s-%s' % (item['properties']['title'].lower(), item['properties']['time'])
                    instance.mag = item['properties']['mag']
                    instance.place = item['properties']['place']
                    instance.title = item['properties']['title']
                    instance.date_time = datetime.datetime.utcfromtimestamp(item['properties']['time']/1e3)
                    instance.updated = datetime.datetime.utcfromtimestamp(item['properties']['updated']/1e3)
                    instance.updated_raw = item['properties']['updated']
                    instance.tz = item['properties']['tz']
                    instance.url = item['properties']['url']
                    instance.felt = item['properties']['felt']
                    instance.cdi = item['properties']['cdi']
                    instance.mmi = item['properties']['mmi']
                    instance.alert = item['properties']['alert']
                    instance.status = item['properties']['status']
                    instance.tsunami = item['properties']['tsunami']
                    instance.sig = item['properties']['sig']
                    instance.resource_type = item['properties']['type']
                    instance.latitude = item['geometry']['coordinates'][1]
                    instance.longitude = item['geometry']['coordinates'][0]
                    instance.depth = item['geometry']['coordinates'][2]
                    instance.nearest_cities = nearest_cities

            db.session.commit()
        logging.debug('Processed %s records' % (len(list_of_instances)))

class TestDates(Command):
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

class TestUpdates(Command):
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

class InitDb(Command):
    "sets up the database based on models"
    def run(self):
        db.create_all()

class Testing(Command):
    "prints that the test command is working"
    def run(self):
        print "The Test Command Is Working"

manager.add_command('query', UsgsApiQuery())
manager.add_command('date', TestDates())
manager.add_command('updates', TestUpdates())
manager.add_command('initdb', InitDb())
manager.add_command('test', Testing())

if __name__ == "__main__":
    manager.run()