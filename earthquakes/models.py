#!/usr/bin/env python

import os, logging, requests, time, datetime, calendar
from flask import url_for
from flask.ext.sqlalchemy import SQLAlchemy
from earthquakes import app, db
import earthquakes.views

class Earthquake(db.Model):
    __tablename__ = 'earthquake'
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
    nearest_cities = db.relationship('NearestCity', backref='earthquake', lazy='dynamic')

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

    def resource_uri(self):
        ''' take database record and add resource_uri '''
        url_prefix = "%s/api/earthquakes" % app.config["SITE_URL"]
        return "%s/%s" % (url_prefix, self.id)

    def __repr__(self):
        return '<place %r>' % self.place

    @property
    def serialize(self):
        return {
            'id': self.id,
            'primary_slug': self.primary_slug,
            'mag': self.mag,
            'place': self.place,
            'title': self.title,
            'date_time': self.date_time,
            'date_time_raw': self.date_time_raw,
            'updated': self.updated,
            'updated_raw': self.updated_raw,
            'tz': self.tz,
            'url': self.url,
            'felt': self.felt,
            'cdi': self.cdi,
            'mmi': self.mmi,
            'alert': self.alert,
            'status': self.status,
            'tsunami': self.tsunami,
            'sig': self.sig,
            'resource_type': self.resource_type,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'depth': self.depth,
            'net': self.net,
            'code': self.code,
            'ids': self.ids,
            'sources': self.sources,
            'nst': self.nst,
            'dmin': self.dmin,
            'rms': self.rms,
            'gap': self.gap,
            'magType': self.magType,
            'nearest_cities_url': self.nearest_cities_url,
            #'nearest_cities': self.nearest_cities,
        }

    @property
    def serialize_many2many(self):
       '''
       Return object's relations in easily serializeable format.
       NB! Calls many2many's serialize property.
       '''
       return [item.serialize for item in self.many2many]

class NearestCity(db.Model):
    __tablename__ = 'nearest_cities'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    distance = db.Column(db.Integer, nullable=True)
    direction = db.Column(db.String(1000))
    name = db.Column(db.String(5000))
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    population = db.Column(db.Integer, nullable=True)
    earthquake_id = db.Column(db.Integer, db.ForeignKey('earthquake.id'))

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
        return '<name %r>' % self.name