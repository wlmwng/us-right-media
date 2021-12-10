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


def get_media_outlet_netloc(include_national = False,
                             include_regional = False,
                             include_gop = False,
                             include_government = False):

    netloc_groups = [['ABC News', 'abcnews.go.com', include_national, False, 'abcnews'],
                    ['ABC News', 'abcn.ws', include_national, False, 'abcnews'],
                    ['American Renaissance', 'amren.com', include_national, True, 'americanrenaissance'],
                    ['AP News', 'apnews.com', include_national, False, 'apnews'],
                    ['Axios', 'axios.com', include_national, False, 'axios'],
                    ['BBC', 'bbc.com', include_national, False, 'bbc'],
                    ['Bloomberg', 'bloomberg.com', include_national, False, 'bloomberg'],
                    ['Business Insider', 'businessinsider.com', include_national, False, 'businessinsider'],
                    ['Breitbart', 'breitbart.com', include_national, True, 'breitbart'],
                    ['Buzzfeed News', 'buzzfeednews.com', include_national, False, 'buzzfeed'],
                    ['CBS News', 'cbsnews.com', include_national, False, 'cbsnews'],
                    ['CBS News', 'cbsn.ws', include_national, False, 'cbsnews'],
                    ['CBS News', 'cbsloc.al', include_national, False, 'cbsnews'],
                    ['CNBC', 'cnbc.com', include_national, False, 'cnbc'],
                    ['CNBC', 'cnb.cx', include_national, False, 'cnbc'],
                    ['CNN', 'cnn.com', include_national, False, 'cnn'],
                    ['CNN', 'edition.cnn.com', include_national, False, 'cnn'],
                    ['CNN', 'cnn.it', include_national, False, 'cnn'],
                    ['CNS News', 'cnsnews.com', include_national, False, 'cnsnews'], # conservative news site
                    ['Daily Caller', 'dailycaller.com', include_national, True, 'dailycaller'],
                    ['Daily Caller', 'amp.dailycaller.com', include_national, True, 'dailycaller'],
                    ['Daily Caller', 'checkyourfact.com', include_national, True, 'dailycaller'],
                    ['Daily Caller', 'smokeroom.com', include_national, True, 'dailycaller'],
                    ['Daily Signal', 'dailysignal.com', include_national, False, 'dailysignal'],
                    ['Daily Stormer', 'dailystormer.com', include_national, True, 'dailystormer'],
                    ['Daily Stormer', 'dailystormer.name', include_national, True, 'dailystormer'],
                    ['Daily Stormer', 'dailystormer.su', include_national, True, 'dailystormer'],
                    ['Forbes', 'forbes.com', include_national, False, 'forbes'],
                    ['Fox News', 'fxn.ws', include_national, True, 'foxnews'],
                    ['Fox News', 'foxbusiness.com', include_national, True, 'foxnews'],
                    ['Fox News', 'foxsports.com', include_national, True, 'foxnews'],
                    ['Fox News', 'foxnews.com', include_national, True,'foxnews'],
                    ['Fox News', '925foxnews.com', include_national, True, 'foxnews'],
                    ['Fox News', 'insider.foxnews.com', include_national, True, 'foxnews'],
                    ['Fox News', 'latino.foxnews.com', include_national, True,'foxnews'],
                    ['Fox News', 'nation.foxnews.com', include_national, True, 'foxnews'],
                    ['Fox News', 'press.foxnews.com', include_national, True, 'foxnews'],
                    ['Fox News', 'press.foxbusiness.com', include_national, True, 'foxnews'],
                    ['Fox News', 'radio.foxnews.com', include_national, True, 'foxnews'],
                    ['Fox News', 'video.foxbusiness.com', include_national, True, 'foxnews'],
                    ['Fox News', 'video.foxnews.com', include_national, True, 'foxnews'],
                    ['Huffington Post', 'huffpost.com', include_national, False, 'huffingtonpost'],
                    ['Infowars', 'archives.infowars.com', include_national, True, 'infowars'],
                    ['Infowars', 'europe.infowars.com', include_national, True, 'infowars'],
                    ['Infowars', 'infowars.com', include_national, True, 'infowars'],
                    ['Infowars', 'planet.infowars.com', include_national, True, 'infowars'],
                    ['Infowars', 'newswars.com', include_national, True, 'infowars'],
                    ['Just the News', 'justthenews.com', include_national, False], # https://capitolcommunicator.com/award-winning-journalist-john-solomon-launches-new-media-outlet/
                    ['Los Angeles Times', 'latimes.com', include_national, False, 'latimes'],
                    ['MarketWatch', 'marketwatch.com', include_national, False, 'marketwatch'],
                    ['MSNBC', 'msnbc.com', include_national, False, 'msnbc'],
                    ['National Review', 'nationalreview.com', include_national, False, 'nationalreview'],
                    ['NBC News', 'nbcnews.com', include_national, False, 'nbcnews'],
                    ['NBC News', 'nbcnews.to', include_national, False, 'nbcnews'],
                    ['Newsmax', 'newsmax.com', include_national, True, 'newsmax'],
                    ['Newsmax', 'newsmaxtv.com', include_national, True, 'newsmax'],
                    ['Newsweek', 'newsweek.com', include_national, False, 'newsweek'],
                    ['New York Post', 'nypost.com', include_national, False, 'newyorkpost'],
                    ['New York Times', 'nytimes.com', include_national, False, 'newyorktimes'],
                    ['New York Times', 'nyti.ms', include_national, False, 'newyorktimes'],
                    ['NPR', 'npr.org', include_national, False, 'npr'], # national public radio
                    ['NPR', 'n.pr', include_national, False, 'npr'],
                    ['One America News', 'oann.com', include_national, True, 'oneamericanews'],
                    ['PBS', 'pbs.org', include_national, False, 'pbs'],
                    ['Politico', 'politico.com', include_national, False, 'politico'],
                    ['Politico', 'politi.co', include_national, False, 'politico'],
                    ['Real Clear Politics', 'realclearpolitics.com', include_national, False, 'realclearpolitics'],
                    ['Reuters', 'reuters.com', include_national, False, 'reuters'],
                    ['Reuters', 'reut.rs', include_national, False, 'reuters'],
                    ['Ripon Advance', 'riponadvance.com', include_national, False, 'riponadvance'], # https://riponadvance.com/about-us/
                    ['Roll Call', 'rollcall.com', include_national, False, 'rollcall'], # congressional news, legislative tracking and advocacy services
                    ['Rush Limbaugh', 'rushlimbaugh.com', include_national, True, 'rushlimbaugh'],
                    ['Sara Carter', 'saraacarter.com', include_national, False, 'saracarter'], # Fox News investigative reporter
                    ['Sean Hannity', 'hannity.com', include_national, True, 'seanhannity'],
                    ['Sean Hannity', 'm.hannity.com', include_national, True, 'seanhannity'],
                    ['Sean Hannity', 'hann.it', include_national, True, 'seanhannity'],
                    ['The Blaze', 'theblaze.com', include_national, False, 'theblaze'], # conservative media, founded by Glenn Beck
                    ['The Business Journals', 'bizjournals.com', include_national, False, 'thebusinessjournals'], # metropolitan business newsweeklies
                    ['The Gateway Pundit', 'thegatewaypundit.com', include_national, True, 'gatewaypundit'],
                    ['The Guardian', 'theguardian.com', include_national, False, 'guardian'],
                    ['The Epoch Times', 'theepochtimes.com', include_national, False, 'epochtimes'],
                    ['The Federalist', 'thefederalist.com', include_national, False, 'federalist'],
                    ['The Hill', 'thehill.com', include_national, False, 'thehill'],
                    ['The Hill', 'hill.cm', include_national, False, 'thehill'],
                    ['Time', 'time.com', include_national, False, 'time'],
                    ['Townhall', 'townhall.com', include_national, False, 'townhall'], # conservative news and political commentary and analysis
                    ['Univision', 'univision.com', include_national, False, 'univision'],
                    ['USA Today', 'eu.usatoday.com', include_national, False, 'usatoday'],
                    ['USA Today', 'usatoday.com', include_national, False, 'usatoday'],
                    ['VDARE', 'vdare.com', include_national, True, 'vdare'],
                    ['Vox', 'vox.com', include_national, False, 'vox'],
                    ['VICE', 'vice.com', include_national, False, 'vice'],
                    ['Wall Street Journal', 'on.wsj.com', include_national, False, 'wallstreetjournal'],
                    ['Wall Street Journal', 'wsj.com', include_national, False, 'wallstreetjournal'],
                    ['Washington Free Beacon', 'freebeacon.com', include_national, False, 'washingtonfreebeacon'], # American conservative political journalism website launched in 2012
                    ['Washington Examiner', 'washingtonexaminer.com', include_national, True, 'washingtonexaminer'],
                    ['Washington Examiner', 'm.washingtonexaminer.com', include_national, True, 'washingtonexaminer'],
                    ['Washington Examiner', 'washex.am', include_national, True, 'washingtonexaminer'],
                    ['Washington Post', 'washingtonpost.com', include_national, False, 'washingtonpost'],
                    ['Washington Post', 'wapo.st', include_national, False, 'washingtonpost'],
                    ['Washington Times', 'washingtontimes.com', include_national, False, 'washingtontimes'],
                    ['Yahoo Finance', 'finance.yahoo.com', include_national, False, 'yahoofinance'],
                
                    # regional
                    ['Regional', 'theadvocate.com', include_regional, False, ''], # Louisiana
                    ['Regional', 'abc13.com', include_regional, False, ''], # Houston
                    ['Regional', 'ajc.com', include_regional, False, ''], # Atlanta
                    ['Regional', 'al.com', include_regional, False, ''], # Alabama
                    ['Regional', 'aldailynews.com', include_regional, False, ''], # Alabama
                    ['Regional', 'alreporter.com', include_regional, False, ''], # Alabama
                    ['Regional', 'altoday.com', include_regional, False, ''], # Alabama
                    ['Regional', 'argusleader.com', include_regional, False, ''], # Sioux Falls, South Dakota
                    ['Regional', 'arkansasonline.com', include_regional, False, ''],
                    ['Regional', 'auburnpub.com', include_regional, False, ''], # Auburn, New York
                    ['Regional', 'azcentral.com', include_regional, False, ''], # Arizona
                    ['Regional', 'eu.azcentral.com', include_regional, False, ''], # Arizona
                    ['Regional', 'bladenonline.com', include_regional, False, ''], # Bladen County, North Carolina
                    ['Regional', 'cincinnati.com', include_regional, False, ''],
                    ['Regional', 'chron.com', include_regional, False, ''], # Houston Chronicle
                    ['Regional', 'clarionledger.com', include_regional, False, ''], # Mississippi
                    ['Regional', 'cleveland.com', include_regional, False, ''],
                    ['Regional', 'dallasnews.com', include_regional, False, ''],
                    ['Regional', 'denverpost.com', include_regional, False, ''],
                    ['Regional', 'deseretnews.com', include_regional, False, ''], # Utah
                    ['Regional', 'deseret.com', include_regional, False, ''],
                    ['Regional', 'detroitnews.com', include_regional, False, ''],
                    ['Regional', 'expressnews.com', include_regional, False, ''],
                    ['Regional', 'floridadaily.com', include_regional, False, ''],
                    ['Regional', 'fox11online.com', include_regional, False, ''], # Green Bay, Wisconsin
                    ['Regional', 'gazette.com', include_regional, False, ''], # Colorado
                    ['Regional', 'graydc.com', include_regional, False, ''], # 'hyperlocal' news in DC
                    ['Regional', 'greenbaypressgazette.com', include_regional, False, ''],
                    ['Regional', 'houstonchronicle.com', include_regional, False, ''],
                    ['Regional', 'indystar.com', include_regional, False, ''],
                    ['Regional', 'joplinglobe.com', include_regional, False, ''], # Missouri
                    ['Regional', 'jsonline.com', include_regional, False, ''], # Milwaukee, Wisconsin
                    ['Regional', 'journalgazette.net', include_regional, False, ''], # Fort Wayne, northeast Indiana
                    ['Regional', 'kansas.com', include_regional, False, ''],
                    ['Regional', 'kansascity.com', include_regional, False, ''],
                    ['Regional', 'keloland.com', include_regional, False, ''], # Sioux Falls, South Dakota
                    ['Regional', 'kentucky.com', include_regional, False, ''],
                    ['Regional', 'kfyo.com', include_regional, False, ''], # West Texas
                    ['Regional', 'ksl.com', include_regional, False, ''],
                    ['Regional', 'ktar.com', include_regional, False, ''], # Arizona
                    ['Regional', 'ktvb.com', include_regional, False, ''], # Boise, Idaho
                    ['Regional', 'lancasteronline.com', include_regional, False, ''], # Lancaster, PA
                    ['Regional', 'courier-journal.com', include_regional, False, ''], # Louisville, Kentucky
                    ['Regional', 'miamiherald.com', include_regional, False, ''], # Florida
                    ['Regional', 'mlive.com', include_regional, False, ''], # Michigan
                    ['Regional', 'montgomeryadvertiser.com', include_regional, False, ''], # Montgomery, Alabama
                    ['Regional', 'nebraska.tv', include_regional, False, ''], 
                    ['Regional', 'newspressnow.com', include_regional, False, ''], # St. Joseph, Missouri
                    ['Regional', 'news-leader.com', include_regional, False, ''],
                    ['Regional', 'nny360.com', include_regional, False, ''], # Northern New York
                    ['Regional', 'nola.com', include_regional, False, ''], # New Orleans
                    ['Regional', 'nj.com', include_regional, False, ''],
                    ['Regional', 'omaha.com', include_regional, False, ''],
                    ['Regional', 'patch.com', include_regional, False, ''], # hyper-local news platform
                    ['Regional', 'postandcourier.com', include_regional, False, ''], # Charleston, South Carolina
                    ['Regional', 'postregister.com', include_regional, False, ''], # Eastern Idaho
                    ['Regional', 'poststar.com', include_regional, False, ''], # New York
                    ['Regional', 'reviewjournal.com', include_regional, False, ''], # Las Vegas, Nevada
                    ['Regional', 'richmond.com', include_regional, False, ''], # Richmond, Virginia
                    ['Regional', 'sltrib.com', include_regional, False, ''], # Salt Lake City, Utah
                    ['Regional', 'star-telegram.com', include_regional, False, ''], # Fort Worth Texas
                    ['Regional', 'statesman.com', include_regional, False, ''], # Austin, Texas
                    ['Regional', 'spokesman.com', include_regional, False, ''], # Spokane, Washington
                    ['Regional', 'stltoday.com', include_regional, False, ''], # St. Louis, Missouri
                    ['Regional', 'syracuse.com', include_regional, False, ''], # Syracuse, New York
                    ['Regional', 'tapinto.net',  include_regional, False, ''], # TAPInto
                    ['Regional', 'tcpalm.com', include_regional, False, ''], # southeastern Florida, Treasure Coast Newspapers
                    ['Regional', 'tennessean.com', include_regional, False, ''], # Tennessee
                    ['Regional', 'thenewsstar.com', include_regional, False, ''], # Monroe, Louisiana
                    ['Regional', 'tri-cityherald.com', include_regional, False, ''], # Tri-City, Washington
                    ['Regional', 'tucson.com', include_regional, False, ''], # Tucson, Arizona
                    ['Regional', 'wafb.com', include_regional, False, ''], # Baton Rouge, Louisiana
                    ['Regional', 'wbrz.com', include_regional, False, ''], # Baton Rouge, Louisiana
                    ['Regional', 'wdam.com', include_regional, False, ''], # Mississippi
                    ['Regional', 'woodtv.com', include_regional, False, ''], # Michigan
                    ['Regional', 'wowo.com', include_regional, False, ''], # Indiana
                    ['Regional', 'wvmetronews.com', include_regional, False, ''], # West Virginia
                    ['Regional', 'wwnytv.com', include_regional, False, ''], # Watertown, New York
                    ['Regional', 'yallpolitics.com', include_regional, False, ''], # political news and commentary media outlet in the state of Mississippi.
                    ['Regional', 'yellowhammernews.com', include_regional, False, ''], # Alabama
                                
                    # GOP
                    ['.gop', 'didyouknow.gop', include_gop, False, ''],
                    ['.gop', 'fairandsimple.gop', include_gop, False, ''],


                    # government
                    ['Military', 'army.mil', include_government, False, ''],
                    ['Military', 'defensenews.com', include_government, False, ''],
                    ['Military', 'military.com', include_government, False, ''],
                    ['Military', 'militarytimes.com', include_government, False, ''],
                    ['Military', 'navy.mil', include_government, False, ''],
                    ['Military', 'stripes.com', include_government, False, ''],
                    ['C-SPAN', 'c-span.org', include_government, False, ''], # Cable-Satellite Public Affairs Network
                    ['C-SPAN', 'cs.pn', include_government, False, ''],
                    ['GovTrack.us', 'govtrack.us', include_government, False, ''],
                    ['2020 Census', 'my2020census.gov', include_government, False, ''],
                    ['2020 Census', '2020census.gov', include_government, False, ''],
                    ['CDC', 'cdc.gov', include_government, False, ''], # Center for Disease Control
                    ['Disaster Response', 'disasterassistance.gov', include_government, False, ''],
                    ['Disaster Response', 'hurricanes.gov', include_government, False, ''],
                    ['Disaster Response', 'nvoad.org', include_government, False, ''],
                    ['Disaster Response', 'redcross.org', include_government, False, ''],
                    ['Disaster Response', 'rdcrss.org', include_government, False, ''],
                    ['Small Business Administration', 'sba.gov', include_government, False, ''],
                    ['Take Back Day', 'takebackday.dea.gov', include_government, False, ''],
                    ['Take Back Day', 'deatakeback.com', include_government, False, ''],
                    ['Coronavirus', 'coronavirus.gov', include_government, False, '']
                    ]
        
    df_media_netloc = pd.DataFrame(netloc_groups, columns =['netloc_group', 'url_netloc', 'include_netloc', 'is_selected_outlet', 'outlet_std'])

    return df_media_netloc

def get_media_outlet_ideo():
    # Pew numbers are from Jurkowitz et al.: U.S. Media Polarization and the 2020 Election: A Nation Divided
    # https://www.pewresearch.org/journalism/wp-content/uploads/sites/8/2020/01/PJ_2020.01.24_Media-Polarization_FINAL.pdf
    outlet_ideo = [['Vox','vox',62, 4, 58,'left','left',0],
                    ['Huffington Post','huffingtonpost', 53,11,42,'left','left',1],
                    ['The Guardian','guardian', 54,12,42,'left','left',2],
                    ['VICE','vice',48,7,41,'left','left',3],
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
                    ['Fox News','foxnews',9,46,-38,'right','established right',25],
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