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