import datetime
import pandas as pd

import pytz

START_TIME_TEST = datetime.datetime(2020, 12, 1, 0, 0, 0, 0, datetime.timezone.utc)
END_TIME_TEST = datetime.datetime(2021, 1, 1, 0, 0, 0, 0, datetime.timezone.utc)
START_TIME = datetime.datetime(2016, 1, 1, 0, 0, 0, 0, datetime.timezone.utc)
END_TIME = datetime.datetime(2021, 1, 1, 0, 0, 0, 0, datetime.timezone.utc)


def EST_to_UTC(date):
    """convert implicit EST datetime to UTC

    Args:
        date (datetime)

    Returns:
        date_utc (datetime): timezone-aware datetime in UTC

    """
    try:
        # checked with Media Cloud: "dates are all in America/New_York (EST)"
        # "publish dates are what's specified on the RSS feeds (so assuming that we've been provided with accurate data, you should be all set)."
        # https://stackoverflow.com/a/55524561
        date_utc = date.replace(tzinfo=pytz.timezone("US/Eastern")).astimezone(pytz.utc)
    except ValueError as e:
        date_utc = pd.NaT
    return date_utc
