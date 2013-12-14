#!/usr/bin/env python

import os, logging
from flask import Flask, jsonify, render_template, request, \
    Response, send_from_directory, session, g, redirect, \
    url_for, abort, flash, make_response
import flask.ext.sqlalchemy
import flask.ext.restless
from earthquakes import app, db
from earthquakes.models import Earthquake

logging.basicConfig(format='\033[1;36m%(levelname)s:\033[0;37m %(message)s', level=logging.DEBUG)

@app.route('/')
def index():
    earthquake_instances = Earthquake.query.order_by(Earthquake.date_time.desc())
    return render_template('index.html', earthquake_instances=earthquake_instances)

@app.route('/<int:primary_id>', methods=['GET'])
def detail(primary_id):
    earthquake_instances = Earthquake.query.filter_by(primary_id=primary_id).order_by(Earthquake.date_time.desc()).first_or_404()
    return render_template('detail.html', earthquake_instances=earthquake_instances)

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
manager.create_api(Earthquake, methods=['GET'], include_methods=['resource_uri'], results_per_page=5)