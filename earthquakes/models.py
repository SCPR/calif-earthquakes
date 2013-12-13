#!/usr/bin/env python

import os, logging
from sqlalchemy import Column, Integer, String, Float, BigInteger
from earthquakes.database import Base

class Earthquake(Base):
    __tablename__ = 'earthquakes'
    primary_id = Column(Integer, primary_key=True)
    mag = Column(Integer)
    place = Column(String(1000))
    title = Column(String(1000))
    date_time = Column(BigInteger)
    updated = Column(BigInteger)
    tz = Column(Integer)
    url = Column(String(1000))
    felt = Column(Integer)
    cdi = Column(Float)
    mmi = Column(Integer)
    alert = Column(String(1000))
    status = Column(String(1000))
    tsunami = Column(Integer)
    sig = Column(Integer)
    resource_type = Column(String(1000))
    latitude = Column(Float)
    longitude = Column(Float)
    depth = Column(Float)

    def __init__(self, primary_id, mag, place, title, date_time, updated, tz, url, felt, cdi, mmi, alert, status, tsunami, sig, resource_type, latitude, longitude, depth):
        self.primary_id = primary_id
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