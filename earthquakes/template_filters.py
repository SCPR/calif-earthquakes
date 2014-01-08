import os, logging, time, datetime, calendar
import pytz
from pytz import timezone
from datetime import tzinfo, date

logging.basicConfig(format='\033[1;36m%(levelname)s:\033[0;37m %(message)s', level=logging.DEBUG)

def datetime_format(value):
	pacific = pytz.timezone('US/Pacific')
	utc = timezone('UTC')
	date_format = '%B %d, %Y %I:%M %p'
	value = value.replace(tzinfo=pytz.UTC).astimezone(pacific)
	value = value.strftime(date_format)
	return value

def date_format(value):
	date_format = '%B %d, %Y'
	value = value.strftime(date_format)
	return value

def strip_state(value):
    value = value.replace(', California', '')
    split_value = value.split(' of ')
    formatted_value = '%s of <mark>%s</mark>' % (split_value[0], split_value[1])
    return formatted_value

def place_format(value, date):
    value = value.replace(', California', '')
    split_value = value.split(' of ')
    date_format = '%B %d, %Y'
    date_string = date.strftime(date_format)
    formatted_value = '%s: %s' % (split_value[1], date_string)
    return formatted_value