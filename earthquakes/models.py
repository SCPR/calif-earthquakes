#!/usr/bin/env python

import os, logging, requests, time, datetime, calendar
from flask import url_for
from flask.ext.sqlalchemy import SQLAlchemy
import pytz
from pytz import timezone
from datetime import tzinfo, date
from earthquakes import app, db
import earthquakes.views

logging.basicConfig(format="\033[1;36m%(levelname)s:\033[0;37m %(message)s", level=logging.DEBUG)

class Earthquake(db.Model):
    __tablename__ = "earthquake"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    primary_slug = db.Column(db.Text)
    mag = db.Column(db.Float, nullable=True)
    place = db.Column(db.String(1000), nullable=True)
    title = db.Column(db.String(1000), nullable=True)
    date_time = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    date_time_raw = db.Column(db.BigInteger)
    updated = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated_raw = db.Column(db.BigInteger)
    tz = db.Column(db.Integer, nullable=True)
    url = db.Column(db.Text, nullable=True)
    felt = db.Column(db.Integer, nullable=True)
    cdi = db.Column(db.Float, nullable=True)
    mmi = db.Column(db.Float, nullable=True)
    alert = db.Column(db.String(1000), nullable=True)
    status = db.Column(db.String(1000), nullable=True)
    tsunami = db.Column(db.Integer, nullable=True)
    sig = db.Column(db.Integer, nullable=True)
    resource_type = db.Column(db.String(1000), nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    depth = db.Column(db.Float, nullable=True)
    net = db.Column(db.String(1000), nullable=True)
    code = db.Column(db.String(1000), nullable=True)
    ids = db.Column(db.String(1000), nullable=True)
    sources = db.Column(db.String(1000), nullable=True)
    nst = db.Column(db.Integer, nullable=True)
    dmin = db.Column(db.Float, nullable=True)
    rms = db.Column(db.Float, nullable=True)
    gap = db.Column(db.Float, nullable=True)
    magType = db.Column(db.String(1000), nullable=True)
    nearest_cities_url = db.Column(db.Text, nullable=True)
    nearest_cities = db.relationship("NearestCity", backref="earthquake", lazy="dynamic")

    def __init__(self, id, primary_slug, mag, place, title, date_time, date_time_raw, updated, updated_raw, tz, url, felt, cdi, mmi, alert, status, tsunami, sig, resource_type, latitude, longitude, depth, net, code, ids, sources, nst, dmin, rms, gap, magType, nearest_cities_url, nearest_cities):
        self.id = id
        self.primary_slug = primary_slug
        self.mag = mag
        self.place = place
        self.title = title
        self.date_time = date_time
        self.date_time_raw = date_time_raw
        self.updated = updated
        self.updated_raw = updated_raw
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
        self.net = net
        self.code = code
        self.ids = ids
        self.sources = sources
        self.nst = nst
        self.dmin = dmin
        self.rms = rms
        self.gap = gap
        self.magType = magType
        self.nearest_cities_url = nearest_cities_url
        self.nearest_cities = nearest_cities

    def __repr__(self):
        return "<place %r>" % self.place

    @staticmethod
    def generate_resource_uri(id):
        ''' take database record and add resource_uri '''
        url_prefix = "%s/api/earthquakes" % app.config["SITE_URL"]
        return "%s/%s" % (url_prefix, id)

    @staticmethod
    def generate_pacific_time(date_time):
        ''' take database record and create pacific timezone day and date '''
        pacific = pytz.timezone("US/Pacific")
        utc = timezone("UTC")
        date = date_time.replace(tzinfo=pytz.UTC).astimezone(pacific)
        pacific_timezone = date.strftime("%a, %d %b %Y %H:%M:%S %z")
        return pacific_timezone

    @staticmethod
    def strip_state(value):
        try:
            value = value.replace(", California", "")
        except:
            value = value
        return value

    @staticmethod
    def split_location_from_state(value):
        value = Earthquake.strip_state(value)
        split_value = value.split(" of ")
        return split_value

    @staticmethod
    def format_date_for_display(date, date_format):
        pacific = pytz.timezone("US/Pacific")
        utc = timezone("UTC")
        date = date.replace(tzinfo=pytz.UTC).astimezone(pacific)
        date_string = date.strftime(date_format)
        return date_string

    @staticmethod
    def generate_tracker_url(value, date, id):
        ''' take database record and creates link to earthquake tracker instance '''
        split_value = Earthquake.split_location_from_state(value)
        instance_date = Earthquake.format_date_for_display(date, "%B-%-d-%Y").lower()
        if len(split_value) == 1:
            instance_location = str(split_value[0]).replace(" ", "-").lower()
        elif len(split_value) == 2:
            instance_location = str(split_value[1]).replace(" ", "-").lower()
        formatted_value = "%s-%s" % (instance_location, instance_date)
        url_prefix = "%s/%s" % (app.config["SITE_URL"], formatted_value)
        return "%s/%s" % (url_prefix, id)

    @staticmethod
    def serialize_many2many(nearest_cities):
       '''
       Return object's relations in easily serializeable format.
       nb! calls many2many's serialize property.
       '''

       list_of_nearest_cities = [i.serialize for i in nearest_cities]
       return list_of_nearest_cities

    @property
    def serialize(self):
        return {
            "pacific_timezone": Earthquake.generate_pacific_time(self.date_time),
            "earthquake_tracker_url": Earthquake.generate_tracker_url(self.place, self.date_time, self.id),
            "resource_uri": Earthquake.generate_resource_uri(self.id),
            "nearest_cities": Earthquake.serialize_many2many(self.nearest_cities),
            "id": self.id,
            "primary_slug": self.primary_slug,
            "mag": self.mag,
            "place": self.place,
            "title": self.title,
            "date_time": self.date_time,
            "date_time_raw": self.date_time_raw,
            "updated": self.updated,
            "updated_raw": self.updated_raw,
            "tz": self.tz,
            "url": self.url,
            "felt": self.felt,
            "cdi": self.cdi,
            "mmi": self.mmi,
            "alert": self.alert,
            "status": self.status,
            "tsunami": self.tsunami,
            "sig": self.sig,
            "resource_type": self.resource_type,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "depth": self.depth,
            "net": self.net,
            "code": self.code,
            "ids": self.ids,
            "sources": self.sources,
            "nst": self.nst,
            "dmin": self.dmin,
            "rms": self.rms,
            "gap": self.gap,
            "magType": self.magType,
            "nearest_cities_url": self.nearest_cities_url,
        }

class NearestCity(db.Model):
    __tablename__ = "nearest_cities"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    distance = db.Column(db.Integer, nullable=True)
    direction = db.Column(db.String(1000))
    name = db.Column(db.String(5000))
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    population = db.Column(db.Integer, nullable=True)
    earthquake_id = db.Column(db.Integer, db.ForeignKey("earthquake.id"))

    def __init__(self, id, distance, direction, name, latitude, longitude, population, earthquake_id):
        self.id = id
        self.name = name
        self.distance = distance
        self.direction = direction
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.population = population
        self.earthquake_id = earthquake_id

    def __repr__(self):
        return "<name %r>" % self.name

    @property
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "distance": self.distance,
            "direction": self.direction,
            "name": self.name,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "population": self.population,
            "earthquake_id": self.earthquake_id
        }

    @property
    def serialize_many2many(self):
       '''
       Return object's relations in easily serializeable format.
       NB! Calls many2many's serialize property.
       '''
       return [item.serialize for item in self.many2many]