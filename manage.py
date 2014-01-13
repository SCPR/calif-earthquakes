#!/usr/bin/env python

import os, logging, requests, time, datetime, calendar
import pytz
from requests_futures.sessions import FuturesSession
from pytz import timezone
from datetime import tzinfo, date
from flask.ext.script import Manager, Command
from flask.ext.migrate import Migrate, MigrateCommand
from concurrent import futures
from earthquakes import app, db
from earthquakes.models import Earthquake, NearestCity

logging.basicConfig(format='\033[1;36m%(levelname)s:\033[0;37m %(message)s', level=logging.DEBUG)

migrate = Migrate(app, db)
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
        usgs_query_api = requests.get(app.config['ALL_PAST_DAY'], headers=app.config['API_MANAGER_HEADERS'])
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
        list_of_instances = []
        session = FuturesSession(max_workers=3)
        for detail_url in list_of_urls:
            #time.sleep(5)
            usgs_query_details = session.get(detail_url, headers=app.config['API_MANAGER_HEADERS'])
            try:
                usgs_api_details = usgs_query_details.result()
                usgs_api_details = usgs_api_details.json()
                list_of_instances.append(usgs_api_details)
            except:
                pass
        self.retrieve_nearby_cities_from(list_of_instances)

    "performs request on local earthquake nearby cities url and returns the data"
    def retrieve_nearby_cities_from(self, list_of_instances):
        session = FuturesSession(max_workers=1)
        for detail_instance in list_of_instances:
            try:
                nearest_cities_url = detail_instance['properties']['products']['nearby-cities'][0]['contents']['nearby-cities.json']['url']
            except:
                nearest_cities_url = None
            if nearest_cities_url is not None:
                nearest_cities_query_details = session.get(nearest_cities_url, headers=app.config['API_MANAGER_HEADERS'])
                nearest_cities_api_details = nearest_cities_query_details.result()
                nearest_cities_api_details = nearest_cities_api_details.json()
                list_of_nearby_cities = []
                for nearby_city in nearest_cities_api_details:
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
                    list_of_nearby_cities.append(city)
                logging.debug(list_of_nearby_cities)
                detail_instance['nearest_cities_url'] = nearest_cities_url
                detail_instance['nearest_cities'] = list_of_nearby_cities
            else:
                pass
        logging.debug(list_of_instances)
        self.write(list_of_instances)

    "write class instances to the database"
    def write(self, list_of_instances):
        for item in list_of_instances:
            comparison_slug = '%s-%s' % (item['properties']['title'].lower(), item['properties']['time'])
            comparison_updated_raw = item['properties']['updated']
            instance = Earthquake.query.filter_by(primary_slug=comparison_slug).first()
            if instance is None:
                logging.debug('creating new record')
                quake = Earthquake(
                    id = None,
                    primary_slug = '%s-%s' % (item['properties']['title'].lower(), item['properties']['time']),
                    mag = item['properties']['mag'],
                    place = item['properties']['place'],
                    title = item['properties']['title'],
                    date_time = datetime.datetime.utcfromtimestamp(item['properties']['time']/1e3),
                    date_time_raw = item['properties']['time'],
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
                    net = item['properties']['net'],
                    code = item['properties']['code'],
                    ids = item['properties']['ids'],
                    sources = item['properties']['sources'],
                    nst = item['properties']['nst'],
                    dmin = item['properties']['dmin'],
                    rms = item['properties']['rms'],
                    gap = item['properties']['gap'],
                    magType = item['properties']['magType'],
                    nearest_cities_url = item['nearest_cities_url'],
                    nearest_cities=item['nearest_cities']
                )
                db.session.add(quake)
                for city in item['nearest_cities']:
                    logging.debug(city)
                    db.session.add(city)
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
                    instance.date_time_raw = item['properties']['time']
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
                    instance.net = item['properties']['net']
                    instance.code = item['properties']['code']
                    instance.ids = item['properties']['ids']
                    instance.sources = item['properties']['sources']
                    instance.nst = item['properties']['nst']
                    instance.dmin = item['properties']['dmin']
                    instance.rms = item['properties']['rms']
                    instance.gap = item['properties']['gap']
                    instance.magType = item['properties']['magType']
                    instance.nearest_cities_url = item['nearest_cities_url']
            db.session.commit()
        logging.debug('Processed %s records' % (len(list_of_instances)))

class InitDb(Command):
    "sets up the database based on models"
    def run(self):
        db.create_all()

manager.add_command('query', UsgsApiQuery())
manager.add_command('initdb', InitDb())
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()