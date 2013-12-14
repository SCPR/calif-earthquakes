#!/usr/bin/env python

import os, logging, requests, time, datetime, calendar
import pytz
from pytz import timezone
from datetime import tzinfo, date
from earthquakes import app_config
from flask.ext.script import Manager, Command
from earthquakes import app, db
from earthquakes.models import Earthquake, Experiment

logging.basicConfig(format='\033[1;36m%(levelname)s:\033[0;37m %(message)s', level=logging.DEBUG)

manager = Manager(app)

class UsgsApiQuery(Command):

    #"mimics django's get or create function"
    #def get_or_create(self, session, model, **kwargs):
        #instance = session.query(model).filter_by(**kwargs).first()
        #if instance:
            #return instance
        #else:
            #instance = model(**kwargs)
            #session.add(instance)
            #session.commit()
            #return instance

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
        logging.debug(list_of_urls)
        list_of_data = []
        for detail_url in list_of_urls:
            time.sleep(5)
            logging.debug('sleeping prior to details request')
            usgs_query_details = requests.get(detail_url, headers=app_config.config_settings['headers'])
            usgs_api_details = usgs_query_details.json()
            list_of_data.append(usgs_api_details)
        self.write(list_of_data)

    "write class instances to the database"
    def write(self, list_of_instances):
        for item in list_of_instances:
            comparison_slug = '%s-%s' % (item['properties']['title'].lower(), item['properties']['time'])
            comparison_updated_raw = item['properties']['updated']
            instance = Earthquake.query.filter_by(primary_slug=comparison_slug).first()

            if instance is not None and instance.updated_raw == comparison_updated_raw:
                logging.debug('record exists and hasnt been updated')
                quake = None

            elif instance is not None and instance.updated_raw != comparison_updated_raw:
                logging.debug('there is an update to this record')
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
                    depth = item['geometry']['coordinates'][2]
                )

            elif instance is None:
                logging.debug('record doesnt exist')
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
                    depth = item['geometry']['coordinates'][2]
                )

            else:
                logging.debug('dont know what this might be')
                logging.debug(instance.updated_raw)
                quake = None

            if quake is not None:
                db.session.add(quake)
                db.session.commit()
            else:
                pass

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

class InitDb(Command):
    "sets up the database based on models"
    def run(self):
        db.create_all()

class Testing(Command):
    "prints that the test command is working"
    def run(self):
        print "The Test Command Is Working"

manager.add_command('initdb', InitDb())
manager.add_command('query', UsgsApiQuery())
manager.add_command('date', TestDates())
manager.add_command('test', Testing())

if __name__ == "__main__":
    manager.run()