from __future__ import with_statement
import os
import logging
import time
import datetime
from fabric.operations import prompt
from fabric.api import *
from fabric.contrib.console import confirm
from fabric.colors import green

logger = logging.getLogger("root")
logging.basicConfig(
    format="\033[1;36m%(levelname)s: %(filename)s (def %(funcName)s %(lineno)s): \033[1;37m %(message)s",
    level=logging.DEBUG
)

# TODO: Move this to Rundeck


def server_query(api_url=''):
    """
    Production to query the USGS api and ingest to db
    """
    with cd(env.project_root):
        run("export FLASK_ENV=production")
        run(__env_cmd("python manage.py query --api_url " + api_url))

# Can this be removed?


def server_migration_init():
    """
    enable migrations on db
    """
    with cd(env.project_root):
        run("export FLASK_ENV=production")
        run(__env_cmd("python manage.py db init"))

# Can this be removed?


def server_migration_migrate():
    """
    generate initial db migration
    """
    with cd(env.project_root):
        run("export FLASK_ENV=production")
        run(__env_cmd("python manage.py db migrate"))

# TODO: Move this to Rundeck


def server_drop_earthquakes():
    ''' deletes all instances of the Earthquake model in the table '''
    with cd(env.project_root):
        run("export FLASK_ENV=production")
        run(__env_cmd("python manage.py drop_earthquakes"))

# TODO: Move this to Rundeck


def server_drop_nearby_cities():
    ''' deletes all instances of the NearbyCities model in the table '''
    with cd(env.project_root):
        run("export FLASK_ENV=production")
        run(__env_cmd("python manage.py drop_cities"))

# TODO: Move this to Rundeck


def server_drop_row(record_id=''):
    """
    deletes a specific record
    """
    with cd(env.project_root):
        run("export FLASK_ENV=production")
        run(__env_cmd("python manage.py drop_row --record " + record_id))

# TODO: Move this to Rundeck


def server_find_dupes():
    ''' finds duplicate records '''
    with cd(env.project_root):
        run("export FLASK_ENV=production")
        run(__env_cmd("python manage.py find_dupes"))


def __env_cmd(cmd):
    return env.bin_root + cmd

# local commands
def localinit():
    """
    initialize the database
    """
    local('python manage.py initdb')


def localrun():
    """
    run the flask application
    """
    local('python runserver.py')


def localquery(api_url=''):
    ''' query the usgs api and write data '''
    local('python manage.py query --api_url ' + api_url)


def test():
    """
    runs the test manager command
    """
    local('python tests.py')


def local_migration_init():
    """
    enable migrations on db
    """
    local('python manage.py db init')


def local_migration_migrate():
    """
    generate initial db migration
    """
    local('python manage.py db migrate')


def local_migration_upgrade():
    """
    apply the migration to db
    """
    local('python manage.py db upgrade')


def local_drop_earthquakes():
    """
    deletes all instances of the Earthquake model in the table
    """
    local('python manage.py drop_earthquakes')


def local_drop_nearby_cities():
    """
    deletes all instances of the NearbyCities model in the table
    """
    local('python manage.py drop_cities')


def local_drop_row(record_id=''):
    """
    deletes a specific record
    """
    local('python manage.py drop_row --record ' + record_id)


def local_find_dupes():
    """
    finds duplicate records
    """
    local('python manage.py find_dupes')
