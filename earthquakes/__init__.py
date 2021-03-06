#!/usr/bin/env python

import os
import logging
from flask import Flask, jsonify, render_template, request, \
    Response, send_from_directory, session, g, redirect, \
    url_for, abort, flash, make_response
from flask.ext.assets import Environment, Bundle
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.contrib.cache import RedisCache
import template_filters
import webassets
import settings_common

settings_environment = __import__("settings_%s" % os.environ.setdefault("FLASK_ENV", "production"))

logging.basicConfig(
    format = "\033[1;36m%(levelname)s: %(filename)s (def %(funcName)s %(lineno)s): \033[1;37m %(message)s",
    level=logging.DEBUG
)
logger = logging.getLogger("root")

PROJ_PATH, _ = os.path.split(os.path.abspath(os.path.realpath(__file__)))

app = Flask(__name__, static_url_path="/static")

app.config.from_object(settings_common)
app.config.from_object(settings_environment)

cache = RedisCache(
    host=app.config["CACHE_CONFIG"]["host"],
    port=app.config["CACHE_CONFIG"]["port"],
    db=app.config["CACHE_CONFIG"]["db"]
)

app.jinja_env.filters["time_format"] = template_filters.time_format
app.jinja_env.filters["date_format"] = template_filters.date_format
app.jinja_env.filters["date_format_no_year"] = template_filters.date_format_no_year
app.jinja_env.filters["strip_and_format_state"] = template_filters.strip_and_format_state
app.jinja_env.filters["strip_distance_and_state"] = template_filters.strip_distance_and_state
app.jinja_env.filters["strip_state"] = template_filters.strip_state
app.jinja_env.filters["place_format"] = template_filters.place_format
app.jinja_env.filters["url_structure_format"] = template_filters.url_structure_format
app.jinja_env.filters["convert_km_to_miles"] = template_filters.convert_km_to_miles
app.jinja_env.filters["round_floating_point"] = template_filters.round_floating_point

# asset pipeline
assets = Environment(app)

# rebuild the assets
assets.config["auto_build"] = app.config["ASSETS"]["auto_build"]

core_js = Bundle(
    # already-minified js
    # added to output as-is
    Bundle(
        "scripts/libs/jquery.min.js",
        "scripts/libs/jquery-ui.min.js",
        "scripts/libs/modernizr.min.js",
        "scripts/libs/underscore-min.js",
        "scripts/libs/backbone-min.js",
        "scripts/libs/moment.min.js",
        "scripts/libs/leaflet.min.js",
        "scripts/libs/leaflet.markercluster.min.js",
    ),
    # unminified js
    # gets minified and added to the output file
    Bundle(
        "scripts/app.js",
        "scripts/router/router.js",
        "scripts/models/earthquake.js",
        "scripts/models/map.js",
        "scripts/models/marker.js",
        "scripts/collections/earthquakes.js",
        "scripts/collections/la-habra-earthquakes.js",
        "scripts/collections/markers.js",
        "scripts/views/map.js",
        "scripts/views/la-habra-map.js",
        "scripts/views/clustered-marker.js",
        "scripts/libs/leaflet.usermarker.min.js",
        filters = "rjsmin",
    ),
    output = "assets/min.js"
)
assets.register("core_js", core_js)

detail_js = Bundle(
    # already-minified js
    # added to output as-is
    Bundle(
        "scripts/libs/jquery.min.js",
        "scripts/libs/jquery-ui.min.js",
        "scripts/libs/modernizr.min.js",
        "scripts/libs/moment.min.js",
        "scripts/libs/leaflet.min.js",
    ),
    output = "assets/min.js"
)
assets.register("detail_js", detail_js)

core_css = Bundle(
    "css/jquery-ui.css",
    "css/leaflet.min.css",
    "css/MarkerCluster.css",
    "css/MarkerCluster.Default.css",
    "css/leaflet.usermarker.css",
    "css/style.css",
    "css/map-application.css",
    filters = "cssmin",
    output = "assets/min.css"
)
assets.register("core_css", core_css)

detail_css = Bundle(
    "css/jquery-ui.css",
    "css/leaflet.min.css",
    "css/style.css",
    "css/map-application.css",
    filters = "cssmin",
    output = "assets/detail-min.css"
)
assets.register("detail_css", detail_css)

ie_js = Bundle(
    # js to make ie play nice
    "scripts/selectivizr.js",
    output ="assets/ie-scripts.js"
)
assets.register("ie_js", ie_js)

ie_css = Bundle(
    # css to make ie play nice
    "css/ie-lt9.css",
    filters ="cssmin",
    output ="assets/ie-lt9.css"
)
assets.register("ie_css", ie_css)

# configure database
db = SQLAlchemy(app)

import earthquakes.views

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()
