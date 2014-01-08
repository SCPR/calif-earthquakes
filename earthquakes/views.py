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

#@app.route('/')
#def index():
    #return render_template('index.html')


@app.route('/')
def index():
    recent_instances = Earthquake.query.limit(3).all()
    earthquake_instances = Earthquake.query.all()
    return render_template(
        'index.html',
        recent_instances=recent_instances,
        earthquake_instances=earthquake_instances
    )

@app.route('/<int:id>', methods=['GET'])
def detail(id):
    earthquake_instance = Earthquake.query.filter_by(id=id).order_by(Earthquake.date_time.desc()).first_or_404()
    return render_template('detail.html', earthquake_instance=earthquake_instance)


'''
@app.route('/earthquakes')
def get_earthquakes():
    earthquake_instances = Earthquake.query.order_by(Earthquake.date_time.desc())
    logging.debug(earthquake_instances)
    return jsonify(
        collection=[i.serialize for i in earthquake_instances]
    )
'''

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
manager.create_api(Earthquake, methods=['GET'], include_methods=['resource_uri'], results_per_page=100)