"""
This script scrapes URLs for the given year.
"""
# set this value
YEAR = 2018

import os
import pandas as pd
import datetime
from scraper import scrape

from usrightmedia.shared.loggers import get_logger
LOGGER = get_logger(filename = f'04-inca-prep-scrape-{YEAR}', logger_type='main')

dir_inp = os.path.join("..", "..", "data", "02-intermediate", "04-inca-prep")
df_urls = pd.read_pickle(os.path.join(dir_inp, f'mediacloud_urls_{YEAR}.pkl'))
urls_to_fetch = df_urls.to_dict("records")

LOGGER.info(f"start fetch for {YEAR}: {datetime.datetime.now()}")
for n, url in enumerate(urls_to_fetch):
    LOGGER.info(f"fetching url {n}: {url['url']}")
    scrape(url, LOGGER)
LOGGER.info(f"finished fetch for {YEAR}: {datetime.datetime.now()}")