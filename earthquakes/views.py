#!/usr/bin/env python

import os, logging, json
from flask import Flask, jsonify, render_template, request, \
    Response, send_from_directory, session, g, redirect, \
    url_for, abort, flash, make_response
import flask.ext.sqlalchemy
import flask.ext.restless
from earthquakes import app, cache, db
from earthquakes.models import Earthquake
from haversine import haversine

logging.basicConfig(format='\033[1;36m%(levelname)s:\033[0;37m %(message)s', level=logging.DEBUG)

@app.route('/')
def index():

    cache_expiration = 60 * 10

    # set the cache key
    identifier = 'view/index'

    # see if theres a key
    cached = cache.get(identifier)

    # if it does, return it
    if cached is not None:
        return cached

    else:
        recent_earthquakes = Earthquake.query.order_by(Earthquake.date_time.desc()).limit(3).all()
        earthquake_instances = Earthquake.query.filter(Earthquake.mag>2.5).order_by(Earthquake.date_time.desc()).all()
        tmplt = render_template(
            'index.html',
            recent_earthquakes = recent_earthquakes,
            earthquake_instances = earthquake_instances
        )

        # add pass the identifier and the template to the cache
        cache.set(identifier, tmplt, timeout = cache_expiration)
        return tmplt

@app.route('/<string:title>/<int:id>/', methods=['GET'])
def detail(title, id):

    cache_expiration = 60 * 1

    # set the cache key
    identifier = 'detail_view_for_%d' % id

    # see if theres a key
    cached = cache.get(identifier)

    # if it does, return it
    if cached is not None:
        return cached

    # otherwise create it
    else:
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

        tmplt = render_template(
            'detail.html',
            recent_earthquakes = recent_earthquakes,
            earthquake = earthquake,
            nearest_earthquakes = list_of_nearby_earthquakes
        )

        # add pass the identifier and the template to the cache
        cache.set(identifier, tmplt, timeout = cache_expiration)
        return tmplt

@app.route('/internal-staff-lookup')
def lookup():
    earthquake_instances = Earthquake.query.filter(Earthquake.mag>1.0).order_by(Earthquake.date_time.desc()).all()
    return render_template(
        'lookup.html',
        earthquake_instances = earthquake_instances
    )

@app.route('/explore-the-map', methods=['GET'])
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
manager.create_api(Earthquake, methods=['GET'], include_methods=['resource_uri'], results_per_page=300, max_results_per_page=300)