DEBUG = True
APIKEY = 'kI9xkkQSnL'

#DATABASE = 'earthquake.db'
#SECRET_KEY = 'QKq1256cy<V|Z3Y>B0cq7o?V$3o(6'
#USERNAME = 'admin'
#PASSWORD = 'default'

config_settings = {
    'sqlalchemy_database_uri':  'mysql://root:19NnpnnP19@localhost/test',
    'headers': {
        'From': 'ckeller@scpr.org',
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.53 Safari/525.19'
    },
    'month_sig': 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/significant_month.geojson',
    'seven_days_sig': 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/significant_week.geojson'
}