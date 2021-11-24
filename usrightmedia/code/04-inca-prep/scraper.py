import os
import pandas as pd
from inca import Inca


# cd ~/work/home/us-right-media/usrightmedia/code/04-inca-prep


# https://github.com/tmux/tmux/wiki/Getting-Started
# tmux new -s scrape_2016
# python3 scrape_2016.py &
# To detach: the C-b d key binding is used
# To attach: tmux attach -t scrape_2016
# Pressing C-b & prompts for confirmation then kills (closes) the current window. All panes in the window are killed at the same time. C-b x kills only the active pane.
# You can use tmux kill-server to cleanly and gracefully kill all tmux open sessions (and server).


def scrape(url_dict, LOGGER):
    """Collect a URL using the appropriate scraper in INCA.
    Args:
        url_dict
        
        Example:
        {'url_id': '1565840471',
         'outlet': 'Gateway Pundit',
         'publish_date': Timestamp('2020-04-01 17:00:59+0000', tz='UTC'),
         'title': 'Joe Biden Appears To Be Reading From Note Cards During Media Spot (VIDEO)',
         'url': 'https://www.thegatewaypundit.com/2020/04/joe-biden-appears-to-be-reading-from-note-cards-during-media-spot-video/',
         'alt_url': '',
         'ap_syndicated': False,
         'themes': ''}
        
        LOGGER
        
    Returns:
        None
        *URL's info is stored as a document in Elasticsearch
    """
    
    myinca = Inca()
    
    d = url_dict
    url_id = d['url_id']
    outlet = d['outlet']
    
    es_id = f"{outlet.replace(' ', '')}_{url_id}"
    
    if myinca.database.check_exists(es_id)[0]:
        LOGGER.info(f"URL with es_id {es_id} already exists; skip.")
    
    else:
        LOGGER.info(f"Collecting {es_id}...")
        
        if outlet == "American Renaissance":
            myinca.usmedia_scrapers.americanrenaissance(url_info=d)

        elif outlet == "Breitbart":
            myinca.usmedia_scrapers.breitbart(url_info=d)

        elif outlet == "Daily Caller":
            myinca.usmedia_scrapers.dailycaller(url_info=d)

        elif outlet == "Daily Stormer":
            myinca.usmedia_scrapers.dailystormer(url_info=d)

        elif outlet == "Fox News":
            myinca.usmedia_scrapers.foxnews(url_info=d)

        elif outlet == "Gateway Pundit":
            myinca.usmedia_scrapers.gatewaypundit(url_info=d)

        elif outlet == "InfoWars":
            myinca.usmedia_scrapers.infowars(url_info=d)

        elif outlet == "Newsmax":
            myinca.usmedia_scrapers.newsmax(url_info=d)

        elif outlet == "One America News":
            myinca.usmedia_scrapers.oneamericanews(url_info=d)

        elif outlet == "Rush Limbaugh":
            myinca.usmedia_scrapers.rushlimbaugh(url_info=d)

        elif outlet == "Sean Hannity":
            myinca.usmedia_scrapers.seanhannity(url_info=d)

        elif outlet == "VDARE":
            myinca.usmedia_scrapers.vdare(url_info=d)

        elif outlet == "Washington Examiner":
            myinca.usmedia_scrapers.washingtonexaminer(url_info=d)
            
        LOGGER.info(f"Finished collecting {es_id}.")