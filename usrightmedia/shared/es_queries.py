def query_tw_author_id(author_id):
    """ES query by Twitter's author_id

    Args:
        author_id (str)

    Returns:
        ES query (JSON)

    Note:
        INCA

    """
    return {
        "query": {
            "bool": {
                "filter": [
                    {"term": {"doctype": "tweets2"}},
                    {"match": {"author_id": author_id}},
                ]
            }
        }
    }


def query_tw_username(username):
    """ES query by Twitter's author.username

    Args:
        username (str)

    Returns:
        ES query (JSON)

    """
    return {
        "query": {
            "bool": {
                "filter": [
                    {"term": {"doctype": "tweets2"}},
                    {"match": {"author.username": username}},
                ]
            }
        }
    }


def query_tw_field_exists(field):
    """ES query within documents pulled from Twitter API v2

    Args:
        field (str)

    Returns:
        ES query (JSON)

    """

    return {
        "query": {
            "bool": {
                "filter": [
                    {"term": {"doctype": "tweets2"}},
                    {"exists": {"field": field}},
                ]
            }
        }
    }


def query_doctypes(doctypes):
    """ES query for specified doctypes

    Args:
        doctypes (list)

    Returns:
        ES query (JSON)

    """
    return {"query": {"terms": {"doctype": doctypes}}}


def spot_check_by_query(myinca, query, n_examples=5):
    """Spot-check a sample of docs.

    Args:
        myinca (object): INCA instance
        query (dict): elasticsearch query
        n_examples (int): number of examples to return

    Returns:
        list of documents (dict)

    """
    generator = myinca.database.document_generator(query=query)

    docs = []
    for n, doc in enumerate(generator):
        if n >= n_examples:
            break
        docs.append(doc)
    return docs


def query_by_ids(ids):
    """Get documents from ES based on specified ID.

    Args:
        ids (list): selected IDs
        fields (list): selected fields

    Returns:
        search_params (dict): ES query
    """
    search_params = {"query": {"terms": {"_id": ids}}}
    return search_params
