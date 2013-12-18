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

# asset pipeline
assets = Environment(app)

js = Bundle(
    'scripts/libs/jquery.min.js',
    'scripts/libs/modernizr.min.js',
    'scripts/libs/underscore-min.js',
    'scripts/libs/backbone-min.js',
    'scripts/libs/moment.min.js',
    'scripts/libs/bootstrap.min.js',
    'scripts/app.js',
    'scripts/router/router.js',
    'scripts/models/earthquake.js',
    'scripts/collections/earthquakes.js',
    'scripts/views/list.js',
    'scripts/views/details.js',
    filters='rjsmin',
    output='assets/scripts/min.js',
)
assets.register('scripts_all', js)

css = Bundle(
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