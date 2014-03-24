#!/usr/bin/env python

import os
import logging
import requests
import time
import datetime
import calendar
import pytz
from requests_futures.sessions import FuturesSession
from pytz import timezone
from datetime import tzinfo, date
from flask.ext.script import Manager, Command, Option
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.mail import Mail, Message
from concurrent import futures
from earthquakes import app, db
from earthquakes.models import Earthquake, NearestCity

logging.basicConfig(
    format="\033[1;36m%(levelname)s:\033[0;37m %(message)s", level=logging.DEBUG)

migrate = Migrate(app, db)
manager = Manager(app)
mail = Mail(app)

class UsgsApiQuery(Command):

    option_list = (
        Option("--api_url", "-api_url", dest="api_url"),
    )

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
    def run(self, api_url):
        usgs_query_api = requests.get(
            app.config[api_url], headers=app.config["API_MANAGER_HEADERS"])
        usgs_api_data = usgs_query_api.json()
        list_of_urls = []
        for item in usgs_api_data["features"]:
            if "California" in item["properties"]["place"]:
                logging.debug("Details: %s. URL: %s" % (item["properties"]["title"], item["properties"]["url"]))
                usgs_details_link = str(item["properties"]["detail"])
                list_of_urls.append(usgs_details_link)
            else:
                logging.debug("passing this one by")
                pass
        self.retrieve_details_from(list_of_urls)

    "performs request on local earthquake details url and returns the data"
    def retrieve_details_from(self, list_of_urls):
        list_of_instances = []
        session = FuturesSession(max_workers=3)
        for detail_url in list_of_urls:
            # time.sleep(5)
            usgs_query_details = session.get(
                detail_url, headers=app.config["API_MANAGER_HEADERS"])
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
                nearest_cities_url = detail_instance["properties"]["products"][
                    "nearby-cities"][0]["contents"]["nearby-cities.json"]["url"]
            except:
                nearest_cities_url = None
            if nearest_cities_url is not None:
                nearest_cities_query_details = session.get(
                    nearest_cities_url, headers=app.config["API_MANAGER_HEADERS"])
                nearest_cities_api_details = nearest_cities_query_details.result(
                )
                nearest_cities_api_details = nearest_cities_api_details.json()
                list_of_nearby_cities = []
                for nearby_city in nearest_cities_api_details:
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
                    list_of_nearby_cities.append(city)
                detail_instance["nearest_cities_url"] = nearest_cities_url
                detail_instance["nearest_cities"] = list_of_nearby_cities
            else:
                pass
        self.write(list_of_instances)

    "write class instances to the database"
    def write(self, list_of_instances):
        for item in list_of_instances:
            comparison_code = "%s" % (item["properties"]["code"])
            comparison_updated_raw = item["properties"]["updated"]
            instance = Earthquake.query.filter_by(code=comparison_code).first()
            if instance is None:
                logging.debug("Creating new record for %s" % (item["properties"]["title"]))
                quake = Earthquake(
                    id=None,
                    primary_slug="%s-%s" % (
                        item["properties"]["title"].lower(),
                        item["properties"]["time"]
                    ),
                    mag=item["properties"]["mag"],
                    place=item["properties"]["place"],
                    title=item["properties"]["title"],
                    date_time=datetime.datetime.utcfromtimestamp(
                        item["properties"]["time"] / 1e3
                    ),
                    date_time_raw=item["properties"]["time"],
                    updated=datetime.datetime.utcfromtimestamp(
                        item["properties"]["updated"] / 1e3
                    ),
                    updated_raw=item["properties"]["updated"],
                    tz=item["properties"]["tz"],
                    url=item["properties"]["url"],
                    felt=item["properties"]["felt"],
                    cdi=item["properties"]["cdi"],
                    mmi=item["properties"]["mmi"],
                    alert=item["properties"]["alert"],
                    status=item["properties"]["status"],
                    tsunami=item["properties"]["tsunami"],
                    sig=item["properties"]["sig"],
                    resource_type=item["properties"]["type"],
                    latitude=item["geometry"]["coordinates"][1],
                    longitude=item["geometry"]["coordinates"][0],
                    depth=item["geometry"]["coordinates"][2],
                    net=item["properties"]["net"],
                    code=item["properties"]["code"],
                    ids=item["properties"]["ids"],
                    sources=item["properties"]["sources"],
                    nst=item["properties"]["nst"],
                    dmin=item["properties"]["dmin"],
                    rms=item["properties"]["rms"],
                    gap=item["properties"]["gap"],
                    magType=item["properties"]["magType"],
                    nearest_cities_url=item["nearest_cities_url"],
                    nearest_cities=item["nearest_cities"]
                )

                self.generate_email(quake)

                db.session.add(quake)
                for city in item["nearest_cities"]:
                    db.session.add(city)
            else:
                if instance.updated_raw == comparison_updated_raw:
                    logging.debug(
                        "compared and found record exists and doesnt need to be updated")
                    pass
                else:
                    logging.debug("compared and have updated this record")
                    instance.primary_slug = "%s-%s" % (
                        item["properties"]["title"].lower(),
                        item["properties"]["time"]
                    )
                    instance.mag = item["properties"]["mag"]
                    instance.place = item["properties"]["place"]
                    instance.title = item["properties"]["title"]
                    instance.date_time = datetime.datetime.utcfromtimestamp(
                        item["properties"]["time"] / 1e3
                    )
                    instance.date_time_raw = item["properties"]["time"]
                    instance.updated = datetime.datetime.utcfromtimestamp(
                        item["properties"]["updated"] / 1e3
                    )
                    instance.updated_raw = item["properties"]["updated"]
                    instance.tz = item["properties"]["tz"]
                    instance.url = item["properties"]["url"]
                    instance.felt = item["properties"]["felt"]
                    instance.cdi = item["properties"]["cdi"]
                    instance.mmi = item["properties"]["mmi"]
                    instance.alert = item["properties"]["alert"]
                    instance.status = item["properties"]["status"]
                    instance.tsunami = item["properties"]["tsunami"]
                    instance.sig = item["properties"]["sig"]
                    instance.resource_type = item["properties"]["type"]
                    instance.latitude = item["geometry"]["coordinates"][1]
                    instance.longitude = item["geometry"]["coordinates"][0]
                    instance.depth = item["geometry"]["coordinates"][2]
                    instance.net = item["properties"]["net"]
                    instance.code = item["properties"]["code"]
                    instance.ids = item["properties"]["ids"]
                    instance.sources = item["properties"]["sources"]
                    instance.nst = item["properties"]["nst"]
                    instance.dmin = item["properties"]["dmin"]
                    instance.rms = item["properties"]["rms"]
                    instance.gap = item["properties"]["gap"]
                    instance.magType = item["properties"]["magType"]
                    instance.nearest_cities_url = item["nearest_cities_url"]
            db.session.commit()
        logging.debug('Processed %s records' % (len(list_of_instances)))

    "generate an email to send out"
    def generate_email(self, quake):
        if quake.mag >= 4:
            value = quake.place.replace(", California", "")
            split_value = value.split(" of ")
            quake_distance = split_value[0].split(" ")
            quake_miles = int(quake_distance[0].replace("km", ""))
            quake_miles = "{0:.3g}".format(quake_miles / 1.609344)
            quake_direction = quake_distance[1]
            quake_location = split_value[1]
            pacific = pytz.timezone("US/Pacific")
            utc = timezone("UTC")
            value = quake.date_time.replace(tzinfo=pytz.UTC).astimezone(pacific)
            url_format = "%B-%-d-%Y"
            url_string = value.strftime(url_format).lower()
            weekday_format = "%A"
            weekday_string = value.strftime(weekday_format)
            time_format = "%I:%M %p %Z"
            time_string = value.strftime(time_format)
            quake_depth = "{0:.3g}".format(quake.depth / 1.609344)
            link_to_quake = "http://projects.scpr.org/earthquakes"

            subject_line = "USGS alert: %s. %s on %s" % (
                quake.title,
                time_string,
                weekday_string
            )

            msg = Message(
                subject_line,
                sender = "kpccdatadesk@gmail.com",
                recipients = app.config["EMAIL_DISTRIBUTION"]
            )

            msg.body = "An alert from USGS suggests a magnitude %s earthquake occurred at %s %s about %s miles %s of %s, which could be of interest to our audience.\n\nPlease confirm the acccuracy of the alert and double check the details against the USGS' report: %s\n\nYou can find a link to the Earthquake Tracker page for this earthquake on our internal lookup page:\nhttp://projects.scpr.org/earthquakes/internal-staff-lookup\n\nBasic details of the earthquake are below.\n\n----------\n\nA magnitude %s earthquake struck about %s miles %s of %s at %s on %s, according to the U.S. Geological Survey.\n\nThe earthquake's depth was recorded at about %s miles, according to the USGS.\n\nRELATED: More details on KPCC's Earthquake Tracker: %s" % (
                    quake.mag,
                    time_string,
                    weekday_string,
                    quake_miles,
                    quake_direction,
                    quake_location,
                    quake.url,
                    quake.mag,
                    quake_miles,
                    quake_direction,
                    quake_location,
                    time_string,
                    weekday_string,
                    quake_depth,
                    link_to_quake
                )

            mail.send(msg)

            logging.debug(msg)

        else:
            pass

class InitDb(Command):

    "sets up the database based on models"
    def run(self):
        db.create_all()

class dropEarthquakesRows(Command):

    "deletes all instances of the Earthquake model in the table"
    def run(self):
        database_rows = len(Earthquake.query.all())
        Earthquake.query.delete()
        db.session.commit()
        logging.debug("deleted %s records" % (database_rows))

class dropNearbyCitiesRows(Command):

    "deletes all instances of the NearbyCities model in the table"
    def run(self):
        database_rows = len(NearestCity.query.all())
        NearestCity.query.delete()
        db.session.commit()
        logging.debug("deleted %s records" % (database_rows))

class dropIndividualRow(Command):

    option_list = (
        Option("--record", "-record", dest="record"),
    )

    "deletes instance of a record in the table"
    def run(self, record):
        id = int(record)
        earthquake = Earthquake.query.get(id)
        db.session.delete(earthquake)
        db.session.commit()

class findDuplicates(Command):

    "deletes instance of a duplicate record in the table"
    def run(self):

        # lets get all of the earthquakes
        earthquakes = Earthquake.query.all()

        # create a list to hold the duplicates
        list_of_duplicate_quakes = []

        # cycle through our queryset
        for quake in earthquakes:

            # identify if it's a duplicate
            duplicate = Earthquake.query.filter_by(code=quake.code).count()

            # if it is a double dupe append it to a list
            if duplicate == 2:
                logging.debug("Two matches")
                this_quake = Earthquake.query.filter_by(code=quake.code).all()
                list_of_duplicate_quakes.append(this_quake)

            # if it is a three dupe append it to a list
            elif duplicate == 3:
                logging.debug("Three matches")
                this_quake = Earthquake.query.filter_by(code=quake.code).all()
                list_of_duplicate_quakes.append(this_quake)

            # pass it on by
            else:
                logging.debug("No matches or outlier")

        findDuplicates.process(list_of_duplicate_quakes)

    @staticmethod
    def process(list_of_duplicate_quakes):

        # here's a list of lists of duplicates
        for instance in list_of_duplicate_quakes:

            # let's consider our two instances
            if len(instance) == 2:
                initial_instance = instance[0]
                comparison_instance = instance[1]

                # see if the codes are the same
                if initial_instance.code == comparison_instance.code:
                    logging.debug("checking for the newer record?")

                    # compare timestamps
                    if comparison_instance.updated_raw > initial_instance.updated_raw:
                        findDuplicates.delete_this_duplicate(
                            initial_instance.id)
                    else:
                        findDuplicates.delete_this_duplicate(
                            comparison_instance.id)
                else:
                    logging.debug(
                        "These codes don't match so let's leave things alone")

            # let's consider our three instances
            elif len(instance) == 3:
                initial_instance = instance[0]
                middle_instance = instance[1]
                last_instance = instance[2]

                # see if the codes are the same
                if initial_instance.code == middle_instance.code == last_instance.code:
                    logging.debug("checking for the newer record?")

                    print "%s - %s - %s" % (initial_instance.updated, middle_instance.updated, last_instance.updated)
                    big = last_instance.updated
                    if (initial_instance.updated > middle_instance.updated and initial_instance.updated > last_instance.updated):
                        big = initial_instance.updated
                        findDuplicates.delete_this_duplicate(
                            middle_instance.id)
                        findDuplicates.delete_this_duplicate(last_instance.id)
                        print big
                    elif(middle_instance.updated > last_instance.updated):
                        big = middle_instance.updated
                        findDuplicates.delete_this_duplicate(
                            initial_instance.id)
                        findDuplicates.delete_this_duplicate(last_instance.id)
                        print big
                    else:
                        findDuplicates.delete_this_duplicate(
                            initial_instance.id)
                        findDuplicates.delete_this_duplicate(
                            middle_instance.id)
                        print big

    @staticmethod
    def delete_this_duplicate(record_id):
        logging.debug("Delete %s from database" % (record_id))
        try:
            earthquake = Earthquake.query.get(record_id)
            logging.debug(earthquake)
            db.session.delete(earthquake)
            db.session.commit()
        except:
            print "exception for %s\n" % (record_id)

class local_test_argument(Command):

    "sets up the database based on models"
    option_list = (
        Option("--api_url", "-api_url", dest="api_url"),
    )

    def run(self, api_url):
        logging.debug(app.config[api_url])
        logging.debug("%s" % (api_url))

manager.add_command("query", UsgsApiQuery())
manager.add_command("initdb", InitDb())
manager.add_command("drop_earthquakes", dropEarthquakesRows())
manager.add_command("drop_cities", dropNearbyCitiesRows())
manager.add_command("drop_row", dropIndividualRow())
manager.add_command("find_dupes", findDuplicates())
manager.add_command("local_test_argument", local_test_argument)
manager.add_command("db", MigrateCommand)

if __name__ == "__main__":
    manager.run()