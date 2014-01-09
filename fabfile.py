from __future__ import with_statement
import os
import time, datetime
from fabric.operations import prompt
from fabric.api import *
from fabric.contrib.console import confirm
from fabric.colors import green

env.user            = 'archive'
env.hosts           = ['66.226.4.228']
env.project_root    = '/web/archive/apps/earthquakes/src'
env.python_exe      = "/web/archive/apps/earthquakes/virtualenvs/earthquakes/bin/python"

def update_code():
    """
    Production function to update the code on the remote server
    """
    with cd(env.project_root):
        run('git pull')

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
        restart()

def revert():
    """
    Production function to revert git via reset --hard @{1}
    """
    with cd(env.project_root):
        run('git reset --hard @{1}')
        restart()



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