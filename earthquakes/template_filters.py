import os, logging, time, datetime, calendar
import pytz
from pytz import timezone
from datetime import tzinfo, date

logging.basicConfig(format='\033[1;36m%(levelname)s:\033[0;37m %(message)s', level=logging.DEBUG)

def time_format(value):
	pacific = pytz.timezone('US/Pacific')
	utc = timezone('UTC')
	date_format = '%-I:%M:%S %p %Z'
	value = value.replace(tzinfo=pytz.UTC).astimezone(pacific)
	value = value.strftime(date_format)
	return value

def date_format(value, html_tag):
    if html_tag:
        date_format = '%B %-d, <' + html_tag + '>%Y</' + html_tag + '>'
    else:
        date_format = '%B %-d, %Y'
    value = value.strftime(date_format)
    return value

def date_format_no_year(value):
	date_format = '%B %-d'
	value = value.strftime(date_format)
	return value

def strip_and_format_state(value, html_tag):
    value = value.replace(', California', '')
    split_value = value.split(' of ')
    if html_tag:
        formatted_value = '%s of <%s>%s</%s>' % (split_value[0], html_tag, split_value[1], html_tag)
    else:
        formatted_value = '%s of %s' % (split_value[0], split_value[1])
    return formatted_value

def strip_distance_and_state(value):
    value = value.replace(', California', '')
    split_value = value.split(' of ')
    formatted_value = '%s' % (split_value[1])
    return formatted_value

def strip_state(value):
    try:
        value = value.replace(', California', '')
    except:
        value = value
    return value

def place_format(value, date):
    value = value.replace(', California', '')
    split_value = value.split(' of ')
    date_format = '%B %-d, %Y'
    date_string = date.strftime(date_format)
    formatted_value = '%s: %s' % (split_value[1], date_string)
    return formatted_value

def url_structure_format(value, date):
    value = value.replace(', California', '')
    split_value = value.split(' of ')
    date_format = '%B-%-d-%Y'
    date_string = date.strftime(date_format)
    instance_location = str(split_value[1]).replace(' ', '-').lower()
    instance_date = date_string.lower()
    formatted_value = '%s-%s' % (instance_location, instance_date)
    return formatted_value

def convert_km_to_miles(value):
    value = value / 1.609344
    return '{0:.3g}'.format(value)

def round_floating_point(value):
    value = '{0:.2g}'.format(value)
    if len(value) == 1:
        value = '%s.0' % (value)
    else:
        value = value
    return value