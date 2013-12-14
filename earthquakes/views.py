#!/usr/bin/env python

import os, logging
from flask import Flask, jsonify, render_template, request, \
    Response, send_from_directory, session, g, redirect, \
    url_for, abort, flash, make_response
from flask.ext.restful import reqparse, abort, Api, Resource
from earthquakes import app, db
from earthquakes.models import Earthquake

logging.basicConfig(format='\033[1;36m%(levelname)s:\033[0;37m %(message)s', level=logging.DEBUG)

# flask_restful config
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('task', type=str)

@app.route('/')
def index():
    earthquake_instances = Earthquake.query.order_by(Earthquake.date_time.desc())
    return render_template('index.html', earthquake_instances=earthquake_instances)

@app.route('/<int:primary_id>', methods=['GET'])
def detail(primary_id):
    earthquake_instances = Earthquake.query.filter_by(primary_id=primary_id).order_by(Earthquake.date_time.desc()).first_or_404()
    return render_template('detail.html', earthquake_instances=earthquake_instances)






def make_public_resource(item):
    ''' take database record and add resource_uri '''
    item['resource_uri'] = url_for('earthquake', primary_id = item['primary_id'], _external = True)
    return item

def require_appkey(view_function):
    ''' requires an api key to hit json endpoints '''
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        if request.args.get('apikey') and request.args.get('apikey') == app.config['APIKEY']:
            return view_function(*args, **kwargs)
        else:
            abort(401)
    return decorated_function

def evaluate_query_comparison(comparison):
    ''' evaluates logic for sql query '''
    if comparison == 'gt':
        query_comparison = '>'
    elif comparison == 'lt':
        query_comparison = '<'
    elif comparison == 'is':
        query_comparison = '='
    else:
        query_comparison = None
        abort(400)
    return query_comparison