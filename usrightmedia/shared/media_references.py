import pandas as pd


def get_mediacloud_outlet_ids():
    # 13 selected outlets
    outlets = {
        "American Renaissance": "26186",
        "Breitbart": "19334",
        "Daily Caller": "18775",
        "Daily Stormer": "113988",
        "Fox News": "1092",
        "Gateway Pundit": "25444",
        "InfoWars": "18515",
        "Newsmax": "25349",
        "One America News": "127733",
        "Rush Limbaugh": "24669",
        "Sean Hannity": "28136",
        "VDARE": "24641",
        "Washington Examiner": "6443",
    }

    df = pd.DataFrame(outlets.items(), columns=["outlet", "media_id"]).astype(str)

    return df


def get_media_netlocs(include_general=False,
                    include_specialized = False,
                    include_regional = False,
                    include_public_service = False,
                    include_unknown = False,
                    include_gop = False,
                    include_misc = False):

    netloc_groups = [['ABC News', 'abcnews.go.com', include_general, False],
                    ['ABC News', 'abcn.ws', include_general, False], # ABC Radio
                    ['American Renaissance', 'amren.com', include_general, True],
                    ['AP News', 'apnews.com', include_general, False],
                    ['Axios', 'axios.com', include_general, False],
                    ['BBC', 'bbc.com', include_general, False],
                    ['Bloomberg', 'bloomberg.com', include_general, False],
                    ['Breitbart', 'breitbart.com', include_general, True],
                    ['Buzzfeed News', 'buzzfeednews.com', include_general, False],
                    ['CBS News', 'cbsnews.com', include_general, False],
                    ['CBS News', 'cbsn.ws', include_general, False],
                    ['CBS News', 'cbsloc.al', include_general, False], # could be put in 'regional'
                    ['CNBC', 'cnbc.com', include_general, False],
                    ['CNBC', 'cnb.cx', include_general, False],
                    ['CNN', 'cnn.com', include_general, False],
                    ['CNN', 'edition.cnn.com', include_general, False],
                    ['CNN', 'cnn.it', include_general, False],
                    ['CNS News', 'cnsnews.com', include_general, False], # conservative news site
                    ['Daily Caller', 'dailycaller.com', include_general, True],
                    ['Daily Caller', 'amp.dailycaller.com', include_general, True],
                    ['Daily Signal', 'dailysignal.com', include_general, False],
                    ['Daily Stormer', 'dailystormer.com', include_general, True],
                    ['Daily Stormer', 'dailystormer.name', include_general, True],
                    ['Daily Stormer', 'dailystormer.su', include_general, True],
                    ['Fox', 'fxn.ws', include_general, True],
                    ['Fox', 'foxbusiness.com', include_general, True],
                    ['Fox', 'foxnews.com', include_general, True],
                    ['Fox', '925foxnews.com', include_general, True],
                    ['Fox', 'insider.foxnews.com', include_general, True],
                    ['Fox', 'latino.foxnews.com', include_general, True],
                    ['Fox', 'nation.foxnews.com', include_general, True],
                    ['Fox', 'radio.foxnews.com', include_general, True],
                    ['Fox', 'video.foxbusiness.com', include_general, True],
                    ['Fox', 'video.foxnews.com', include_general, True],
                    ['Fox', 'press.foxnews.com', include_general, True],
                    ['Infowars', 'infowars.com', include_general, True],
                    ['Infowars', 'archives.infowars.com', include_general, True],
                    ['Just the News', 'justthenews.com', include_general, False], # https://capitolcommunicator.com/award-winning-journalist-john-solomon-launches-new-media-outlet/
                    ['Los Angeles Times', 'latimes.com', include_general, False],
                    ['National Review', 'nationalreview.com', include_general, False],
                    ['NBC News', 'nbcnews.com', include_general, False],
                    ['NBC News', 'nbcnews.to', include_general, False],
                    ['Newsmax', 'newsmax.com', include_general, True],
                    ['Newsmax', 'newsmaxtv.com', include_general, True],
                    ['Newsweek', 'newsweek.com', include_general, False],
                    ['New York Post', 'nypost.com', include_general, False],
                    ['New York Times', 'nytimes.com', include_general, False],
                    ['New York Times', 'nyti.ms', include_general, False],
                    ['NPR', 'npr.org', include_general, False], # national public radio
                    ['NPR', 'n.pr', include_general, False],
                    ['One America News Network', 'oann.com', include_general, True],
                    ['Politico', 'politico.com', include_general, False],
                    ['Politico', 'politi.co', include_general, False],
                    ['Real Clear Politics', 'realclearpolitics.com', include_general, False],
                    ['Reuters', 'reuters.com', include_general, False],
                    ['Reuters', 'reut.rs', include_general, False],
                    ['Ripon Advance', 'riponadvance.com', include_general, False], # https://riponadvance.com/about-us/
                    ['Roll Call', 'rollcall.com', include_general, False], # congressional news, legislative tracking and advocacy services
                    ['Rush Limbaugh', 'rushlimbaugh.com', include_general, True],
                    ['Sara Carter', 'saraacarter.com', include_general, False], # Fox News investigative reporter
                    ['Sean Hannity', 'hannity.com', include_general, True],
                    ['Sean Hannity', 'hann.it', include_general, True],
                    ['The Blaze', 'theblaze.com', include_general, False], # conservative media, founded by Glenn Beck
                    ['The Gateway Pundit', 'thegatewaypundit.com', include_general, True],
                    ['The Epoch Times', 'theepochtimes.com', include_general, False],
                    ['The Federalist', 'thefederalist.com', include_general, False],
                    ['The Hill', 'thehill.com', include_general, False],
                    ['The Hill', 'hill.cm', include_general, False],
                    ['Time', 'time.com', include_general, False],
                    ['Townhall', 'townhall.com', include_general, False], # conservative news and political commentary and analysis
                    ['USA Today', 'eu.usatoday.com', include_general, False], # blocked due to GDPR?
                    ['USA Today', 'usatoday.com', include_general, False],
                    ['VDARE', 'vdare.com', include_general, True],
                    ['Washington Free Beacon', 'freebeacon.com', include_general, False], # American conservative political journalism website launched in 2012
                    ['Washington Examiner', 'washingtonexaminer.com', include_general, True],
                    ['Washington Examiner', 'washex.am', include_general, True],
                    ['Washington Post', 'washingtonpost.com', include_general, False],
                    ['Washington Post', 'wapo.st', include_general, False],
                    ['Washington Times', 'washingtontimes.com', include_general, False],
                    
                    # business/finance news
                    ['Business Insider', 'businessinsider.com', include_specialized, False],
                    ['MarketWatch', 'marketwatch.com', include_specialized, False],
                    ['The Business Journals', 'bizjournals.com', include_specialized, False], # metropolitan business newsweeklies
                    ['Wall Street Journal', 'on.wsj.com', include_specialized, False],
                    ['Wall Street Journal', 'wsj.com', include_specialized, False],
                    ['Yahoo Finance', 'finance.yahoo.com', include_specialized, False],
                    ['Forbes', 'forbes.com', include_specialized, False],
                    # Issue: pro-marriage, pro-life
                    ['Family Research Council', 'frc.org', include_specialized, False],
                    # agriculture
                    ['Agri-Pulse', 'agri-pulse.com', include_specialized, False], 
                    # military
                    ['Military', 'army.mil', include_specialized, False], # could be under 'public service'
                    ['Military', 'defensenews.com', include_specialized, False],
                    ['Military', 'military.com', include_specialized, False],
                    ['Military', 'militarytimes.com', include_specialized, False],
                    ['Military', 'navy.mil', include_specialized, False], # could be under 'public service'
                    ['Military', 'stripes.com', include_specialized, False], 
                    # government/congressional coverage
                    ['C-SPAN', 'c-span.org', include_specialized, False], # Cable-Satellite Public Affairs Network
                    ['C-SPAN', 'cs.pn', include_specialized, False],
                    ['GovTrack.us', 'govtrack.us', include_specialized, False],
                    
                    # public service
                    ['Public: 2020 Census', 'my2020census.gov', include_public_service, False],
                    ['Public: 2020 Census', '2020census.gov', include_public_service, False],
                    ['Public: CDC', 'cdc.gov', include_public_service, False], # Center for Disease Control
                    ['Public: Disaster Response', 'disasterassistance.gov', include_public_service, False],
                    ['Public: Disaster Response', 'hurricanes.gov', include_public_service, False],
                    ['Public: Disaster Response', 'nvoad.org', include_public_service, False],
                    ['Public: Disaster Response', 'redcross.org', include_public_service, False],
                    ['Public: Disaster Response', 'rdcrss.org', include_public_service, False],
                    ['Public: Small Business Administration', 'sba.gov', include_public_service, False],
                    ['Public: Take Back Day', 'takebackday.dea.gov', include_public_service, False],
                    ['Public: Take Back Day', 'deatakeback.com', include_public_service, False],
                    ['Public: Coronavirus', 'coronavirus.gov', include_public_service, False],
                
                    # regional
                    ['Regional', 'theadvocate.com', include_regional, False], # Louisiana
                    ['Regional', 'abc13.com', include_regional, False], # Houston
                    ['Regional', 'ajc.com', include_regional, False], # Atlanta
                    ['Regional', 'al.com', include_regional, False], # Alabama
                    ['Regional', 'aldailynews.com', include_regional, False], # Alabama
                    ['Regional', 'alreporter.com', include_regional, False], # Alabama
                    ['Regional', 'altoday.com', include_regional, False], # Alabama
                    ['Regional', 'argusleader.com', include_regional, False], # Sioux Falls, South Dakota
                    ['Regional', 'arkansasonline.com', include_regional, False],
                    ['Regional', 'auburnpub.com', include_regional, False], # Auburn, New York
                    ['Regional', 'azcentral.com', include_regional, False], # Arizona
                    ['Regional', 'eu.azcentral.com', include_regional, False], # Arizona
                    ['Regional', 'bladenonline.com', include_regional, False], # Bladen County, North Carolina
                    ['Regional', 'cincinnati.com', include_regional, False],
                    ['Regional', 'chron.com', include_regional, False], # Houston Chronicle
                    ['Regional', 'clarionledger.com', include_regional, False], # Mississippi
                    ['Regional', 'cleveland.com', include_regional, False],
                    ['Regional', 'dallasnews.com', include_regional, False],
                    ['Regional', 'denverpost.com', include_regional, False],
                    ['Regional', 'deseretnews.com', include_regional, False], # Utah
                    ['Regional', 'deseret.com', include_regional, False],
                    ['Regional', 'detroitnews.com', include_regional, False],
                    ['Regional', 'expressnews.com', include_regional, False],
                    ['Regional', 'floridadaily.com', include_regional, False],
                    ['Regional', 'fox11online.com', include_regional, False], # Green Bay, Wisconsin
                    ['Regional', 'gazette.com', include_regional, False], # Colorado
                    ['Regional', 'graydc.com', include_regional, False], # 'hyperlocal' news in DC
                    ['Regional', 'greenbaypressgazette.com', include_regional, False],
                    ['Regional', 'houstonchronicle.com', include_regional, False],
                    ['Regional', 'indystar.com', include_regional, False],
                    ['Regional', 'joplinglobe.com', include_regional, False], # Missouri
                    ['Regional', 'jsonline.com', include_regional, False], # Milwaukee, Wisconsin
                    ['Regional', 'journalgazette.net', include_regional, False], # Fort Wayne, northeast Indiana
                    ['Regional', 'kansas.com', include_regional, False],
                    ['Regional', 'kansascity.com', include_regional, False],
                    ['Regional', 'keloland.com', include_regional, False], # Sioux Falls, South Dakota
                    ['Regional', 'kentucky.com', include_regional, False],
                    ['Regional', 'kfyo.com', include_regional, False], # West Texas
                    ['Regional', 'ksl.com', include_regional, False],
                    ['Regional', 'ktar.com', include_regional, False], # Arizona
                    ['Regional', 'ktvb.com', include_regional, False], # Boise, Idaho
                    ['Regional', 'lancasteronline.com', include_regional, False], # Lancaster, PA
                    ['Regional', 'courier-journal.com', include_regional, False], # Louisville, Kentucky
                    ['Regional', 'miamiherald.com', include_regional, False], # Florida
                    ['Regional', 'mlive.com', include_regional, False], # Michigan
                    ['Regional', 'montgomeryadvertiser.com', include_regional, False], # Montgomery, Alabama
                    ['Regional', 'nebraska.tv', include_regional, False], 
                    ['Regional', 'newspressnow.com', include_regional, False], # St. Joseph, Missouri
                    ['Regional', 'news-leader.com', include_regional, False],
                    ['Regional', 'nny360.com', include_regional, False], # Northern New York
                    ['Regional', 'nola.com', include_regional, False], # New Orleans
                    ['Regional', 'nj.com', include_regional, False],
                    ['Regional', 'omaha.com', include_regional, False],
                    ['Regional', 'patch.com', include_regional, False], # hyper-local news platform
                    ['Regional', 'postandcourier.com', include_regional, False], # Charleston, South Carolina
                    ['Regional', 'postregister.com', include_regional, False], # Eastern Idaho
                    ['Regional', 'poststar.com', include_regional, False], # New York
                    ['Regional', 'reviewjournal.com', include_regional, False], # Las Vegas, Nevada
                    ['Regional', 'richmond.com', include_regional, False], # Richmond, Virginia
                    ['Regional', 'sltrib.com', include_regional, False], # Salt Lake City, Utah
                    ['Regional', 'star-telegram.com', include_regional, False], # Fort Worth Texas
                    ['Regional', 'statesman.com', include_regional, False], # Austin, Texas
                    ['Regional', 'spokesman.com', include_regional, False], # Spokane, Washington
                    ['Regional', 'stltoday.com', include_regional, False], # St. Louis, Missouri
                    ['Regional', 'syracuse.com', include_regional, False], # Syracuse, New York
                    ['Regional', 'tapinto.net',  include_regional, False], # TAPInto
                    ['Regional', 'tcpalm.com', include_regional, False], # southeastern Florida, Treasure Coast Newspapers
                    ['Regional', 'tennessean.com', include_regional, False], # Tennessee
                    ['Regional', 'thenewsstar.com', include_regional, False], # Monroe, Louisiana
                    ['Regional', 'tri-cityherald.com', include_regional, False], # Tri-City, Washington
                    ['Regional', 'tucson.com', include_regional, False], # Tucson, Arizona
                    ['Regional', 'wafb.com', include_regional, False], # Baton Rouge, Louisiana
                    ['Regional', 'wbrz.com', include_regional, False], # Baton Rouge, Louisiana
                    ['Regional', 'wdam.com', include_regional, False], # Mississippi
                    ['Regional', 'woodtv.com', include_regional, False], # Michigan
                    ['Regional', 'wowo.com', include_regional, False], # Indiana
                    ['Regional', 'wvmetronews.com', include_regional, False], # West Virginia
                    ['Regional', 'wwnytv.com', include_regional, False], # Watertown, New York
                    ['Regional', 'yallpolitics.com', include_regional, False], # political news and commentary media outlet in the state of Mississippi.
                    ['Regional', 'yellowhammernews.com', include_regional, False], # Alabama
                
                    # aggregators, URL shorteners, social media engagement tools
                    ['Unknown', 'amp.twimg.com', include_unknown, False], # Twitter hosted image
                    ['Unknown', 'podcasts.apple.com', include_unknown, False],
                    ['Unknown', 'apple.news', include_unknown, False],
                    ['Unknown', 'apple.co', include_unknown, False],
                    ['Unknown', 'apne.ws', include_unknown, False],
                    ['Unknown', 'bit.ly', include_unknown, False],
                    ['Unknown', 'buff.ly', include_unknown, False],
                    ['Unknown', 'dlvr.it', include_unknown, False],
                    ['Unknown', 'fb.me', include_unknown, False],
                    ['Unknown', 'goo.gl', include_unknown, False],
                    ['Unknown', 'google.com', include_unknown, False],
                    ['Unknown', 'iheart.com', include_unknown, False],
                    ['Unknown', 'iqconnect.lmhostediq.com', include_unknown, False], # newsletter service
                    ['Unknown', 'j.mp', include_unknown, False],
                    ['Unknown', 'medium.com', include_unknown, False], # not a news media source
                    ['Unknown', 'omny.fm', include_unknown, False], # podcasting
                    ['Unknown', 'ow.ly', include_unknown, False],
                    ['Unknown', 'snpy.tv', include_unknown, False], # SnappyTV, Twitter's real-time video-clipping service
                    ['Unknown', 'spectrumnews1.com', include_unknown, False], # generic
                    ['Unknown', 'tinyurl.com', include_unknown, False],
                    ['Unknown', 'trib.al', include_unknown, False],
                    ['Unknown', 'usat.ly', include_unknown, False], # custom domain from bitly
                    ['Unknown', 'vimeo.com', include_unknown, False],
                    
                    # GOP
                    ['.gop', 'didyouknow.gop', include_gop, False],
                    ['.gop', 'fairandsimple.gop', include_gop, False],
                    
                    # miscellaneous
                    ['Misc', 'espn.com', include_misc, False],
                    ['Misc', 'safetravelusa.com', include_misc, False], # road conditions
                    ['Misc', 'access.live', include_misc, False], # conferencing tool
                    ['Misc', 'vekeo.com', include_misc, False], # conferencing tool
                    ['Misc', 'eventbrite.com', include_misc, False],
                    ['Misc', 'moaa.org', include_misc, False]
                    ]
        
    df_media_netloc = pd.DataFrame(netloc_groups, columns =['netloc_group', 'url_netloc', 'include_netloc', 'is_selected_outlet'])

    return df_media_netloc

def get_media_outlet_ideo():
    # Pew numbers are from Jurkowitz et al.: U.S. Media Polarization and the 2020 Election: A Nation Divided
    outlet_ideo = [['Vox','vox',62, 4, 58,'left','left',0],
                    ['HuffPost','huffingtonpost', 53,11,42,'left','left',1],
                    ['The Guardian','guardian', 54,12,42,'left','left',2],
                    ['Vice','vice',48,7,41,'left','left',3],
                    ['New York Times','newyorktimes', 48,11,37,'left','left',4],
                    ['NPR', 'npr',49,12,37,'left','left',5],
                    ['Politico','politico', 49,13,36,'left','left',6],
                    ['Washington Post','washingtonpost', 45,12,33,'left','left',7],
                    ['BBC','bbc',42,14,28,'left','left',8],
                    ['Time','time',37,13,25,'left','left',9],
                    ['MSNBC','msnbc',37,13,24,'left','left',10],
                    ['BuzzFeed','buzzfeed', 40,17,23,'left','left',11],
                    ['PBS','pbs',39,16,22,'left','left',12],
                    ['The Hill','thehill', 42,22,21,'left','left',13],
                    ['CNN', 'cnn',34,13,20,'left','left',14],
                    ['Newsweek','newsweek',34,14,20,'left','left',15],
                    ['Business Insider','businessinsider', 40,20,20,'left','left',16],
                    ['Wall Street Journal','wallstreetjournal', 31,24,7,'mixed','mixed',17],
                    ['NBC News','nbcnews',27,20,7,'mixed','mixed',18],
                    ['Univision','univision',19,12,7,'mixed','mixed',19],
                    ['USA Today','usatoday',25,19,6,'mixed','mixed',20],
                    ['ABC News','abcnews',22,21,1,'mixed','mixed',21],
                    ['CBS News','cbsnews',23,22,1,'mixed','mixed',22],
                    ['New York Post','newyorkpost',22,32,-10,'mixed','mixed',23],
                    ['Washington Examiner','washingtonexaminer',14,44,-29,'right','established right',24],
                    ['Fox','foxnews',9,46,-38,'right','established right',25],
                    ['Daily Caller','dailycaller',3,72,-69,'right','established right',26],
                    ['Breitbart','breitbart',1,80,-79,'right','alternative right',27],
                    ['Sean Hannity','seanhannity',2,82,-80,'right','established right',28],
                    ['Rush Limbaugh','rushlimbaugh',1,81,-80,'right','established right',29],
                    ['Newsmax','newsmax',None, None, -999, 'right','alternative right', 30],
                    ['One America News', 'oneamericanews',None, None, -999,'right','alternative right', 31],
                    ['The Gateway Pundit','gatewaypundit',None, None, -999, 'right','alternative right',32],
                    ['InfoWars','infowars',None, None, -999, 'right','alternative right',33],
                    ['American Renaissance', 'americanrenaissance',None, None, -999, 'right','alternative right', 34],
                    ['VDARE','vdare',None, None, -999, 'right','alternative right', 35],
                    ['Daily Stormer','dailystormer',None, None, -999, 'right','alternative right', 36]]

    df_outlet_ideo = pd.DataFrame(outlet_ideo, columns = ['outlet','outlet_std','pew_libdem', 'pew_consrep', 'pew_libdem_consrep_diff', 'ideo_category', 'ideo_subcategory', 'ideo_left2right'])

    return df_outlet_ideo