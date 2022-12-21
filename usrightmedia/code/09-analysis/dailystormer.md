# Notes on Daily Stormer

- As of June 13, 2022, Daily Stormer accessible at https://stormer-daily.rw/

## Indirect shares (2)

1. (Re)tweets

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
              "SenHawleyPress_1255975777528619009_0",
              "DrPhilRoe_829852767086850048_0"
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
    "total" : 2,
    "max_score" : 0.0,
    "hits" : [
      {
        "_index" : "inca2",
        "_type" : "doc",
        "_id" : "SenHawleyPress_1255975777528619009_0",
        "_score" : 0.0,
        "_source" : {
          "doctype" : "tweets2_url",
          "tweet_id" : "1255975777528619009",
          "text" : [redacted],
          "author_id" : "1080960924687704064",
          "tweet_url" : "https://twitter.com/SenHawleyPress/status/1255975777528619009",
          "standardized_url" : "www.foxnews.com/politics/hawley-meatpacking-titans-coronavirus-monopoly-farmers"
        }
      },
      {
        "_index" : "inca2",
        "_type" : "doc",
        "_id" : "DrPhilRoe_829852767086850048_0",
        "_score" : 0.0,
        "_source" : {
          "doctype" : "tweets2_url",
          "tweet_id" : "829852767086850048",
          "text" : [redacted],
          "author_id" : "52503751",
          "tweet_url" : "https://twitter.com/DrPhilRoe/status/829852767086850048",
          "standardized_url" : "www.foxnews.com/politics/defiant-trump-tweets-see-you-in-court-after-ruling-again-blocks-immigration-order"
        }
      }
    ]
  }
}

```

2: Articles of 'follower' outlet

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
        {"terms": {"_id": ["FoxNews_1592642771", "FoxNews_694938422"]}}
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
        "_id" : "FoxNews_694938422",
        "_score" : 0.0,
        "_source" : {
          "tweets2_url_ids" : [
            "DrPhilRoe_829852767086850048_0"
          ],
          "tweets2_url_match_count" : 1,
          "tweets2_url_match_ind" : true,
          "ap_syndicated" : false,
          "title" : "Defiant Trump tweets 'SEE YOU IN COURT' after ruling again blocks immigration order",
          "standardized_url" : "www.foxnews.com/politics/defiant-trump-tweets-see-you-in-court-after-ruling-again-blocks-immigration-order",
          "publish_date" : "2017-02-09T12:00:00+00:00"
        }
      },
      {
        "_index" : "inca2",
        "_type" : "doc",
        "_id" : "FoxNews_1592642771",
        "_score" : 0.0,
        "_source" : {
          "tweets2_url_ids" : [
            "SenHawleyPress_1255975777528619009_0"
          ],
          "tweets2_url_match_count" : 1,
          "tweets2_url_match_ind" : true,
          "ap_syndicated" : false,
          "title" : "Hawley eyes meatpacking titans amid coronavirus crisis: 'Monopoly is bad for farmers'",
          "standardized_url" : "www.foxnews.com/politics/hawley-meatpacking-titans-coronavirus-monopoly-farmers",
          "publish_date" : "2020-04-29T20:09:12+00:00"
        }
      }
    ]
  }
}


```



3. Articles of 'lead' outlet

- `DailyStormer_1590014524`: [commentary; lengthy quote from Bloomberg](https://web.archive.org/web/20200425000446/https://www.bloomberg.com/news/articles/2020-04-24/meat-threats-grow-with-first-brazil-shutdown-u-s-turkey-halt)
- `DailyStormer_576843628`: [commentary; lengthy quote from Fox News](https://web.archive.org/web/20190628093820/https://www.foxnews.com/politics/pence-will-use-all-legal-means-at-our-disposal-to-reinstate-immigration-ban)
  -  Fox News article link leads to 404: scraping would fail even if URL was included in Media Cloud dataset -> wouldn't be used for news event clustering -> wouldn't be used in dyadic comparisons)
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
        {"terms": {"_id": ["DailyStormer_1590014524", "DailyStormer_576843628"]}}
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
        "_id" : "DailyStormer_576843628",
        "_score" : 0.0,
        "_source" : {
          "tweets2_url_ids" : [ ],
          "tweets2_url_match_count" : 0,
          "tweets2_url_match_ind" : false,
          "ap_syndicated" : false,
          "title" : "Pence Vows to Do Everything in His Power to Get Moslem Ban Restored",
          "standardized_url" : "www.dailystormer.com:80/pence-vows-to-do-everything-in-his-power-to-get-moslem-ban-restored",
          "publish_date" : "2017-02-05T18:09:29+00:00"
        }
      },
      {
        "_index" : "inca2",
        "_type" : "doc",
        "_id" : "DailyStormer_1590014524",
        "_score" : 0.0,
        "_source" : {
          "tweets2_url_ids" : [ ],
          "tweets2_url_match_count" : 0,
          "tweets2_url_match_ind" : false,
          "ap_syndicated" : false,
          "title" : "Loli Vegan Dictatorship Confirmed – US Meat Plants Shutting Down, Pork Production Down One Third, Beef Prices Soar",
          "standardized_url" : "dailystormer.su/loli-vegan-dictatorship-confirmed-us-meat-plants-shutting-down-pork-production-down-one-third-beef-prices-soar",
          "publish_date" : "2020-04-27T04:00:02+00:00"
        }
      }
    ]
  }
}


```