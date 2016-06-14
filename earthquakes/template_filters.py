import os
import logging
import time
import datetime
import calendar
import pytz
from pytz import timezone
from datetime import tzinfo, date

logger = logging.getLogger("root")
logging.basicConfig(
    format="\033[1;36m%(levelname)s: %(filename)s (def %(funcName)s %(lineno)s): \033[1;37m %(message)s",
    level=logging.DEBUG
)


def format_date_for_display(date, date_format):
    pacific = pytz.timezone("US/Pacific")
    utc = timezone("UTC")
    date = date.replace(tzinfo=pytz.UTC).astimezone(pacific)
    date_string = date.strftime(date_format)
    return date_string


def date_format(date, html_tag):
    if html_tag:
        date_format = "%B %-d, <" + html_tag + ">%Y</" + html_tag + ">"
    else:
        date_format = "%B %-d, %Y"
    value = format_date_for_display(date, date_format)
    return value


def time_format(date):
    date = format_date_for_display(date, "%-I:%M:%S %p %Z")
    return date


def date_format_no_year(date):
    date = format_date_for_display(date, "%B %-d")
    return date


def strip_and_format_state(value, html_tag):
    split_value = split_location_from_state(value)
    if html_tag:
        if len(split_value) == 1:
            formatted_value = "<%s>%s</%s>" % (html_tag,
                                               split_value[0], html_tag)
        elif len(split_value) == 2:
            formatted_value = "%s of <%s>%s</%s>" % (
                split_value[0], html_tag, split_value[1], html_tag)
    else:
        if len(split_value) == 1:
            formatted_value = "%s" % (split_value[0])
        elif len(split_value) == 2:
            formatted_value = "%s of %s" % (split_value[0], split_value[1])
    return formatted_value


def strip_distance_and_state(value):
    split_value = split_location_from_state(value)
    if len(split_value) == 1:
        formatted_value = "%s" % (split_value[0])
    elif len(split_value) == 2:
        formatted_value = "%s" % (split_value[1])
    return formatted_value


def place_format(value, date):
    split_value = split_location_from_state(value)
    date_string = format_date_for_display(date, "%B %-d, %Y")
    if len(split_value) == 1:
        formatted_value = "%s: %s" % (split_value[0], date_string)
    elif len(split_value) == 2:
        formatted_value = "%s: %s" % (split_value[1], date_string)
    return formatted_value


def url_structure_format(value, date):
    split_value = split_location_from_state(value)
    date_string = format_date_for_display(date, "%B-%-d-%Y")
    if len(split_value) == 1:
        formatted_value = str(split_value[0]).replace(" ", "-").lower()
    elif len(split_value) == 2:
        formatted_value = str(split_value[1]).replace(" ", "-").lower()
    instance_date = date_string.lower()
    formatted_value = "%s-%s" % (formatted_value, instance_date)
    return formatted_value


def strip_state(value):
    try:
        value = value.replace(", California", "")
    except:
        value = value
    return value


def split_location_from_state(value):
    value = strip_state(value)
    split_value = value.split(" of ")
    if len(split_value) >= 3:
        output = []
        output.append(split_value[0])
        output.append(split_value[-1])
    elif len(split_value) == 2:
        output = split_value
    else:
        output = split_value
    return output


def convert_km_to_miles(value):
    if not isinstance(value, (int, long, float)):
        value = float(value)
    else:
        value = value
    output = value / 1.609344
    logger.debug(output)
    return "{0:.3g}".format(output)


def round_floating_point(value):
    value = "{0:.2g}".format(value)
    if len(value) == 1:
        value = "%s.0" % (value)
    else:
        value = value
    return value
