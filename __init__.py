# -*- coding: utf-8 -*-
import os, logging
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, jsonify, render_template, request, \
    Response, send_from_directory, session, g, redirect, url_for, abort, flash
from flask.ext.assets import Environment, Bundle
from contextlib import closing
from concurrent import futures
import config
import webassets

logging.basicConfig(level=logging.DEBUG)
PROJ_PATH, _ = os.path.split(os.path.abspath(os.path.realpath(__file__)))
app = Flask(__name__, static_url_path='/static')
app.config.from_object(config)
assets = Environment(app)

# combine and compress scripts
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

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()