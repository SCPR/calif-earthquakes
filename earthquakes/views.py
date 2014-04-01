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

# set the maximum number of records to return to the view
DB_QUERY_LIMIT = 1000

@app.route('/')
def index():

    # set the cache key
    cache_expiration = 60 * 10

    # set the cache identifier
    identifier = 'view/index'

    # see if cache exists
    cached = cache.get(identifier)

    # if cache exists return it
    if cached is not None:
        return cached

    # if cache doesnt exist generate the page
    else:
        earthquakes = Earthquake.query.order_by(Earthquake.date_time_raw.desc()).limit(DB_QUERY_LIMIT).all()
        recent_earthquakes = earthquakes[:3]
        earthquake_instances = []
        for earthquake in earthquakes:
            if earthquake.mag > 2.5:
                earthquake_instances.append(earthquake)
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

    # set the cache key
    cache_expiration = 60 * 10

    # set the cache identifier
    identifier = 'detail_view_for_%d' % id

    # see if cache exists
    cached = cache.get(identifier)

    # if cache exists return it
    if cached is not None:
        return cached

    # otherwise generate the page
    else:

        # get this earthquake
        earthquake = Earthquake.query.filter_by(id=id).first_or_404()
        this_earthquake = (earthquake.latitude, earthquake.longitude)

        # get earthquakes that aren't this one
        earthquake_instances = Earthquake.query.filter(Earthquake.id!=id).order_by(Earthquake.date_time_raw.desc()).limit(DB_QUERY_LIMIT).all()
        recent_earthquakes = earthquake_instances[:6]

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

    # set the cache key
    cache_expiration = 60 * 10

    # set the cache identifier
    identifier = 'internal_staff_lookup'

    # see if cache exists
    cached = cache.get(identifier)

    # if cache exists return it
    if cached is not None:
        return cached

    # otherwise generate the page
    else:
        earthquake_instances = Earthquake.query.order_by(Earthquake.date_time_raw.desc()).limit(100).all()
        tmplt = render_template(
            'lookup.html',
            earthquake_instances = earthquake_instances
        )

        # add pass the identifier and the template to the cache
        cache.set(identifier, tmplt, timeout = cache_expiration)
        return tmplt

@app.route('/explore-the-map', methods=['GET'])
def map():

    # set the cache key
    cache_expiration = 60 * 10

    # set the cache identifier
    identifier = 'explore_the_map'

    # see if cache exists
    cached = cache.get(identifier)

    # if cache exists return it
    if cached is not None:
        logging.debug(cached)
        return cached

    # otherwise generate the page
    else:
        tmplt = render_template(
            'full-screen-map.html'
        )

        # add pass the identifier and the template to the cache
        cache.set(identifier, tmplt, timeout = cache_expiration)
        return tmplt

@app.route('/la-habra-earthquakes', methods=['GET'])
def la_habra_map():


    # set the cache key
    cache_expiration = 60 * 10

    # set the cache identifier
    identifier = 'la_habra_earthquakes'

    # see if cache exists
    cached = cache.get(identifier)

    # if cache exists return it
    if cached is not None:
        logging.debug(cached)
        return cached

    # otherwise generate the page
    else:
        tmplt = render_template(
            'la-habra-earthquakes.html'
        )

        # add pass the identifier and the template to the cache
        cache.set(identifier, tmplt, timeout = cache_expiration)
        return tmplt

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
manager.create_api(Earthquake, methods=['GET'], include_methods=['resource_uri', 'earthquake_tracker_url', 'pacific_timezone'], results_per_page=300, max_results_per_page=300)
