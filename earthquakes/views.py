#!/usr/bin/env python

import os, logging
from flask import Flask, jsonify, render_template, request, \
    Response, send_from_directory, session, g, redirect, \
    url_for, abort, flash, make_response
import flask.ext.sqlalchemy
import flask.ext.restless

from flask.ext.cache import Cache
from earthquakes import app, cache, db

#from earthquakes import app, db
from earthquakes.models import Earthquake
from haversine import haversine

logging.basicConfig(format='\033[1;36m%(levelname)s:\033[0;37m %(message)s', level=logging.DEBUG)

@app.route('/')
def index():
    cached = cache.get("view/index")

    if cached is not None:
        return cached

    recent_earthquakes = Earthquake.query.order_by(Earthquake.date_time.desc()).limit(3).all()
    earthquake_instances = Earthquake.query.filter(Earthquake.mag>2.5).order_by(Earthquake.date_time.desc()).all()
    tmplt = render_template(
        'index.html',
        recent_earthquakes = recent_earthquakes,
        earthquake_instances = earthquake_instances
    )

    cache.set("view/index", tmplt)
    return tmplt


@app.route('/<string:title>/<int:id>/', methods=['GET'])
def detail(title, id):

    recent_earthquakes = Earthquake.query.order_by(Earthquake.date_time.desc()).limit(6).all()

    earthquake = Earthquake.query.filter_by(id=id).order_by(Earthquake.date_time.desc()).first_or_404()

    # this earthquakes lat and long
    this_earthquake = (earthquake.latitude, earthquake.longitude)

    # return all earthquakes except this one
    earthquake_instances = Earthquake.query.filter(Earthquake.id!=id).order_by(Earthquake.date_time.desc()).all()

    # list to hold earthquakes found
    list_of_nearby_earthquakes = []

    # loop through our list of earthquakes
    for instance in earthquake_instances:

        # build a comparison
        comparision_earthquake = (instance.latitude, instance.longitude)

        # calculate the distance
        evaluated_distance = haversine(this_earthquake, comparision_earthquake)

        # if less than
        if evaluated_distance < 25:

            # add param to object
            instance.distance = evaluated_distance

            # move along if we have six
            if len(list_of_nearby_earthquakes) == 6:
                pass

            else:
                # append if we don't
                list_of_nearby_earthquakes.append(instance)

        # move along if not
        else:
            pass

    return render_template(
        'detail.html',
        recent_earthquakes = recent_earthquakes,
        earthquake = earthquake,
        nearest_earthquakes = list_of_nearby_earthquakes
    )

@app.route('/full-screen-map', methods=['GET'])
def map():
    return render_template(
        'full-screen-map.html',
    )

def require_appkey(view_function):
    ''' requires an api key to hit json endpoints '''
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        if request.args.get('apikey') and request.args.get('apikey') == app.config['APIKEY']:
            return view_function(*args, **kwargs)
        else:
            abort(401)
    return decorated_function

# flask_restless config
manager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=db)
manager.create_api(Earthquake, methods=['GET'], include_methods=['resource_uri'], results_per_page=200, max_results_per_page=200)