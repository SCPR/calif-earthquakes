#!/usr/bin/env python

import os, logging
from flask import Flask, jsonify, render_template, request, \
    Response, send_from_directory, session, g, redirect, \
    url_for, abort, flash, make_response
from flask.ext.assets import Environment, Bundle
from flask.ext.sqlalchemy import SQLAlchemy
import app_config
import template_filters
import webassets

logging.basicConfig(format='\033[1;36m%(levelname)s:\033[0;37m %(message)s', level=logging.DEBUG)

PROJ_PATH, _ = os.path.split(os.path.abspath(os.path.realpath(__file__)))

app = Flask(__name__, static_url_path='/static')

app.config.from_object(app_config)

app.config['ASSETS_DEBUG'] = app_config.config_settings['DEBUG']

app.jinja_env.filters['datetime_format'] = template_filters.datetime_format
app.jinja_env.filters['date_format'] = template_filters.date_format
app.jinja_env.filters['strip_and_format_state'] = template_filters.strip_and_format_state
app.jinja_env.filters['strip_state'] = template_filters.strip_state
app.jinja_env.filters['place_format'] = template_filters.place_format
app.jinja_env.filters['convert_km_to_miles'] = template_filters.convert_km_to_miles

# asset pipeline
assets = Environment(app)

js = Bundle(
    'scripts/libs/jquery.min.js',
    'scripts/libs/modernizr.min.js',
    'scripts/libs/jquery-ui.js',
    'scripts/libs/underscore-min.js',
    'scripts/libs/backbone-min.js',
    'scripts/libs/moment.min.js',
    'scripts/libs/bootstrap.min.js',
    'scripts/libs/leaflet.js',
    'scripts/libs/leaflet.markercluster-src.js',
    'scripts/libs/jQRangeSlider-min.js',
    'data/california/california-la-county.js',
    'data/la-county-faults/la-county-faults.js',
    'scripts/app.js',
    'scripts/router/router.js',
    'scripts/models/earthquake.js',
    'scripts/models/map.js',
    'scripts/models/marker.js',
    'scripts/collections/earthquakes.js',
    'scripts/collections/markers.js',
    #'scripts/views/list.js',
    #'scripts/views/details.js',
    'scripts/views/map.js',
    'scripts/views/clustered-marker.js',
    filters='rjsmin',
    output='assets/scripts/min.js',
)
assets.register('scripts_all', js)

css = Bundle(
    'css/jquery-ui.css',
    'css/iThing.css',
    'css/leaflet.min.css',
    'css/MarkerCluster.css',
    'css/MarkerCluster.Default.css',
    'css/style.css',
    filters='cssmin',
    output='assets/css/min.css'
)
assets.register('css_all', css)

# configure database
app.config['SQLALCHEMY_DATABASE_URI'] = app_config.config_settings['sqlalchemy_database_uri']
db = SQLAlchemy(app)

import earthquakes.views

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()