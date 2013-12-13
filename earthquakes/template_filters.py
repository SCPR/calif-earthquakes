import os, datetime, logging

logging.basicConfig(format='\033[1;36m%(levelname)s:\033[0;37m %(message)s', level=logging.DEBUG)

def datetime_format(value):
	date_format = '%B %d, %Y %I:%M %p'
	value = datetime.datetime.fromtimestamp(value / 1e3)
	value = value.strftime(date_format)
	return value