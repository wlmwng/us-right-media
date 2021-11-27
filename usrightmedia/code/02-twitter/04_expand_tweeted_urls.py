"""
This script expands URLs (re-)tweeted by congressional Republicans during 2016-2020.

Note: this project uses a [forked version of urlExpander](https://github.com/wlmwng/urlExpander)
To check progress, `cd` to the output directory:
- `wc -l urlexpander_modified.json` (number of URL entries in cache)
- `tail -n 100 urlexpander_cache.jsonl | grep [URL domain]` (show last n URL entries which include the URL domain)
- `tail -n 100 urlexpander_cache.jsonl | grep -v "\"response_code\": 2.*"` (show last n URL entries if their response codes were *not* 2XX; likely 4XX or 5XX)
"""

import os
import datetime
import pandas as pd
import urlexpander

# matplotlib is logged even though disable_existing_loggers=yes in logging_config.yaml
# https://stackoverflow.com/a/51529172/7016397
# workaround is to manually set the level before creating my logger
import logging

logging.getLogger("matplotlib").setLevel(logging.WARNING)
from usrightmedia.shared.loggers import get_logger

LOGGER = get_logger(filename=f"04-twitter-prep-urls-urlexpander", logger_type="main")

dir_fig = os.path.join("..", "..", "figures")
dir_url = os.path.join("..", "..", "data", "02-intermediate", "02-twitter")
urls = pd.read_pickle(os.path.join(dir_url, f"politicians_tweeted_urls.pkl"))
urls["created_week"] = urls["created_at"].dt.to_period("W").dt.to_timestamp()
urls["created_month"] = urls["created_at"].dt.to_period("M").dt.to_timestamp()
urls["created_year"] = urls["created_at"].dt.to_period("Y").dt.to_timestamp()
LOGGER.info(
    f"URLs (re-)tweeted by congressional Republicans during 2016-2020: {len(urls)}"
)

LOGGER.info(f"started url expansion at {datetime.datetime.now()}")
resolved_urls = urlexpander.expand(
    list(urls["most_unrolled_url"]),
    chunksize=1280,
    n_workers=4,
    timeout=10,
    cache_file=os.path.join(dir_url, "urlexpander_cache.jsonl"),
    verbose=1,
    filter_function=None,
)
LOGGER.info(f"finished url expansion at {datetime.datetime.now()}")

urls["resolved_url"] = resolved_urls

urls = urls[
    [
        "tweet_id",
        "created_at",
        "created_week",
        "created_month",
        "created_year",
        "text",
        "author_id",
        "username",
        "tweet_url",
        "url_id",
        "url",
        "expanded_url",
        "display_url",
        "unwound_url",
        "most_unrolled_url",
        "most_unrolled_field",
        "is_dupe",
        "is_from_tw",
        "resolved_url",
    ]
]

urls.to_pickle(os.path.join(dir_url, f"politicians_tweeted_urls_resolved.pkl"))
