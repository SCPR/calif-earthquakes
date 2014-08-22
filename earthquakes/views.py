#!/usr/bin/env python

import os, logging, json
from flask import Flask, jsonify, render_template, request, \
    Response, send_from_directory, session, g, redirect, \
    url_for, abort, flash, make_response
import flask.ext.sqlalchemy
import flask.ext.restless
from sqlalchemy import or_, and_
from earthquakes import app, cache, db
from earthquakes.models import Earthquake
from haversine import haversine

logging.basicConfig(format="\033[1;36m%(levelname)s:\033[0;37m %(message)s", level=logging.DEBUG)

# set the maximum number of records to return to the view
DB_QUERY_LIMIT = 1000

@app.route("/")
def index():

    cache_expiration = 60 * 10

    # set the cache identifier
    identifier = "view/index"

    # see if cache exists
    cached = cache.get(identifier)

    # if cache exists return it
    if cached is not None:
        return cached

    # if cache doesnt exist generate the page
    else:
        earthquakes = Earthquake.query.order_by(Earthquake.date_time_raw.desc()).limit(DB_QUERY_LIMIT).all()
        recent_earthquakes = earthquakes[:3]
        earthquake_instances = []
        for earthquake in earthquakes:
            if earthquake.mag > 2.5:
                earthquake_instances.append(earthquake)
        tmplt = render_template(
            "index.html",
            recent_earthquakes = recent_earthquakes,
            earthquake_instances = earthquake_instances
        )

        # add pass the identifier and the template to the cache
        cache.set(identifier, tmplt, timeout = cache_expiration)
        return tmplt

@app.route("/<string:title>/<int:id>/", methods=["GET"])
def detail(title, id):

    cache_expiration = 60 * 10

    # set the cache identifier
    identifier = "view/detail_view_for_%d" % id

    # see if cache exists
    cached = cache.get(identifier)

    # if cache exists return it
    if cached is not None:
        return cached

    # otherwise generate the page
    else:

        # get this earthquake
        earthquake = Earthquake.query.filter_by(id=id).first_or_404()
        this_earthquake = (earthquake.latitude, earthquake.longitude)

        # get earthquakes that aren't this one
        earthquake_instances = Earthquake.query.filter(Earthquake.id!=id).order_by(Earthquake.date_time_raw.desc()).limit(DB_QUERY_LIMIT).all()
        recent_earthquakes = earthquake_instances[:6]

        # list to hold earthquakes found
        list_of_nearby_earthquakes = []

        # loop through our list of earthquakes
        for instance in earthquake_instances:

            # build a comparison
            comparision_earthquake = (instance.latitude, instance.longitude)

            # calculate the distance
            evaluated_distance = haversine(this_earthquake, comparision_earthquake)

            # if less than
            if evaluated_distance < 25:

                # add param to object
                instance.distance = evaluated_distance

                # move along if we have six
                if len(list_of_nearby_earthquakes) == 6:
                    pass

                else:
                    # append if we don't
                    list_of_nearby_earthquakes.append(instance)

        tmplt = render_template(
            "detail.html",
            recent_earthquakes = recent_earthquakes,
            earthquake = earthquake,
            nearest_earthquakes = list_of_nearby_earthquakes
        )

        # add pass the identifier and the template to the cache
        cache.set(identifier, tmplt, timeout = cache_expiration)
        return tmplt

@app.route("/internal-staff-lookup", methods=["GET"])
def lookup():

    cache_expiration = 60 * 10

    # set the cache identifier
    identifier = "view/internal_staff_lookup"

    # see if cache exists
    cached = cache.get(identifier)

    # if cache exists return it
    if cached is not None:
        return cached

    # otherwise generate the page
    else:
        earthquake_instances = Earthquake.query.order_by(Earthquake.date_time_raw.desc()).limit(100).all()
        tmplt = render_template(
            "lookup.html",
            earthquake_instances = earthquake_instances
        )

        # add pass the identifier and the template to the cache
        cache.set(identifier, tmplt, timeout = cache_expiration)
        return tmplt

@app.route("/explore-the-map", methods=["GET"])
def map():

    cache_expiration = 60 * 10

    # set the cache identifier
    identifier = "view/explore_the_map"

    # see if cache exists
    cached = cache.get(identifier)

    # if cache exists return it
    if cached is not None:
        logging.debug(cached)
        return cached

    # otherwise generate the page
    else:
        tmplt = render_template(
            "full-screen-map.html"
        )

        # add pass the identifier and the template to the cache
        cache.set(identifier, tmplt, timeout = cache_expiration)
        return tmplt

@app.route("/la-habra-earthquakes", methods=["GET"])
def la_habra_map():

    cache_expiration = 60 * 10

    # set the cache identifier
    identifier = "view/la_habra_earthquakes"

    # see if cache exists
    cached = cache.get(identifier)

    # if cache exists return it
    if cached is not None:
        logging.debug(cached)
        return cached

    # otherwise generate the page
    else:
        tmplt = render_template(
            "la-habra-earthquakes.html"
        )

        # add pass the identifier and the template to the cache
        cache.set(identifier, tmplt, timeout = cache_expiration)
        return tmplt

@app.route("/test-cluster-map", methods=["GET"])
def test_cluster_map():

    cache_expiration = 60 * 10

    # set the cache identifier
    identifier = "view/la_habra_earthquakes"

    # see if cache exists
    #cached = cache.get(identifier)

    # if cache exists return it
    #if cached is not None:
        #logging.debug(cached)
        #return cached

    # otherwise generate the page
    #else:
    tmplt = render_template(
        "test-cluster-map.html"
    )

    # add pass the identifier and the template to the cache
    cache.set(identifier, tmplt, timeout = cache_expiration)
    return tmplt

@app.route("/earthquaketracker/api/v1.0/earthquakes", methods=["GET"])
def api_recent_earthquakes_endpoint():

    cache_expiration = 60 * 20

    # set the cache identifier
    identifier = "view/api_recent_earthquakes_endpoint"

    # see if cache exists
    cached = cache.get(identifier)

    # if cache exists return it
    if cached is not None:
        return cached

    # otherwise generate the json response
    else:
        earthquakes = Earthquake.query.order_by(Earthquake.date_time_raw.desc()).limit(300).all()
        resp = jsonify(
            results = len(earthquakes),
            objects = [i.serialize for i in earthquakes]
        )
        cache.set(identifier, resp, timeout = cache_expiration)
        return resp

@app.route("/earthquaketracker/api/v1.0/earthquakes/<int:id>/", methods=["GET"])
def api_detail_earthquakes_endpoint(id):

    cache_expiration = 60 * 20

    # set the cache identifier
    identifier = "view/api_detail_earthquakes_endpoint_for_%d" % id

    # see if cache exists
    cached = cache.get(identifier)

    # if cache exists return it
    if cached is not None:
        return cached

    # otherwise generate the json response
    else:
        earthquake = Earthquake.query.filter_by(id=id).first_or_404()
        resp = jsonify(earthquake.serialize)
        cache.set(identifier, resp, timeout = cache_expiration)
        return resp

@app.route("/earthquaketracker/api/v1.0/earthquakes/la-habra-quakes", methods=["GET"])
def api_search_earthquakes_endpoint():

    cache_expiration = 60 * 20

    # set the cache identifier
    identifier = "view/api_detail_earthquakes_endpoint_for_la_habra_quakes"

    # see if cache exists
    cached = cache.get(identifier)

    # if cache exists return it
    if cached is not None:
        return cached

    # otherwise generate the json response
    # keying on primary_slug = "m5.1  - 1km s of la habra, california-1396066182010"
    else:
        target_earthquakes = Earthquake.query.filter(Earthquake.date_time_raw > 1396059504300).order_by(Earthquake.date_time_raw.desc()).all()
        la_habra_earthquake = (33.919, -117.943)
        list_of_la_habra_earthquakes = []
        for earthquake in target_earthquakes:
            comparision_earthquake = (earthquake.latitude, earthquake.longitude)
            evaluated_distance = haversine(la_habra_earthquake, comparision_earthquake)
            if evaluated_distance < 40:
                earthquake.distance = evaluated_distance
                list_of_la_habra_earthquakes.append(earthquake)
        resp = jsonify(
            results = len(list_of_la_habra_earthquakes),
            objects = [i.serialize for i in list_of_la_habra_earthquakes]
        )
        cache.set(identifier, resp, timeout = cache_expiration)
        return resp
