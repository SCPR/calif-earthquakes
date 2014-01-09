#!/usr/bin/env python

import os, logging
from flask import Flask, jsonify, render_template, request, \
    Response, send_from_directory, session, g, redirect, \
    url_for, abort, flash, make_response
import flask.ext.sqlalchemy
import flask.ext.restless
from earthquakes import app, db
from earthquakes.models import Earthquake
from haversine import haversine

logging.basicConfig(format='\033[1;36m%(levelname)s:\033[0;37m %(message)s', level=logging.DEBUG)

@app.route('/')
def index():
    recent_instances = Earthquake.query.order_by(Earthquake.date_time.desc()).limit(3).all()
    earthquake_instances = Earthquake.query.filter(Earthquake.mag>2.5).order_by(Earthquake.date_time.desc()).all()
    return render_template(
        'index.html',
        recent_instances=recent_instances,
        earthquake_instances=earthquake_instances
    )

@app.route('/<int:id>', methods=['GET'])
def detail(id):
    earthquake_instance = Earthquake.query.filter_by(id=id).order_by(Earthquake.date_time.desc()).first_or_404()
    recent_instances = Earthquake.query.order_by(Earthquake.date_time.desc()).limit(6).all()
    nearby_instances = Earthquake.query.order_by(Earthquake.date_time.desc()).all()
    this_earthquake = (earthquake_instance.latitude, earthquake_instance.longitude)
    list_of_incidents_near_here = []
    for instance in nearby_instances:
        comparision_earthquake = (instance.latitude, instance.longitude)
        distance_evaluation = haversine(this_earthquake, comparision_earthquake)
        if distance_evaluation < 25:
            list_of_incidents_near_here.append(instance)
            if len(list_of_incidents_near_here) == 6:
                pass
            else:
                continue
        else:
            pass
    return render_template(
        'detail.html',
        earthquake_instance = earthquake_instance,
        recent_instances = recent_instances,
        nearest_instances = list_of_incidents_near_here[0:6]
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