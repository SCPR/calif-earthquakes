from __future__ import with_statement
import os, logging
import time, datetime
from fabric.operations import prompt
from fabric.api import *
from fabric.contrib.console import confirm
from fabric.colors import green

env.user            = 'archive'
env.hosts           = ['66.226.4.228']
env.project_root    = '/web/archive/apps/earthquakes/src'
env.bin_root        = "/web/archive/apps/earthquakes/virtualenvs/earthquakes/bin/"

logging.basicConfig(format='\033[1;36m%(levelname)s:\033[0;37m %(message)s', level=logging.DEBUG)

# server commands
def update_code():
    """
    Production function to update the code on the remote server
    """
    with cd(env.project_root):
        run('git pull')

def update_dependencies():
    """
    Production function to update the application's dependencies
    """
    with cd(env.project_root):
        run(__env_cmd("pip install -r requirements.txt"))

def restart():
    """
    Production function to restart the server
    """
    with cd(env.project_root):
        run('mkdir -p tmp/ && touch tmp/restart.txt')

def deploy():
    """
    Production function to pull the latest code from source control & restarts the server
    """
    with cd(env.project_root):
        update_code()
        update_dependencies()
        restart()

def revert():
    """
    Production function to revert git via reset --hard @{1}
    """
    with cd(env.project_root):
        run('git reset --hard @{1}')
        update_dependencies()
        restart()

def server_query(api_url=''):
    """
    Production to query the USGS api and ingest to db
    """
    with cd(env.project_root):
        run("export FLASK_ENV=production")
        run(__env_cmd("python manage.py query --api_url " + api_url))

def server_migration_init():
    """
    enable migrations on db
    """
    with cd(env.project_root):
        run("export FLASK_ENV=production")
        run(__env_cmd("python manage.py db init"))

def server_migration_migrate():
    """
    generate initial db migration
    """
    with cd(env.project_root):
        run("export FLASK_ENV=production")
        run(__env_cmd("python manage.py db migrate"))

def server_migration_upgrade():
    """
    apply the migration to db
    """
    with cd(env.project_root):
        run("export FLASK_ENV=production")
        run(__env_cmd("python manage.py db upgrade"))

def server_drop_earthquakes():
    ''' deletes all instances of the Earthquake model in the table '''
    with cd(env.project_root):
        run("export FLASK_ENV=production")
        run(__env_cmd("python manage.py drop_earthquakes"))

def server_drop_nearby_cities():
    ''' deletes all instances of the NearbyCities model in the table '''
    with cd(env.project_root):
        run("export FLASK_ENV=production")
        run(__env_cmd("python manage.py drop_cities"))

def __env_cmd(cmd):
    return env.bin_root + cmd

# local commands

def localrun():
    """
    run the flask application
    """
    local('python runserver.py')

def localinit():
    """
    initialize the database
    """
    local('python manage.py initdb')

def localquery(api_url=''):
    ''' query the usgs api and write data '''
    local('python manage.py query --api_url ' + api_url)

def test():
    ''' runs the test manager command '''
    local('python manage.py test')

def local_migration_init():
    ''' enable migrations on db '''
    local('python manage.py db init')

def local_migration_migrate():
    ''' generate initial db migration '''
    local('python manage.py db migrate')

def local_migration_upgrade():
    ''' apply the migration to db '''
    local('python manage.py db upgrade')

def local_drop_earthquakes():
    ''' deletes all instances of the Earthquake model in the table '''
    local('python manage.py drop_earthquakes')

def local_drop_nearby_cities():
    ''' deletes all instances of the NearbyCities model in the table '''
    local('python manage.py drop_cities')

def local_test_argument(api_url=''):
    logging.debug(api_url)
    local('python manage.py local_test_argument --api_url ' + api_url)