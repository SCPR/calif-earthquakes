from __future__ import with_statement
import os
import time, datetime
from fabric.operations import prompt
from fabric.api import *
from fabric.contrib.console import confirm
from fabric.colors import green

def localrun():
    ''' run the flask application '''
    local('python runserver.py')

def init():
    ''' initialize the database '''
    local('python manage.py initdb')

def query():
    ''' query the usgs api and write data '''
    local('python manage.py query')

def test():
    ''' runs the test manager command '''
    local('python manage.py test')

def init_migration():
    ''' enable migrations on db '''
    local('python manage.py db init')

def generate_migration():
    ''' generate initial db migration '''
    local('python manage.py db migrate')

def apply_migration():
    ''' apply the migration to db '''
    local('python manage.py db upgrade')