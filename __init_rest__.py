# -*- coding: utf-8 -*-
import os, logging
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, jsonify, render_template, request, \
    Response, send_from_directory, session, g, redirect, \
    url_for, abort, flash, make_response
from flask.ext.assets import Environment, Bundle
from flask.ext.restful import reqparse, abort, Api, Resource
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
api = Api(app)
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

###########################

# handcrafted api endpoints
@app.route('/api/v1.0/earthquakes/', methods=['GET'])
#@require_appkey
def return_earthquakes_from_database():
    ''' returns all of the earthquakes in the database sorted by newest first '''
    earthquakes = query_db('SELECT * from Earthquakes order by time desc')

    logging.debug(earthquakes)

    if earthquakes is None:
        abort(404)
    return jsonify({
        'metadata': {'status': 200, 'records': len(earthquakes)},
        'results': map(make_public_resource, earthquakes)
    })

@app.route('/api/v1.0/earthquakes/<int:primary_id>/', methods=['GET'])
#@require_appkey
def return_earthquake_from_database(primary_id):
    earthquakes = query_db('SELECT * from Earthquakes WHERE primary_id = ? order by primary_id desc', [primary_id], one=True)
    if earthquakes is None:
        abort(404)
    return jsonify({
        'metadata': {'status': 200, 'records': 1},
        'results': make_public_resource(earthquakes)
    })

@app.route('/api/v1.0/earthquakes/mag_gt=<float:mag>', methods=['GET'])
#@require_appkey
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



###########################

# handcrafted api endpoints

# https://github.com/miguelgrinberg/REST-tutorial/blob/master/rest-server-v2.py

earthquakes = [{'status': u'reviewed', 'sig': 882, 'updated': 1386710939478, 'tz': -360, 'title': u'M4.5  - 11km NNW of Jones, Oklahoma', 'url': u'http://earthquake.usgs.gov/earthquakes/eventpage/usb000ldeh', 'felt': 3638, 'cdi': 5.7, 'longitude': -97.3261, 'alert': u'green', 'primary_id': 0, 'tsunami': None, 'depth': 5, 'place': u'11km NNW of Jones, Oklahoma', 'mag': 4.5, 'time': 1386439823060, 'latitude': 35.6627, 'mmi': 4.47, 'type': u'earthquake'}, {'status': u'reviewed', 'sig': 632, 'updated': 1385873780000, 'tz': 540, 'title': u'M6.4  - Kepulauan Barat Daya, Indonesia', 'url': u'http://earthquake.usgs.gov/earthquakes/eventpage/usb000l8mb', 'felt': 3, 'cdi': 5.8, 'longitude': 128.3757, 'alert': u'green', 'primary_id': 1, 'tsunami': None, 'depth': 10.01, 'place': u'Kepulauan Barat Daya, Indonesia', 'mag': 6.4, 'time': 1385861053620, 'latitude': -7.0137, 'mmi': 6.4, 'type': u'earthquake'}, {'status': u'reviewed', 'sig': 754, 'updated': 1385477923937, 'tz': -240, 'title': u'M7.0  - South Atlantic Ocean', 'url': u'http://earthquake.usgs.gov/earthquakes/eventpage/usb000l5zn', 'felt': None, 'cdi': None, 'longitude': -54.8821, 'alert': u'green', 'primary_id': 2, 'tsunami': None, 'depth': 10, 'place': u'South Atlantic Ocean', 'mag': 7, 'time': 1385360853990, 'latitude': -53.8813, 'mmi': 0, 'type': u'earthquake'}, {'status': u'reviewed', 'sig': 651, 'updated': 1386255344172, 'tz': -720, 'title': u'M6.5  - Fiji region', 'url': u'http://earthquake.usgs.gov/earthquakes/eventpage/usb000l51g', 'felt': 3, 'cdi': 2.9, 'longitude': -176.5416, 'alert': u'green', 'primary_id': 3, 'tsunami': None, 'depth': 371, 'place': u'Fiji region', 'mag': 6.5, 'time': 1385192912120, 'latitude': -17.1137, 'mmi': 3.57, 'type': u'earthquake'}, {'status': u'reviewed', 'sig': 912, 'updated': 1386400251592, 'tz': -180, 'title': u'M7.7  - Scotia Sea', 'url': u'http://earthquake.usgs.gov/earthquakes/eventpage/usb000l0gq', 'felt': None, 'cdi': None, 'longitude': -46.4011, 'alert': u'green', 'primary_id': 4, 'tsunami': 1, 'depth': 10, 'place': u'Scotia Sea', 'mag': 7.7, 'time': 1384679095530, 'latitude': -60.2738, 'mmi': 6.71, 'type': u'earthquake'}, {'status': u'reviewed', 'sig': 711, 'updated': 1384989142188, 'tz': -180, 'title': u'M6.8  - Scotia Sea', 'url': u'http://earthquake.usgs.gov/earthquakes/eventpage/usb000kznc', 'felt': None, 'cdi': None, 'longitude': -47.1076, 'alert': u'green', 'primary_id': 5, 'tsunami': 1, 'depth': 9.98, 'place': u'Scotia Sea', 'mag': 6.8, 'time': 1384572871950, 'latitude': -60.2132, 'mmi': 4.92, 'type': u'earthquake'}, {'status': u'reviewed', 'sig': 631, 'updated': 1386669010611, 'tz': 720, 'title': u"M6.4  - 172km S of Ust'-Kamchatsk Staryy, Russia", 'url': u'http://earthquake.usgs.gov/earthquakes/eventpage/usb000kw1x', 'felt': 1, 'cdi': 4.3, 'longitude': 162.3024, 'alert': u'green', 'primary_id': 6, 'tsunami': 1, 'depth': 43, 'place': u"172km S of Ust'-Kamchatsk Staryy, Russia", 'mag': 6.4, 'time': 1384239831090, 'latitude': 54.6859, 'mmi': 6.33, 'type': u'earthquake'}]

def abort_if_doesnt_exist(primary_id):
    return abort(404, message="An item with the id of {} doesn't exist".format(primary_id))

parser = reqparse.RequestParser()
parser.add_argument('task', type=str)


# list all items
class EarthquakeList(Resource):
    def get(self):
        return earthquakes

# show single item
class Earthquake(Resource):
    def get(self, primary_id):
        for quake in earthquakes:
            logging.debug(quake['primary_id'])
            if quake['primary_id'] == primary_id:
                return quake
            else:
                abort_if_doesnt_exist(primary_id)



api.add_resource(EarthquakeList, '/test_quakes')
api.add_resource(Earthquake, '/test_quakes/<int:primary_id>')





if __name__ == '__main__':
    #init_db()
    app.run()