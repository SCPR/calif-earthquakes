DEBUG=True

config_settings = {
    'DEBUG': True,
    'APIKEY': 'kI9xkkQSnL',
    'sqlalchemy_database_uri':  'mysql://root:19NnpnnP19@localhost/test',
    'headers': {
        'From': 'ckeller@scpr.org',
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.53 Safari/525.19'
    },
    'month_sig': 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/significant_month.geojson',
    'seven_days_sig': 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/significant_week.geojson',
    'seven_days_2.5': 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_week.geojson'
}