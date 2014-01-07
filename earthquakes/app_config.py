DEBUG = True

config_settings = {
    'DEBUG': True,
    'APIKEY': 'kI9xkkQSnL',
    'sqlalchemy_database_uri':  'mysql://root:19NnpnnP19@localhost/test',
    'headers': {
        'From': 'ckeller@scpr.org',
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.53 Safari/525.19'
    },
    'all_past_hour': 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson',
    'all_past_day': 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson',
    'all_past_seven': 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson',
    'all_past_thirty': 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson',
}