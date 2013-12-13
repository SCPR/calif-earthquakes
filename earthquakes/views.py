#!/usr/bin/env python

import os, logging
from flask import Flask, jsonify, render_template, request, \
    Response, send_from_directory, session, g, redirect, \
    url_for, abort, flash, make_response
from flask.ext.restful import reqparse, abort, Api, Resource
from earthquakes import app
from earthquakes.database import db_session
from earthquakes.models import Earthquake, Experiment

logging.basicConfig(format='\033[1;36m%(levelname)s:\033[0;37m %(message)s', level=logging.DEBUG)

# flask_restful config
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('task', type=str)

@app.route('/')
def index():
    earthquake_instances = Earthquake.query.all()
    experiment_instances = Experiment.query.all()
    return render_template('index.html', earthquake_instances=earthquake_instances, experiment_instances=experiment_instances)