# Notes on Sean Hannity

Of 4,203 Sean Hannity URLs which included for analysis, 999 include text indicating a re-post from another source.


- 5,647 URLs scraped into Elasticsearch

```
GET inca_alias/_search?filter_path=hits.total
{
  "query": {
    "bool": {
      "filter": [
        {
          "terms": {
            "doctype": [
              "seanhannity"
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
    "total" : 5647
  }
}

```

- 4,203 URLs which are included for analysis

```
GET inca_alias/_search?filter_path=hits.total
{
  "query": {
    "bool": {
      "filter": [
        {
          "term": {
            "should_include": true
          }
        },
        {
          "terms": {
            "doctype": [
              "seanhannity"
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
    "total" : 4203
  }
}

```

- 201 URLs where scraped text matched "Read the full story at" (case-insensitive)

```
GET inca_alias/_search?filter_path=hits.total
{
  "query": {
    "bool": {
      "filter": [
        {
          "term": {
            "should_include": true
          }
        },
        {
          "terms": {
            "doctype": [
              "seanhannity"
            ]
          }
        },
        {
          "match_phrase": {
            "article_maintext": "Read the full story at"
          }
        }
      ]
    }
  }
  
---

{
  "hits" : {
    "total" : 201
  }
}

```

- 798 URLs where scraped text matched "Read the full report at" (case-insensitive)

```
GET inca_alias/_search?filter_path=hits.total
{
  "query": {
    "bool": {
      "filter": [
        {
          "term": {
            "should_include": true
          }
        },
        {
          "terms": {
            "doctype": [
              "seanhannity"
            ]
          }
        },
        {
          "match_phrase": {
            "article_maintext": "Read the full report at"
          }
        }
      ]
    }
  }
}

---

{
  "hits" : {
    "total" : 798
  }
}
```