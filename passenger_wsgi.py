import sys, os, yaml

env = os.environ.setdefault("FLASK_ENV", "production")
app_config = yaml.load(open("config/app.yml", 'r'))[env]

INTERP = os.path.join(app_config['bin_root'], 'python')

if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

sys.path.append(os.getcwd())

from earthquakes import app as application
