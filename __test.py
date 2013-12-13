# -*- coding: utf-8 -*-
import os, logging
from flask import Flask, jsonify, render_template, request, \
    Response, send_from_directory, session, g, redirect, \
    url_for, abort, flash, make_response
from flask.ext.assets import Environment, Bundle
from flask.ext.restful import reqparse, abort, Api, Resource
from flask.ext.sqlalchemy import SQLAlchemy
from functools import wraps
from contextlib import closing
from concurrent import futures
import app_config
import template_filters
import webassets

logging.basicConfig(format='\033[1;36m%(levelname)s:\033[0;37m %(message)s', level=logging.DEBUG)

# app settings
PROJ_PATH, _ = os.path.split(os.path.abspath(os.path.realpath(__file__)))
app = Flask(__name__, static_url_path='/static')
app.jinja_env.filters['datetime_format'] = template_filters.datetime_format
app.config.from_object(app_config)

# initiate the database
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

# flask_restful
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('task', type=str)

# asset pipeline
assets = Environment(app)
js = Bundle(
    'scripts/app.js',
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

# start the application
if __name__ == '__main__':
    app.run()