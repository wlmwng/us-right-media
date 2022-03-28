import datetime
import pandas as pd

import pytz

START_TIME_TEST = datetime.datetime(2020, 12, 1, 0, 0, 0, 0, datetime.timezone.utc)
END_TIME_TEST = datetime.datetime(2021, 1, 1, 0, 0, 0, 0, datetime.timezone.utc)
START_TIME = datetime.datetime(2016, 1, 1, 0, 0, 0, 0, datetime.timezone.utc)
END_TIME = datetime.datetime(2021, 1, 1, 0, 0, 0, 0, datetime.timezone.utc)

"""
    https://www.nist.gov/pml/time-and-frequency-division/popular-links/daylight-saving-time-dst
    - begins at 2:00 a.m. on the second Sunday of March
        (at 2 a.m. the local time time skips ahead to 3 a.m.
        so there is one less hour in the day)
    - ends at 2:00 a.m. on the first Sunday of November
        (at 2 a.m. the local time becomes 1 a.m. and that hour is repeated,
        so there is an extra hour in the day)
        
    - EDT: 4 hours behind UTC        
        2016 DST: Sunday, March 13 at 2:00 a.m. - Sunday, November 06 at 2:00 a.m.
        2017 DST: Sunday, March 12 at 2:00 a.m. - Sunday, November 05 at 2:00 a.m.
        2018 DST: Sunday, March 11 at 2:00 a.m. - Sunday, November 04 at 2:00 a.m.
        2019 DST: Sunday, March 10 at 2:00 a.m. - Sunday, November 03 at 2:00 a.m.
        2020 DST: Sunday, March 08 at 2:00 a.m. - Sunday, November 01 at 2:00 a.m.
    
    - EST: 5 hours behind UTC
"""

def EST_to_UTC(date):
    """convert implicit EST datetime to UTC
       Per Media Cloud, "dates are all in America/New_York (EST)"
       "publish dates are what's specified on the RSS feeds
       (so assuming that we've been provided with accurate data, you should be all set)."

    Args:
        date (datetime)

    Returns:
        date_utc (datetime): timezone-aware datetime in UTC

    """
    try:

        # https://stackoverflow.com/a/55524561
        date_utc = date.replace(tzinfo=pytz.timezone("US/Eastern")).astimezone(pytz.utc)
    except ValueError as e:
        date_utc = pd.NaT
    return date_utc



