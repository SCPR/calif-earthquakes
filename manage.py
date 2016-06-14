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
from earthquakes import app, db, assets
from earthquakes.models import Earthquake, NearestCity
from flask.ext.assets import ManageAssets

logger = logging.getLogger("root")
logging.basicConfig(
    format="\033[1;36m%(levelname)s: %(filename)s (def %(funcName)s %(lineno)s): \033[1;37m %(message)s",
    level=logging.DEBUG
)

logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

migrate = Migrate(app, db)
manager = Manager(app)
mail = Mail(app)


class UsgsApiQuery(Command):

    option_list = (
        Option("--api_url", "-api_url", dest="api_url"),
    )

    def run(self, api_url):
        """
        performs request on earthquake api url and returns the data
        """
        earthquakes = self.get_usgs_api_response(api_url)
        if earthquakes:
            for item in earthquakes["features"]:
                if "Baja California" in item["properties"]["place"]:
                    pass
                else:
                    if "California" in item["properties"]["place"]:
                        compare_code = "%s" % (item['properties']["code"])
                        compare_place = '%s' % (item['properties']['place'])
                        compare_time = '%s' % (item['properties']['time'])
                        compare_raw = item['properties']['updated']
                        instance = Earthquake.query.filter_by(
                            code=compare_code,
                            place=compare_place,
                            date_time_raw=compare_time
                        ).first()
                        if instance is None:
                            earthquake_details = self.get_usgs_details_response(
                                item["properties"]["detail"])
                            if earthquake_details:
                                this_quake = self.get_usgs_nearby_cities(earthquake_details)
                                self.write_to_db(this_quake)
                                logger.debug("Created %s on %s" % (item['properties']["title"], datetime.datetime.utcfromtimestamp(item['properties']["time"] / 1e3)))
                                if item["properties"]["mag"] >= 3.5:
                                    self.generate_email(this_quake)
                        else:
                            if instance.updated_raw == compare_raw:
                                logger.debug("Exists: %s" % (item['properties']["title"]))
                            else:
                                earthquake_details = self.get_usgs_details_response(item["properties"]["detail"])
                                if earthquake_details:
                                    this_quake = self.get_usgs_nearby_cities(earthquake_details)
                                    self.update_to_db(instance, this_quake)
                                    logger.debug("Updated: %s" % (item['properties']["title"]))
        else:
            logger.debug("Nothing here to show for our efforts")
            pass

    def get_usgs_api_response(self, url):
        """
        test response from usgs api
        """
        try:
            response = requests.get(app.config[url], headers=app.config[
                                    "API_MANAGER_HEADERS"])
            response.raise_for_status()
            response_data = response.json()
            return response_data
        except requests.exceptions as exception:
            logger.error("%s: %s" % (exception))
            return False

    def get_usgs_details_response(self, url):
        """
        performs request on local earthquake details url and returns the data
        """
        session = FuturesSession(max_workers=1)
        usgs_api_details = session.get(
            url, headers=app.config["API_MANAGER_HEADERS"])
        try:
            earthquake_details = usgs_api_details.result().json()
            return earthquake_details
        except requests.exceptions as exception:
            logger.error("%s: %s" % (exception))
            return False

    def get_usgs_nearby_cities(self, earthquake):
        """
        performs request on local earthquake nearby cities url and returns the data
        """
        try:
            nearest_cities_object = earthquake[
                "properties"]["products"]["nearby-cities"]
            nearest_cities_url = nearest_cities_object[0][
                "contents"]["nearby-cities.json"]["url"]
        except:
            nearest_cities_url = None
        if nearest_cities_url:
            session = FuturesSession(max_workers=1)
            nearest_cities_response = session.get(
                nearest_cities_url, headers=app.config["API_MANAGER_HEADERS"])
            nearest_cities_details = nearest_cities_response.result().json()
            list_of_nearby_cities = []
            for item in nearest_cities_details:
                city = NearestCity(
                    id=None,
                    distance=item["distance"],
                    direction=item["direction"],
                    name=item["name"],
                    latitude=item["latitude"],
                    longitude=item["longitude"],
                    population=item["population"],
                    earthquake_id=None
                )
                list_of_nearby_cities.append(city)
            earthquake["properties"]["nearest_cities_url"] = nearest_cities_url
            earthquake["properties"]["nearest_cities"] = list_of_nearby_cities
        else:
            earthquake["properties"]["nearest_cities_url"] = None
            earthquake["properties"]["nearest_cities"] = []
        return earthquake

    def write_to_db(self, earthquake):
        """
        try pulling earthquake codes into memory and querying those
        sted of pinging the database each time to see if it exists
        write class instances to the database
        """
        this = earthquake["properties"]
        quake = Earthquake(
            id=None,
            primary_slug="%s-%s" % (this["title"].lower(), this["time"]),
            mag=this["mag"],
            place=this["place"],
            title=this["title"],
            date_time=datetime.datetime.utcfromtimestamp(
                this["time"] / 1e3),
            date_time_raw=this["time"],
            updated=datetime.datetime.utcfromtimestamp(
                this["updated"] / 1e3),
            updated_raw=this["updated"],
            tz=this["tz"],
            url=this["url"],
            felt=this["felt"],
            cdi=this["cdi"],
            mmi=this["mmi"],
            alert=this["alert"],
            status=this["status"],
            tsunami=this["tsunami"],
            sig=this["sig"],
            resource_type=this["type"],
            latitude=earthquake["geometry"]["coordinates"][1],
            longitude=earthquake["geometry"]["coordinates"][0],
            depth=earthquake["geometry"]["coordinates"][2],
            net=this["net"],
            code=this["code"],
            ids=this["ids"],
            sources=this["sources"],
            nst=this["nst"],
            dmin=this["dmin"],
            rms=this["rms"],
            gap=this["gap"],
            magType=this["magType"],
            nearest_cities_url=this["nearest_cities_url"],
            nearest_cities=this["nearest_cities"]
        )
        db.session.add(quake)
        if this["nearest_cities"]:
            for city in this["nearest_cities"]:
                db.session.add(city)
        db.session.commit()

    def update_to_db(self, instance, earthquake):
        """
        update an instance of an earthquake that already exists
        """
        this = earthquake["properties"]
        instance.primary_slug = "%s-%s" % (this["title"].lower(), this["time"])
        instance.mag = this["mag"]
        instance.place = this["place"]
        instance.title = this["title"]
        instance.date_time = datetime.datetime.utcfromtimestamp(this[
                                                                "time"] / 1e3)
        instance.date_time_raw = this["time"]
        instance.updated = datetime.datetime.utcfromtimestamp(
            this["updated"] / 1e3)
        instance.updated_raw = this["updated"]
        instance.tz = this["tz"]
        instance.url = this["url"]
        instance.felt = this["felt"]
        instance.cdi = this["cdi"]
        instance.mmi = this["mmi"]
        instance.alert = this["alert"]
        instance.status = this["status"]
        instance.tsunami = this["tsunami"]
        instance.sig = this["sig"]
        instance.resource_type = this["type"]
        instance.latitude = earthquake["geometry"]["coordinates"][1]
        instance.longitude = earthquake["geometry"]["coordinates"][0]
        instance.depth = earthquake["geometry"]["coordinates"][2]
        instance.net = this["net"]
        instance.code = this["code"]
        instance.ids = this["ids"]
        instance.sources = this["sources"]
        instance.nst = this["nst"]
        instance.dmin = this["dmin"]
        instance.rms = this["rms"]
        instance.gap = this["gap"]
        instance.magType = this["magType"]
        instance.nearest_cities_url = this["nearest_cities_url"]
        instance.nearest_cities = this["nearest_cities"]
        if this["nearest_cities_url"]:
            for city in this["nearest_cities"]:
                db.session.add(city)
        db.session.commit()

    def generate_email(self, quake):
        """
        generate an email to send out
        """
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
        if len(split_value) == 1:
            formatted_value = str(split_value[0]).replace(" ", "-").lower()
        elif len(split_value) == 2:
            formatted_value = str(split_value[1]).replace(" ", "-").lower()
        link_to_quake = "http://earthquakes.scpr.org/%s-%s/%s" % (
            formatted_value, url_string, quake.id)
        subject_line = "USGS alert: %s. %s on %s" % (
            quake.title,
            time_string,
            weekday_string
        )
        msg = Message(
            subject_line,
            sender="kpccdatadesk@gmail.com",
            recipients=app.config["CONFIG"]["email_distribution"]
        )
        msg.body = "An alert from USGS suggests a magnitude %s earthquake occurred at %s %s about %s miles %s of %s, which could be of interest to our audience:\n%s.\n\nPlease confirm the acccuracy of the alert and double check the details against the USGS' report:\n%s\n\nand the California Integrated Seismic Network:\nhttp://www.cisn.org/eqinfo.html\n\nYou can find a link to the Earthquake Tracker page for this earthquake at\n%s\nand on our internal lookup page:\nhttp://earthquakes.scpr.org/internal-staff-lookup\n\nTo see if the Caltech Seismological Laboratory offer a media briefing call (626) 395-3227 during regular business hours or (626) 449-2631 after hours and on weekends.\n\nBasic details of the earthquake are below.\n\n----------\n\nA magnitude %s earthquake struck about %s miles %s of %s at %s on %s, according to the U.S. Geological Survey.\n\nThe earthquake's depth was recorded at about %s miles, according to the USGS.\n\nRELATED: Find more details on KPCC's Earthquake Tracker: %s" % (
            quake.mag, time_string, weekday_string, quake_miles, quake_direction, quake_location, link_to_quake, quake.url, link_to_quake, quake.mag, quake_miles, quake_direction, quake_location, time_string, weekday_string, quake_depth, link_to_quake)
        mail.send(msg)


class InitDb(Command):
    """
    sets up the database based on models
    """

    def run(self):
        db.create_all()


class dropEarthquakesRows(Command):
    """
    deletes all instances of the Earthquake model in the table
    """

    def run(self):
        database_rows = len(Earthquake.query.all())
        Earthquake.query.delete()
        db.session.commit()
        logger.debug("deleted %s records" % (database_rows))


class dropNearbyCitiesRows(Command):
    """
    deletes all instances of the NearbyCities model in the table
    """

    def run(self):
        database_rows = len(NearestCity.query.all())
        NearestCity.query.delete()
        db.session.commit()
        logger.debug("deleted %s records" % (database_rows))


class dropIndividualRow(Command):
    """
    deletes instance of a record in the table
    """
    option_list = (
        Option("--record", "-record", dest="record"),
    )

    def run(self, record):
        id = int(record)
        earthquake = Earthquake.query.get(id)
        db.session.delete(earthquake)
        db.session.commit()


class findDuplicates(Command):
    """
    deletes instance of a duplicate record in the table
    """

    def run(self):
        earthquakes = Earthquake.query.all()
        list_of_duplicate_quakes = []
        for quake in earthquakes:
            duplicate = Earthquake.query.filter_by(code=quake.code).count()
            if duplicate == 2:
                logger.debug("Two matches")
                this_quake = Earthquake.query.filter_by(code=quake.code).all()
                list_of_duplicate_quakes.append(this_quake)
            elif duplicate == 3:
                logger.debug("Three matches")
                this_quake = Earthquake.query.filter_by(code=quake.code).all()
                list_of_duplicate_quakes.append(this_quake)
            else:
                logger.debug("No matches or outlier")
        findDuplicates.process(list_of_duplicate_quakes)

    @staticmethod
    def process(list_of_duplicate_quakes):
        for instance in list_of_duplicate_quakes:
            if len(instance) == 2:
                initial_instance = instance[0]
                comparison_instance = instance[1]
                if initial_instance.code == comparison_instance.code:
                    logger.debug("checking for the newer record?")
                    if comparison_instance.updated_raw > initial_instance.updated_raw:
                        findDuplicates.delete_this_duplicate(
                            initial_instance.id)
                    else:
                        findDuplicates.delete_this_duplicate(
                            comparison_instance.id)
                else:
                    logger.debug(
                        "These codes don't match so let's leave things alone")
            elif len(instance) == 3:
                initial_instance = instance[0]
                middle_instance = instance[1]
                last_instance = instance[2]
                if initial_instance.code == middle_instance.code == last_instance.code:
                    logger.debug("checking for the newer record?")
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
        logger.debug("Delete %s from database" % (record_id))
        try:
            earthquake = Earthquake.query.get(record_id)
            logger.debug(earthquake)
            db.session.delete(earthquake)
            db.session.commit()
        except:
            print "exception for %s\n" % (record_id)


manager.add_command("query", UsgsApiQuery())
manager.add_command("initdb", InitDb())
manager.add_command("drop_earthquakes", dropEarthquakesRows())
manager.add_command("drop_cities", dropNearbyCitiesRows())
manager.add_command("drop_row", dropIndividualRow())
manager.add_command("find_dupes", findDuplicates())
manager.add_command("db", MigrateCommand)
manager.add_command("assets", ManageAssets(assets))

if __name__ == "__main__":
    manager.run()
