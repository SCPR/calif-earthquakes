import sys
import os
import yaml
import newrelic.agent
from earthquakes import app as application

sys.path.append(os.getcwd())

newrelic.agent.initialize("config/newrelic.ini")
