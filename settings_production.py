import os
import yaml

# env = 'production'

CONFIG_FILE = os.environ.setdefault("CONFIG_PATH","./development.yml")

CONFIG = yaml.load(open(CONFIG_FILE))

DEBUG = CONFIG.get("debug",False)

ASSETS_DEBUG = CONFIG.get("assets_debug",False)

SITE_URL = CONFIG["site_url"]

ASSETS = {
    "auto_build": CONFIG["assets"]["auto_build"]
}

CACHE_CONFIG = CONFIG["cache"]

if CONFIG_FILE == "./development.yml":
    SQLALCHEMY_DATABASE_URI = CONFIG["database"]["sqlalchemy_database_uri"]
else:
    SQLALCHEMY_DATABASE_URI = "mysql://%s:%s@%s:%s/%s" % (
        CONFIG["database"]["username"],
        CONFIG["database"]["password"],
        CONFIG["database"]["host"],
        CONFIG["database"]["port"],
        CONFIG["database"]["database"]
    )

MAIL_SERVER = CONFIG["email"]["host"]
MAIL_PORT = CONFIG["email"]["port"]
MAIL_USE_TLS = CONFIG["email"]["use_tls"]
MAIL_USE_SSL = CONFIG["email"]["use_ssl"]
MAIL_USERNAME = CONFIG["email"]["username"]
MAIL_PASSWORD = CONFIG["email"]["password"]
