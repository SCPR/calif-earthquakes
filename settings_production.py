import yaml

env = 'production'

DEBUG = False
ASSETS_DEBUG = False
SITE_URL = "http://earthquakes.scpr.org"

ASSETS = {
    "auto_build" : False
}

CONFIG_DB       = yaml.load(open("config/database.yml", 'r'))[env]
CONFIG_MAIL     = yaml.load(open("config/mail.yml", 'r'))[env]

CACHE_CONFIG    = yaml.load(open("config/cache.yml", 'r'))[env]
EMAIL_DISTRIBUTION  = yaml.load(open("config/contacts.yml", 'r'))[env]['contacts']

SQLALCHEMY_DATABASE_URI = "mysql://%s:%s@%s:%s/%s" % (
    CONFIG_DB['username'],
    CONFIG_DB['password'],
    CONFIG_DB['host'],
    CONFIG_DB['port'],
    CONFIG_DB['database']
)

MAIL_SERVER     = CONFIG_MAIL['server']
MAIL_PORT       = CONFIG_MAIL['port']
MAIL_USE_TLS    = CONFIG_MAIL['use_tls']
MAIL_USE_SSL    = CONFIG_MAIL['use_ssl']
MAIL_USERNAME   = CONFIG_MAIL['username']
MAIL_PASSWORD   = CONFIG_MAIL['password']
