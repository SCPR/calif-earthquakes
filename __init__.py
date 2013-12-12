# -*- coding: utf-8 -*-
import os, logging
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, jsonify, render_template, request, \
    Response, send_from_directory, session, g, redirect, \
    url_for, abort, flash, make_response
from flask.ext.assets import Environment, Bundle
from functools import wraps
from contextlib import closing
from concurrent import futures
import config
import template_filters
import webassets

logging.basicConfig(format='\033[1;36m%(levelname)s:\033[0;37m %(message)s', level=logging.DEBUG)
PROJ_PATH, _ = os.path.split(os.path.abspath(os.path.realpath(__file__)))
app = Flask(__name__, static_url_path='/static')
app.jinja_env.filters['datetime_format'] = template_filters.datetime_format
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
    ''' best reusable function ever '''
    cur = get_db().execute(query, args)
    rv = [dict((cur.description[i][0], value) \
               for i, value in enumerate(row)) for row in cur.fetchall()]
    cur.close()
    return (rv[0] if rv else None) if one else rv

def make_public_resource(item):
    ''' take database record and add resource_uri '''
    item['resource_uri'] = url_for('return_earthquake_from_database', primary_id = item['primary_id'], _external = True)
    return item

def require_appkey(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        if request.args.get('apikey') and request.args.get('apikey') == app.config['APIKEY']:
            return view_function(*args, **kwargs)
        else:
            abort(401)
    return decorated_function

@app.route('/', methods=['GET'])
def index():
    ''' displays main page and earthquakes in the database '''
    earthquakes = query_db('SELECT * from Earthquakes order by time desc')
    return render_template('index.html', earthquakes=earthquakes)

@app.route('/<int:primary_id>', methods=['GET'])
def detail(primary_id):
    earthquake = query_db('SELECT * from Earthquakes WHERE primary_id = ? order by primary_id desc', [primary_id], one=True)
    if earthquake is None:
        abort(404)
    return render_template('detail.html', earthquake=earthquake)




# trying to create api urls
@app.route('/api/v1.0/earthquakes/', methods=['GET'])
@require_appkey
def return_earthquakes_from_database():
    ''' returns all of the earthquakes in the database sorted by newest first '''
    earthquakes = query_db('SELECT * from Earthquakes order by time desc')

    if earthquakes is None:
        abort(404)
    return jsonify({
        'metadata': {'status': 200, 'records': len(earthquakes)},
        'results': map(make_public_resource, earthquakes)
    })

@app.route('/api/v1.0/earthquakes/<int:primary_id>/', methods=['GET'])
@require_appkey
def return_earthquake_from_database(primary_id):
    earthquakes = query_db('SELECT * from Earthquakes WHERE primary_id = ? order by primary_id desc', [primary_id], one=True)
    if earthquakes is None:
        abort(404)
    return jsonify({
        'metadata': {'status': 200, 'records': 1},
        'results': make_public_resource(earthquakes)
    })

@app.route('/api/v1.0/earthquakes/mag_gt=<float:mag>', methods=['GET'])
@require_appkey
def test_return_earthquake_from_database(mag):
    earthquakes = query_db('SELECT * from Earthquakes WHERE mag > ?', [mag])
    if earthquakes is None:
        abort(404)
    return jsonify({
        'metadata': {'status': 200, 'records': len(earthquakes)},
        'results': earthquakes
    })

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Resource Not Found'}), 404)









if __name__ == '__main__':
    #init_db()
    app.run()