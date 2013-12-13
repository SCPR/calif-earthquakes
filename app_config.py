DEBUG = True
SQLALCHEMY_DATABASE_URI = 'mysql://root:19NnpnnP19@localhost/calif_earthquakes'
APIKEY = 'kI9xkkQSnL'

config_settings = {
    'headers': {
        'From': 'ckeller@scpr.org',
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.53 Safari/525.19'
    },
    'month_sig': 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/significant_month.geojson',
    'seven_days_sig': 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/significant_week.geojson'
}