import sys, os

remote_app_root = "/web/archive/apps/earthquakes"
INTERP = os.path.join(remote_app_root, 'virtualenvs', 'earthquakes', 'bin', 'python')

# remote_app_root = "/Users/bryan/projects/calif-earthquakes"
# INTERP = "/Users/bryan/.virtualenvs/calif-earthquakes/bin/python"

if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

sys.path.append(os.getcwd())
os.environ.setdefault("FLASK_ENV", "production")

from earthquakes import app as application
