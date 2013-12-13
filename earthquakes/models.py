#!/usr/bin/env python

import os, logging, requests, time, datetime, calendar
from sqlalchemy import Column, Integer, String, Float, BigInteger, DateTime, Text
from earthquakes.database import Base

class Experiment(Base):
    __tablename__ = 'experiments'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(1000))
    date_time = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)

    def __init__(self, id, name, date_time):
        self.id = id
        self.name = name
        self.date_time = date_time

    def __repr__(self):
        return '<User %r>' % self.name

class Earthquake(Base):
    __tablename__ = 'earthquakes'
    primary_id = Column(BigInteger, primary_key=True, autoincrement=True)
    primary_slug = Column(Text)
    mag = Column(Integer, nullable=True)
    place = Column(String(1000), nullable=True)
    title = Column(String(1000), nullable=True)
    date_time = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    tz = Column(Integer, nullable=True)
    url = Column(Text, nullable=True)
    felt = Column(Integer, nullable=True)
    cdi = Column(Float, nullable=True)
    mmi = Column(Integer, nullable=True)
    alert = Column(String(1000), nullable=True)
    status = Column(String(1000), nullable=True)
    tsunami = Column(Integer, nullable=True)
    sig = Column(Integer, nullable=True)
    resource_type = Column(String(1000), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    depth = Column(Float, nullable=True)

    def __init__(self, primary_id, primary_slug, mag, place, title, date_time, updated, tz, url, felt, cdi, mmi, alert, status, tsunami, sig, resource_type, latitude, longitude, depth):
        self.primary_id = primary_id
        self.primary_slug = primary_slug
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

    def __repr__(self):
        return '<place %r>' % self.place