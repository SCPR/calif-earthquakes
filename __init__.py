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

def connect_db():
    '''Connects to the specific database.'''
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def init_db():
    '''Creates the database tables.'''
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def get_db():
    '''Opens a new database connection if there is none.'''
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    '''Closes the database again at the end of the request.'''
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    init_db()
    app.run()