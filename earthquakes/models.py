#!/usr/bin/env python

import os, logging, requests, time, datetime, calendar
from flask import url_for
from flask.ext.sqlalchemy import SQLAlchemy
from earthquakes import app, db
import earthquakes.views

class Experiment(db.Model):
    __tablename__ = 'experiments'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(1000))
    date_time = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)

    def __init__(self, id, name, date_time):
        self.id = id
        self.name = name
        self.date_time = date_time

    def __repr__(self):
        return '<User %r>' % self.name

class Earthquake(db.Model):
    __tablename__ = 'earthquakes'
    primary_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    primary_slug = db.Column(db.Text)
    mag = db.Column(db.Integer, nullable=True)
    place = db.Column(db.String(1000), nullable=True)
    title = db.Column(db.String(1000), nullable=True)
    date_time = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated_raw = db.Column(db.BigInteger)
    tz = db.Column(db.Integer, nullable=True)
    url = db.Column(db.Text, nullable=True)
    felt = db.Column(db.Integer, nullable=True)
    cdi = db.Column(db.Float, nullable=True)
    mmi = db.Column(db.Integer, nullable=True)
    alert = db.Column(db.String(1000), nullable=True)
    status = db.Column(db.String(1000), nullable=True)
    tsunami = db.Column(db.Integer, nullable=True)
    sig = db.Column(db.Integer, nullable=True)
    resource_type = db.Column(db.String(1000), nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    depth = db.Column(db.Float, nullable=True)

    def __init__(self, primary_id, primary_slug, mag, place, title, date_time, updated, updated_raw, tz, url, felt, cdi, mmi, alert, status, tsunami, sig, resource_type, latitude, longitude, depth):
        self.primary_id = primary_id
        self.primary_slug = primary_slug
        self.mag = mag
        self.place = place
        self.title = title
        self.date_time = date_time
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

    def resource_uri(self):
        ''' take database record and add resource_uri '''
        url_prefix = 'http://127.0.0.1:5000/api/earthquakes'
        return "%s/%s" % (url_prefix, self.primary_id)

    def __repr__(self):
        return '<place %r>' % self.place