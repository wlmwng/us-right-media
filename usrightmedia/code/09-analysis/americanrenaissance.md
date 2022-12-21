# Notes on American Renaissance


## Direct shares (1)

1. (Re-)tweets
```
GET inca_alias/_search?filter_path=hits
{"_source": [
    "doctype",
    "tweet_id",
    "text",
    "author_id",
    "tweet_url",
    "standardized_url"
  ],
  "query": {
    "bool": {
      "filter": [
        {"term": {"url_id": "1007700713038929920_0"}}
      ]
    }
  }
}

---

{
  "hits" : {
    "total" : 1,
    "max_score" : 0.0,
    "hits" : [
      {
        "_index" : "inca2",
        "_type" : "doc",
        "_id" : "CongHuelskamp_1007700713038929920_0",
        "_score" : 0.0,
        "_source" : {
          "doctype" : "tweets2_url",
          "tweet_id" : "1007700713038929920",
          "text" : [redacted],
          "author_id" : "233761277",
          "tweet_url" : "https://twitter.com/CongHuelskamp/status/1007700713038929920",
          "standardized_url" : "www.amren.com/news/2018/06/jared-taylor-wins-first-round-in-anti-censorship-suit-against-twitter",
        }
      }
    ]
  }
}
```

## Indirect shares (3)

1. (Re-)tweets

```
GET inca_alias/_search?filter_path=hits
{"_source": [
    "doctype",
    "tweet_id",
    "text",
    "author_id",
    "tweet_url",
    "standardized_url"
  ],
  "query": {
    "bool": {
      "filter": [
        {
          "terms": {
            "_id": [
              "RepLoudermilk_1217840618078113799_0",
              "RepBrianBabin_1217933512738852865_0",
              "RepMarkWalker_824362661508943873_0"
            ]
          }
        }
      ]
    }
  }
}

---

{
  "hits" : {
    "total" : 3,
    "max_score" : 0.0,
    "hits" : [
      {
        "_index" : "inca2",
        "_type" : "doc",
        "_id" : "RepBrianBabin_1217933512738852865_0",
        "_score" : 0.0,
        "_source" : {
          "doctype" : "tweets2_url",
          "tweet_id" : "1217933512738852865",
          "text" : [redacted],
          "author_id" : "2929491549",
          "tweet_url" : "https://twitter.com/RepBrianBabin/status/1217933512738852865",
          "standardized_url" : "www.foxnews.com/politics/nyc-sanctuary-city-policy-under-fire"
        }
      },
      {
        "_index" : "inca2",
        "_type" : "doc",
        "_id" : "RepLoudermilk_1217840618078113799_0",
        "_score" : 0.0,
        "_source" : {
          "doctype" : "tweets2_url",
          "tweet_id" : "1217840618078113799",
          "text" : [redacted],
          "author_id" : "2914163523",
          "tweet_url" : "https://twitter.com/RepLoudermilk/status/1217840618078113799",
          "standardized_url" : "www.foxnews.com/politics/nyc-sanctuary-city-policy-under-fire"
        }
      },
      {
        "_index" : "inca2",
        "_type" : "doc",
        "_id" : "RepMarkWalker_824362661508943873_0",
        "_score" : 0.0,
        "_source" : {
          "doctype" : "tweets2_url",
          "tweet_id" : "824362661508943873",
          "text" : [redacted],
          "author_id" : "2966205003",
          "tweet_url" : "https://twitter.com/RepMarkWalker/status/824362661508943873",
          "standardized_url" : "www.foxnews.com/politics/education-department-report-finds-billions-spent-under-obama-had-no-impact-on-achievement"
        }
      }
    ]
  }
}
```

2. Articles of 'follower' outlet

```
GET inca_alias/_search?filter_path=hits
{"_source": [
    "_id",
    "title",
    "standardized_url",
    "publish_date",
    "ap_syndicated",
    "tweets2_url_ids",
    "tweets2_url_match_count",
    "tweets2_url_match_ind"
  ],
  "query": {
    "bool": {
      "filter": [
        {"term": {"should_include": true}},
        {"terms": {"_id": ["FoxNews_1517170333", "FoxNews_1517170333", "FoxNews_572052805"]}}
      ]
    }
  }
}

---

{
  "hits" : {
    "total" : 2,
    "max_score" : 0.0,
    "hits" : [
      {
        "_index" : "inca2",
        "_type" : "doc",
        "_id" : "FoxNews_572052805",
        "_score" : 0.0,
        "_source" : {
          "tweets2_url_ids" : [
            "RepMarkWalker_824362661508943873_0"
          ],
          "tweets2_url_match_count" : 1,
          "tweets2_url_match_ind" : true,
          "ap_syndicated" : false,
          "title" : "Education Department report finds billions spent under Obama had 'no impact' on achievement",
          "standardized_url" : "www.foxnews.com/politics/education-department-report-finds-billions-spent-under-obama-had-no-impact-on-achievement",
          "publish_date" : "2017-01-25T14:47:00+00:00"
        }
      },
      {
        "_index" : "inca2",
        "_type" : "doc",
        "_id" : "FoxNews_1517170333",
        "_score" : 0.0,
        "_source" : {
          "tweets2_url_ids" : [
            "RepBrianBabin_1217933512738852865_0",
            "RepLoudermilk_1217840618078113799_0"
          ],
          "tweets2_url_match_count" : 2,
          "tweets2_url_match_ind" : true,
          "ap_syndicated" : false,
          "title" : "NYC’s sanctuary city policy under fire after freed illegal immigrant allegedly murders 92-year-old | Fox News",
          "standardized_url" : "www.foxnews.com/politics/nyc-sanctuary-city-policy-under-fire",
          "publish_date" : "2020-01-16T05:00:00+00:00"
        }
      }
    ]
  }
}

```



3. Articles of 'lead' outlet

- `AmericanRenaissance_571311262`: [re-post of Washington Post article](https://www.washingtonpost.com/local/education/obama-administration-spent-billions-to-fix-failing-schools-and-it-didnt-work/2017/01/19/6d24ac1a-de6d-11e6-ad42-f3375f271c9c_story.html)
- `AmericanRenaissance_1495026172`: [re-post of ICE press release](https://www.ice.gov/news/releases/ice-lodges-detainer-against-guyanese-national-arrested-murder-92-year-old-new-york)

```
GET inca_alias/_search?filter_path=hits
{"_source": [
    "_id",
    "title",
    "standardized_url",
    "publish_date",
    "ap_syndicated",
    "tweets2_url_ids",
    "tweets2_url_match_count",
    "tweets2_url_match_ind"
  ],
  "query": {
    "bool": {
      "filter": [
        {"term": {"should_include": true}},
        {"terms": {"_id": ["AmericanRenaissance_1495026172", "AmericanRenaissance_1495026172", "AmericanRenaissance_571311262"]}}
      ]
    }
  }
}

---

{
  "hits" : {
    "total" : 2,
    "max_score" : 0.0,
    "hits" : [
      {
        "_index" : "inca2",
        "_type" : "doc",
        "_id" : "AmericanRenaissance_571311262",
        "_score" : 0.0,
        "_source" : {
          "tweets2_url_ids" : [ ],
          "tweets2_url_match_count" : 0,
          "tweets2_url_match_ind" : false,
          "ap_syndicated" : false,
          "title" : "Obama Administration Spent Billions to Fix Failing Schools, and It Didn’t Work",
          "standardized_url" : "www.amren.com/news/2017/01/obama-administration-spent-billions-fix-failing-schools-didnt-work",
          "publish_date" : "2017-01-23T22:47:33+00:00"
        }
      },
      {
        "_index" : "inca2",
        "_type" : "doc",
        "_id" : "AmericanRenaissance_1495026172",
        "_score" : 0.0,
        "_source" : {
          "tweets2_url_ids" : [ ],
          "tweets2_url_match_count" : 0,
          "tweets2_url_match_ind" : false,
          "ap_syndicated" : false,
          "title" : "ICE Lodges Detainer Against Guyanese National Arrested for the Murder of a 92-Year-Old New York City Woman",
          "standardized_url" : "www.amren.com/news/2020/01/ice-lodges-detainer-against-guyanese-national-arrested-for-the-murder-of-a-92-year-old-new-york-city-woman",
          "publish_date" : "2020-01-14T22:54:57+00:00"
        }
      }
    ]
  }
}
```