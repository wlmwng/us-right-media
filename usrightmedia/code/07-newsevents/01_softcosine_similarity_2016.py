# Softcosine Similarity
# Purpose: compute softcosine similarity between outlets' documents
# Code based on https://github.com/damian0604/newsevents/blob/master/src/data-processing/020-softcosine_newsevents.py

import os
from datetime import datetime
import gensim
from inca import Inca
import logging

# matplotlib is logged even though disable_existing_loggers=yes in logging_config.yaml
# https://stackoverflow.com/a/51529172/7016397
# workaround is to manually set the level before creating my logger
logging.getLogger("matplotlib").setLevel(logging.WARNING)
from usrightmedia.shared.loggers import get_logger

FROM_YEAR = "2016"
TO_YEAR = "2017"

LOGGER = get_logger(filename=f"01-softcosine-similarity-{FROM_YEAR}", logger_type="main")
LOGGER.info(f"gensim version: {gensim.__version__}")

myinca = Inca()

outlet_doctypes = [
    "americanrenaissance",
    "breitbart",
    "dailycaller",
    "dailystormer",
    "foxnews",
    "gatewaypundit",
    "infowars",
    "newsmax",
    "oneamericanews",
    "rushlimbaugh",
    "seanhannity",
    "vdare",
    "washingtonexaminer",
]

START_TIME = datetime.now()
LOGGER.info(f"Starting softcosine similarity calculation for {FROM_YEAR} at {START_TIME}")

myinca.analysis.softcosine_similarity.fit(
    path_to_model=os.path.join(
        "..",
        "..",
        "data",
        "gensim-data",
        "word2vec-google-news-300",
        "word2vec-google-news-300.gz",
    ),
    source=outlet_doctypes,
    target=outlet_doctypes,
    sourcetext="article_maintext_4",
    sourcedate="publish_date",
    targettext="article_maintext_4",
    targetdate="publish_date",
    keyword_source=None,
    keyword_target=None,
    keyword_source_must=False,
    keyword_target_must=False,
    condition_source={"should_include": True},
    condition_target={"should_include": True},
    days_before=0,
    days_after=2,
    merge_weekend=False,  # do not assume weekend can be collapsed
    threshold=0.2,
    from_time=f"{FROM_YEAR}-01-01",  # gte
    to_time=f"{TO_YEAR}-01-01",  # lte
    to_csv=False,  # return a pickled pandas dataframe instead of a CSV file
    destination=os.path.join(
        "..", "..", "data", "02-intermediate", "07-newsevents", "01-softcosine-output", FROM_YEAR
    ),
    to_pajek=False,  # not available in combination with days_before/days_after parameters
    filter_above=0.5,  # default
    filter_below=5,
)  # default

END_TIME = datetime.now()
LOGGER.info(f"Finished softcosine similarity calculation for {FROM_YEAR} at {END_TIME}")
