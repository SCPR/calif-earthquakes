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

def connect_db():
    '''Connects to the specific database.'''
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/', methods=['GET'])
def index():
    ''' displays main page and earthquakes in the database '''
    earthquakes = query_db('SELECT * from Earthquakes order by primary_id desc')
    records = [dict(
        primary_id=row[0],
        mag=row[1],
        place=row[2],
        title=row[3],
        time=row[4],
        updated=row[5],
        tz=row[6],
        url=row[7],
        felt=row[8],
        cdi=row[9],
        mmi=row[10],
        alert=row[11],
        status=row[12],
        tsunami=row[13],
        sig=row[14],
        type=row[15],
        latitude=row[16],
        longitude=row[17],
        depth=row[18],
    ) for row in earthquakes]
    return render_template('index.html', records=records)

@app.route('/<primary_id>', methods=['GET'])
def detail(primary_id):
    earthquake = query_db('SELECT * from Earthquakes WHERE primary_id = primary_id order by primary_id desc', one=True)
    return render_template('detail.html', earthquake=earthquake)

if __name__ == '__main__':
    #init_db()
    app.run()