#===========================================================
# Session Related Functions
# - Note that these require tzdata to be imported
#===========================================================

from datetime import datetime
from zoneinfo import ZoneInfo


#===========================================================
# Note: The following functions are used as Jinja template
#       filters, rather than being called directly


#-----------------------------------------------------------
# Convert a given UTC timestamp to a local time string
# - The timestamp format is YYYY-MM-DD HH:MM:SS
# - The optional local_format string as per https://strftime.org/
#-----------------------------------------------------------
def _utc_timestamp_to_local(utc_timestamp_str, local_format="%a, %d/%m/%Y at %I:%M%p"):
    utc_dt = datetime.strptime(utc_timestamp_str, "%Y-%m-%d %H:%M:%S")
    utc_dt = utc_dt.replace(tzinfo=ZoneInfo("UTC"))

    # Convert to local timezone (Pacific/Auckland handles DST automatically)
    local_dt = utc_dt.astimezone(ZoneInfo("Pacific/Auckland"))

    # Format to a user-friendly string
    return local_dt.strftime(local_format)


#-----------------------------------------------------------
# Convert a given UTC timestamp to local DD/MM/YYY format
#-----------------------------------------------------------
def _utc_timestamp_to_local_date(utc_timestamp_str):
    return _utc_timestamp_to_local(utc_timestamp_str, "%d/%m/%Y")


#-----------------------------------------------------------
# Convert a given UTC timestamp to local DD/MM/YYY format
#-----------------------------------------------------------
def _utc_timestamp_to_local_day(utc_timestamp_str):
    return _utc_timestamp_to_local(utc_timestamp_str, "%a")


#-----------------------------------------------------------
# Convert a given UTC timestamp to local DD/MM/YYY format
#-----------------------------------------------------------
def _utc_timestamp_to_local_time(utc_timestamp_str):
    return _utc_timestamp_to_local(utc_timestamp_str, "%I:%M%p")


#-----------------------------------------------------------
# Register the above functions as Jinja filters
#-----------------------------------------------------------
def init_datetime(app):
    # Register Jinja filters
    app.jinja_env.filters['localtimestamp'] = _utc_timestamp_to_local
    app.jinja_env.filters['localdate']      = _utc_timestamp_to_local_date
    app.jinja_env.filters['localday']       = _utc_timestamp_to_local_day
    app.jinja_env.filters['localtime']      = _utc_timestamp_to_local_time



#===========================================================
# Note: The following functions are used directly when
#       processing dates/times from HTML form inputs


#-----------------------------------------------------------
# Create a UTC timestamp from a given local date and
# optionally a local time
# - local_date_str is in format "YYYY-MM-DD"
# - local_time_str is in format "HH:MM" or "HH:MM:SS"
# - Returns UTC timestamp in format "YYYY-MM-DD HH:MM:SS"
#-----------------------------------------------------------
def utc_timestamp(local_date_str, local_time_str="00:00:00"):
    # Assume input is in local timezone (e.g., Pacific/Auckland)
    local_tz = ZoneInfo("Pacific/Auckland")

    # If no seconds provided, add some
    if len(local_time_str) == 5:
        local_time_str += ":00"

    # Parse the combined date and time string
    local_dt_str = f"{local_date_str} {local_time_str}"
    local_dt = datetime.strptime(local_dt_str, "%Y-%m-%d %H:%M:%S")
    local_dt = local_dt.replace(tzinfo=local_tz)

    # Convert to UTC
    utc_dt = local_dt.astimezone(ZoneInfo("UTC"))

    # Format as UTC timestamp string
    return utc_dt.strftime("%Y-%m-%d %H:%M:%S")


#-----------------------------------------------------------
# Create a UTC timestamp from the current date and time
# - Returns UTC timestamp in format "YYYY-MM-DD HH:MM:SS"
#-----------------------------------------------------------
def utc_timestamp_now():
    # Get date/time now
    local_dt = datetime.now()
    local_date_str = local_dt.strftime("%Y-%m-%d")
    local_time_str = local_dt.strftime("%H:%M:%S")

    # Convert to UTC
    return utc_timestamp(local_date_str, local_time_str)

