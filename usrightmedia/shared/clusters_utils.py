"""Contains functions used to manipulate a multi-cluster dataframe for dyadic comparison.

The multi-cluster dataframe is tidy-formatted:

cluster_id	    cluster_size    doc_id                      doc_publish_date	        doc_title   doctype         doctype_ideo    doc_topic   doc_tweeted
softcos05_11018	2	            OneAmericaNews_587648558	2017-03-01T13:15:24+00:00	...         oneamericanews  alt             topic2
softcos05_11018	2	            FoxNews_587764050	        2017-03-01T16:03:00+00:00	...         foxnews         est             topic2
softcos05_11019	2	            GatewayPundit_782931861	    2017-02-28T09:10:19+00:00	...         gatewaypundit   alt             topic3
softcos05_11019	2	            DailyCaller_1000717587	    2017-03-01T13:55:14+00:00	...         dailycaller     est             topic1

"""
import datetime
import itertools
import logging
import os


import plotnine as p9
from mizani.breaks import date_breaks
from mizani.formatters import percent_format

# TODO: remove this import
import random
from collections import Counter

LOGGER = logging.getLogger("clusters_utils")

import pandas as pd

# For retrieving topic assignments and (re-)tweets
from inca import Inca

myinca = Inca()

from usrightmedia.shared.es_queries import query_by_ids
from usrightmedia.shared.media_references import get_media_outlet_ideo

df_ideo = get_media_outlet_ideo()
DOCTYPES = sorted(df_ideo.loc[df_ideo["ideo_category"] == "right"]["outlet_std"])
ALT_RIGHT_DOCTYPES = list(
    df_ideo.loc[df_ideo["ideo_subcategory"] == "alternative right"]["outlet_std"]
)
EST_RIGHT_DOCTYPES = list(
    df_ideo.loc[df_ideo["ideo_subcategory"] == "established right"]["outlet_std"]
)
IDEOS = {"established right": "est", "alternative right": "alt"}

# =============================================================================================================
# DATA: CLUSTERS

# -------------------------------------------------------------------------------------------------------------
# functions to load multi-cluster dataframe


def load_clusters(df_dir, similarity_threshold):
    """Load multi-cluster dataframe by similarity threshold. Includes single-document clusters.

    Sort the documents within each cluster by publish date.

    Args:
        df_dir (string): path to directory containing the multi-cluster dataframes
        similarity_threshold (string): e.g., "softcos06"

    Returns:
        df (dataframe): contains clusters of size 1+

    """

    df = pd.read_pickle(os.path.join(df_dir, f"clusters_{similarity_threshold}.pkl"))
    df["doc_publish_date"] = df["doc_publish_date"].map(
        lambda d: datetime.datetime.fromisoformat(d)
    )
    df = df.sort_values(
        by=["cluster_id", "doc_publish_date"], ascending=True
    ).reset_index(drop=True)

    return df


def load_multi_doc_clusters_only(df_dir, similarity_threshold):
    """Get clusters composed of 2+ documents in either a tidy-formatted dataframe.

    Args:
        df_dir (string): path to directory containing the multi-cluster dataframes
        similarity_threshold (string): e.g., "softcos06"

    Returns:
        df_gt1 (dataframe): contains clusters of size > 1

    """
    df = load_clusters(df_dir, similarity_threshold)
    df_gt1 = df.loc[df["cluster_size"] > 1].reset_index(drop=True)
    return df_gt1


# -------------------------------------------------------------------------------------------------------------
# document-level: add columns to multi-cluster dataframe


def extract_doctype(doc_id):
    """Extract the doctype from the doc_id. Lowercased to match the doctype in ES."""
    doctype = doc_id[0 : doc_id.find("_")].lower()
    return doctype


def get_ideo_subcategory(doctype):
    """Get the doctype's ideological subcategory. Each doctype corresponds with an outlet."""
    ideo = (
        df_ideo.loc[df_ideo["outlet_std"] == doctype]
        .reset_index(drop=True)
        .iloc[0]["ideo_subcategory"]
    )
    ideo_abbr = IDEOS[ideo]
    return ideo_abbr


def get_doc_topic(doc_id):
    """Return the topic assignment of the doc_id."""
    # TODO: remove this function once topic modeling is done
    # use get_field_value_for_ids to retrieve the primary topic assignment per doc
    topic = random.sample(["topic1", "topic2", "topic3"], 1)[0]
    return topic


def get_field_value_for_ids(doc_ids, field="tweets2_url_ids"):
    """Return the field value for a list of doc_ids.

    Args:
        doc_ids (list of str): list of document IDs ("_id" in ES)
        field (str): document field to retrieve from ES

    Returns:
        df_tw (dataframe): row index values are the doc_ids
                           one column named according to field

    """

    # initialize dataframe to populate
    df_tw = pd.DataFrame(index=doc_ids)
    df_tw[field] = [[] for _ in range(len(df_tw))]

    # use scroll query because ES returns at most 10,000 docs per window
    for doc in myinca.database.scroll_query(query_by_ids(doc_ids)):
        df_tw.at[doc["_id"], field] = doc["_source"][field]

    return df_tw


# =============================================================================================================
# FILTER: CLUSTERS

# -------------------------------------------------------------------------------------------------------------
# document-level: internal helper functions


def _doc_with_odd_publish_date(doc):
    """Check if the doc is published exactly at 05:00 UTC (midnight EST)"""
    publish_date = doc["doc_publish_date"]
    timezone = publish_date.timetz().tzname()
    hour = publish_date.hour
    minute = publish_date.minute
    second = publish_date.second
    microsecond = publish_date.microsecond
    nanosecond = publish_date.nanosecond
    if all(
        [
            timezone == "UTC",
            hour == 5,
            minute == 0,
            second == 0,
            microsecond == 0,
            nanosecond == 0,
        ]
    ):
        return True
    else:
        return False


def _rmv_docs_with_odd_publish_date(docs):
    """Recursively remove the first document in a cluster if it has an odd publish date."""
    try:
        first_doc = docs[0]
        if _doc_with_odd_publish_date(first_doc):
            LOGGER.debug(
                f"excluding doc_id {first_doc['doc_id']} b/c it has an odd publish date: {first_doc['doc_publish_date']}"
            )
            docs.pop(0)
            if len(docs) > 0:
                _rmv_docs_with_odd_publish_date(docs)
    except IndexError:
        # IndexError: list index out of range
        # empty list: the cluster does not have any docs
        pass
    return docs


# -------------------------------------------------------------------------------------------------------------
# cluster-level: internal helper functions


def _keep_clusters_with_years(df_clusters, years=[2016]):
    """Keep clusters where the first document was published in one of the specified yaers."""

    LOGGER.info(f"years to keep: {years}")

    # dfcx: dataframe of multiple clusters
    dfcx = df_clusters
    cids = list(dfcx["cluster_id"].unique())

    # if no clusters match, an empty dataframe with column headers is returned
    df_base = pd.DataFrame(columns=dfcx.columns)
    dfs_cid = [df_base]

    for cid in cids:
        LOGGER.debug(f"filtering cid: {cid}")
        # df_cid: dataframe of one cluster
        df_cid = dfcx.loc[dfcx["cluster_id"] == cid].reset_index(drop=True)
        LOGGER.debug(f"cluster_id: {df_cid.iloc[0]['cluster_id']}")
        # keep if the first document in the cluster is published in one of the specified years
        # looping through the clusters rather than filtering dfcx all at once b/c clusters can bridge across years
        # e.g., clusters starting in Dec 2019 can continue into Jan 2020
        first_doc_year = df_cid.iloc[0]["doc_publish_date"].year
        if first_doc_year in years:
            dfs_cid.append(df_cid)
            LOGGER.debug(
                f"keeping cluster_id {cid} b/c the first doc is assigned {first_doc_year}"
            )

    df_clusters_filtered = pd.concat(dfs_cid).reset_index(drop=True)

    return df_clusters_filtered


def _keep_clusters_with_topics(df_clusters, topics=["topic1"]):
    """Keep clusters where the first document is assigned one of the specified topics."""

    LOGGER.info(f"topics to keep: {topics}")

    # dfcx: dataframe of multiple clusters
    dfcx = df_clusters
    cids = list(dfcx["cluster_id"].unique())

    # if no clusters match, an empty dataframe with column headers is returned
    df_base = pd.DataFrame(columns=dfcx.columns)
    dfs_cid = [df_base]

    for cid in cids:
        LOGGER.debug(f"filtering cid: {cid}")
        # df_cid: dataframe of one cluster
        df_cid = dfcx.loc[dfcx["cluster_id"] == cid].reset_index(drop=True)
        LOGGER.debug(f"cluster_id: {df_cid.iloc[0]['cluster_id']}")
        # keep if the first document in the cluster is assigned to one of the specified topics
        # most, if not all, docs per cluster should have the same assigned topic
        first_doc_topic = df_cid.iloc[0]["doc_topic"]
        if first_doc_topic in topics:
            dfs_cid.append(df_cid)
            LOGGER.debug(
                f"keeping cluster_id {cid} b/c the first doc is assigned {first_doc_topic}"
            )

    df_clusters_filtered = pd.concat(dfs_cid).reset_index(drop=True)

    return df_clusters_filtered


def _filter_clusters_rmv_odd_publish_date(df_clusters):
    """Only keep a document if it is not published at exactly 05:00 UTC (midnight EST)."""

    # dfcx: dataframe of multiple clusters
    dfcx = df_clusters
    cids = list(dfcx["cluster_id"].unique())

    # if no clusters match, an empty dataframe with column headers is returned
    df_base = pd.DataFrame(columns=dfcx.columns)
    dfs_cid = [df_base]

    for cid in cids:
        LOGGER.debug(f"filtering cid: {cid}")
        df_cid = dfcx.loc[dfcx["cluster_id"] == cid]
        # represent each document within the cluster as a dictionary
        docs = [row.to_dict() for _, row in df_cid.iterrows()]
        docs = _rmv_docs_with_odd_publish_date(docs)
        df_cid = pd.DataFrame(docs)
        dfs_cid.append(df_cid)

    LOGGER.debug(f"length of dfs_cid: {len(dfs_cid)}")
    df_clusters_filtered = pd.concat(dfs_cid).reset_index(drop=True)
    return df_clusters_filtered


# -------------------------------------------------------------------------------------------------------------
# cluster-level: public functions


def filter_clusters(
    df_clusters,
    filters={"years": [], "topics": []},
    rmv_docs_with_odd_publish_date_ind=True,
):
    """Returns a dataframe of filtered clusters based on the conditions.

    Args:
        df_clusters (dataframe): tidy-formatted dataframe containing multiple clusters
        filters (dict):
            years (list of int):
                - e.g., [2016, 2017]
                - if the list is empty, all years are kept
            topics (list of str):
                e.g., ["topic1", "topic2"]
                - if the list is empty, all topics are kept

    Returns:
        df_clusters_filtered (dataframe): filtered version of df_clusters

    """
    # dfcx: dataframe containing multiple clusters
    dfcx = df_clusters

    if rmv_docs_with_odd_publish_date_ind:
        LOGGER.debug(f"filtering documents with odd publish dates...")
        dfcx = _filter_clusters_rmv_odd_publish_date(dfcx)

    # if the user explicitly says to keep all possible values for a particular filter,
    # skip running the respective filter function
    # TODO: update topics
    all_years_ind = sorted(filters["years"]) == sorted(list(range(2016, 2021)))
    all_topics_ind = sorted(filters["topics"]) == sorted(
        list(["topic1", "topic2", "topic3"])
    )

    if len(filters["years"]) > 0 and not all_years_ind:
        LOGGER.debug(f"filtering clusters based on year(s)...")
        dfcx = _keep_clusters_with_years(dfcx, years=filters["years"])
    else:
        # keep all years
        pass

    if len(filters["topics"]) > 0 and not all_topics_ind:
        LOGGER.debug(f"filtering clusters based on topic(s)...")
        dfcx = _keep_clusters_with_topics(dfcx, topics=filters["topics"])
    else:
        # keep all topics
        pass

    df_clusters_filtered = dfcx
    LOGGER.debug(f"finished filtering clusters")

    return df_clusters_filtered


def get_examples_with_odd_dates(df_clusters, n_examples=5):
    """Find clusters with odd dates. Return n_examples.

    Args:
        df_clusters (dataframe): multi-cluster dataframe
        n_examples (int): number of clusters to return

    Returns:
        df_clusters_examples (dataframe)

    """

    dfcx = df_clusters
    cids = list(dfcx["cluster_id"].unique())

    # if no clusters match, an empty dataframe with column headers is returned
    df_base = pd.DataFrame(columns=dfcx.columns)
    dfs_cid = [df_base]

    for cid in cids:
        LOGGER.debug(f"example cid: {cid}")
        df_cid = dfcx.loc[dfcx["cluster_id"] == cid]
        docs_cid = [row.to_dict() for _, row in df_cid.iterrows()]
        # check if any document within the cluster has an odd publish date
        any_odd_publish_dates = any([_doc_with_odd_publish_date(d) for d in docs_cid])
        if any_odd_publish_dates and len(docs_cid) > 1:
            dfs_cid.append(df_cid)
        if len(dfs_cid) > n_examples:
            break

    LOGGER.debug(f"number of odd-date examples: {len(dfs_cid)}")
    df_clusters_examples = pd.concat(dfs_cid).reset_index(drop=True)
    return df_clusters_examples


# =============================================================================================================
# DATA: DYADS

# -------------------------------------------------------------------------------------------------------------
# convert multi-cluster dataframe to dictionary of cluster_id:dyads (key:value)


def _make_dyads(df_cluster):
    """Creates dyads for a given cluster.

    Args:
        df_cluster (dataframe): The dataframe represents a cluster. Each row is a document.

    Returns:
        dyads (list of tuples): Each tuple contains 2 items. Each item is a dict which represents a document.

    """
    docs = [row.to_dict() for _, row in df_cluster.iterrows()]
    doc0 = docs[0]  # initial doc

    dyads_cid = []
    for n in range(1, len(docs)):
        doc1 = docs[n]
        dyad = (doc0, doc1)
        dyads_cid.append(dyad)

    return dyads_cid


def get_clusters_as_dyads(df_clusters):
    """Converts a multi-cluster dataframe into a dictionary.

    Args:
        df_clusters (dataframe):  The dataframe contains multiple clusters per cluster_id where each row is a document.

    Returns:
        dyads_cx (dictionary): the keys are the "cluster_id" (str) and the values are lists.
            Each list is either:
            - empty due to processing a single-document cluster (no dyad can be created), or
            - contains 1+ two-item tuples where each item is a dictionary (document)

    """
    dfcx = df_clusters
    cids = list(dfcx["cluster_id"].unique())

    dyads_cx = {}
    for cid in cids:
        LOGGER.debug(f"making dyadic version of cid: {cid}")
        df = dfcx.loc[dfcx["cluster_id"] == cid]
        dyads_cid = _make_dyads(df)
        dyads_cx[cid] = dyads_cid

    return dyads_cx


# =============================================================================================================
# FILTER: DYADS

# -------------------------------------------------------------------------------------------------------------
# dyad-level: internal helper functions


def _is_bn_diff_doctypes(dyad):
    """Check if a dyad is between two different doctypes.

    Args:
        dyad (tuple): two-item tuple where each item is a dict which represents a document

    Returns:
        ind (bool): True if the dyad is between two different doctypes

    """
    if dyad[0]["doctype"] != dyad[1]["doctype"]:
        ind = True
    else:
        ind = False
    return ind


def _keep_dyads_bn_diff_doctypes_only(dyads_cid):
    """Given a cluster's dyads, only keep the dyads which are between two different doctypes.

    Args:
        dyads_cid (list): list of two-item tuples where each item is a dict which represents a document

    Returns:
        dyads_cid_filtered (list): filtered version of dyads_cid

    """

    dyads_cid_filtered = []
    for dyad in dyads_cid:
        if _is_bn_diff_doctypes(dyad):
            LOGGER.debug(f"keeping dyad b/n {dyad[0]['doctype']}-{dyad[1]['doctype']}")
            dyads_cid_filtered.append(dyad)
        else:
            # don't add the dyad if the two documents have the same doctype
            LOGGER.debug(
                f"excluding dyad b/n {dyad[0]['doctype']}-{dyad[1]['doctype']}"
            )
            pass

    return dyads_cid_filtered


def _keep_first_doctype_pair_only(dyads_cid):
    """Given a cluster's dyads, only keep the first instance of a doctype-pair.

    e.g., if a cluster contains two instances of "foxnews-breitbart", only the first instance is kept.

    Args:
        dyads_cid (list): list of two-item tuples where each item is a dict which represents a document

    Returns:
        dyads_cid_filtered (list): filtered version of dyads_cid

    """

    dyads_cid_filtered = []

    doctype_pairs = []
    for dyad in dyads_cid:
        doctype0 = dyad[0]["doctype"]
        doctype1 = dyad[1]["doctype"]
        doctype_pair = (doctype0, doctype1)
        if doctype_pair not in doctype_pairs:
            LOGGER.debug(f"keeping dyad b/n {doctype0}-{doctype1}")
            doctype_pairs.append(doctype_pair)
            dyads_cid_filtered.append(dyad)
        else:
            LOGGER.debug(f"keeping dyad b/n {doctype0}-{doctype1}")
            # don't add the dyad if the doctype-pair has already appeared in the cluster
            pass

    return dyads_cid_filtered


# -------------------------------------------------------------------------------------------------------------
# dyad-level: public functions


def filter_dyads(
    dyads_cx, keep_dyads_bn_diff_doctypes_only=True, keep_first_doctype_pair_only=True
):
    """Returns a dictionary of clusters based on the dyad-level filter conditions.

    Args:
        dyads_cx (dict): Dictionary containing multiple clusters.
                         Keys are cluster_ids and values are lists of two-item tuples.
                         Each item in a tuple is a dict representing a document.

        keep_dyads_bn_diff_doctypes_only (bool): if True, remove dyads between the same doctype.

        keep_first_doctype_pair_only (bool): if True, keep only the first instance of a doctype-pair.

    Returns:
        dyads_cx_filtered (dict): filtered version of dyads_cx

    """

    cids = dyads_cx.keys()

    dyads_cx_filtered = {}
    for cid in cids:
        LOGGER.debug(f"filtering dyads for cid: {cid}")
        dyads_cid = dyads_cx[cid]
        if keep_dyads_bn_diff_doctypes_only:
            LOGGER.debug(f"filter for keep_dyads_bn_diff_doctypes_only...")
            dyads_cid = _keep_dyads_bn_diff_doctypes_only(dyads_cid)
        if keep_first_doctype_pair_only:
            LOGGER.debug(f"filter for keep_first_doctype_pair_only...")
            dyads_cid = _keep_first_doctype_pair_only(dyads_cid)
        dyads_cx_filtered[cid] = dyads_cid
        LOGGER.debug(f"finished filtering dyads")

    return dyads_cx_filtered


# =============================================================================================================
# DATA: PAIRS (e.g, doctype or doctype_ideo)

# -------------------------------------------------------------------------------------------------------------
# functions for managing data


def extract_dyads(dyads_cx):
    """Simplify the data structure from cluster-level to dyad-level.

    Each dyad is a two-item tuple. Each item is a dict.
    The cluster_id is still available within each dict.
    """

    # see comment by intuited in https://stackoverflow.com/a/952952
    dyads = list(itertools.chain.from_iterable(dyads_cx.values()))

    return dyads


def get_matched_dyads(
    dyads,
    d0_key="doctype",
    d1_key="doctype",
    d0_values=["foxnews"],
    d1_values=["foxnews"],
):
    """Filter which returns dyads which match the specified conditions.

    Args:
        dyads (list): list of 2-item tuples. Each item is a dictionary (document).
        d0_key (str)
        d1_key (str)
        d0_values (list): any values to match
        d1_values (list): any values to match

    Returns:
        matched_dyads (list): filtered version of dyads

    """

    matched_dyads = []
    for dyad in dyads:
        d0 = dyad[0]
        d1 = dyad[1]
        if d0[d0_key] in d0_values and d1[d1_key] in d1_values:
            matched_dyads.append(dyad)

    return matched_dyads


def get_df_tidy_pairs(dyads):
    """Get a tidy-formatted dataframe where each row represents a dyad.

    Args: dyads (list of 2-item tuples); each item is a dict which represents a document.

    Returns:
        df_dyads (dataframe)
        columns: publish_date, publish_year, doctype0,
                 doctype1, doctype_ideo0, doctype_ideo1,
                 doctype_pair, doctype_ideo_pair

    """
    pairs = []
    for dyad in dyads:
        publish_date = dyad[0]["doc_publish_date"]
        publish_year = datetime.datetime(publish_date.year, 1, 1)
        doctype0 = dyad[0]["doctype"]
        doctype1 = dyad[1]["doctype"]
        doctype_ideo0 = dyad[0]["doctype_ideo"]
        doctype_ideo1 = dyad[1]["doctype_ideo"]
        pair = (
            publish_date,
            publish_year,
            doctype0,
            doctype1,
            doctype_ideo0,
            doctype_ideo1,
        )
        pairs.append(pair)

    df_dyads = pd.DataFrame(
        pairs,
        columns=[
            "publish_date",
            "publish_year",
            "doctype0",
            "doctype1",
            "doctype_ideo0",
            "doctype_ideo1",
        ],
    )
    df_dyads["doctype_to_doctype"] = df_dyads.apply(
        lambda r: f"{r['doctype0']}_{r['doctype1']}", axis=1
    )
    df_dyads["doctype_ideo_to_doctype_ideo"] = df_dyads.apply(
        lambda r: f"{r['doctype_ideo0']}_{r['doctype_ideo1']}", axis=1
    )
    df_dyads["doctype_to_doctype_ideo"] = df_dyads.apply(
        lambda r: f"{r['doctype0']}_{r['doctype_ideo1']}", axis=1
    )
    df_dyads["doctype_ideo_to_doctype"] = df_dyads.apply(
        lambda r: f"{r['doctype_ideo0']}_{r['doctype1']}", axis=1
    )
    return df_dyads


# -------------------------------------------------------------------------------------------------------------
# functions for formatting data


def get_pair_template(elements, order_matters=True):
    """Template dictionary used for storing stats.

    Every element-pair is included, even if there are no actual instances.

    Args:
        elements (list of str): doctypes or ideos
        order_matters (bool): if True, the keys are created for each direction of an element-pair.
                              e.g., "foxnews-breitbart" and "breitbart-foxnews" are included separately.
                              if False, only the sorted version ("breitbart-foxnews") is added as a key.

    Returns:
        dict_pairs (dict):
            the dict's keys are 2-item tuples representing doctype pairs
            the dict's values are initialized to 0.

    """

    if order_matters:
        # directional pairs including self-self
        # to exclude self-self: list(itertools.permutations(elements, 2))
        pairs = list(itertools.product(elements, repeat=2))
    else:
        # non-directional pairs including self-self
        # to exclude self-self: list(itertools.combinations(elements, 2))
        pairs = list(itertools.combinations_with_replacement(elements, 2))

    # https://stackoverflow.com/a/2244026
    dict_pairs = {key: 0 for key in pairs}

    return dict_pairs


# -------------------------------------------------------------------------------------------------------------
# functions for calculating stats


def count_pairs(dyads, key="doctype"):
    """Get the count of pairs for a list of dyads. Order matters.
    E.g., the count of "foxnews-breitbart" is separate from "breitbart-foxnews".

    Args:
        dyads (list of tuples): Each 2-item tuple is made up of dicts. Each dict is a document.
        key (str): element type; "doctype" or "doctype_ideo"

    Returns:
        summary (dict):
            Keys are tuples representing doctype-pairs or ideo-pairs.
            Values are the count of instances (int).

    """

    # setup a template
    if key == "doctype":
        summary = get_pair_template(DOCTYPES, order_matters=True)
    elif key == "doctype_ideo":
        summary = get_pair_template(IDEOS.values(), order_matters=True)

    # get the actual counts
    pairs = [(dyad[0][key], dyad[1][key]) for dyad in dyads]
    counter = Counter(pairs)

    # hydrate the template
    for k in counter:
        summary[k] = counter[k]

    return summary


def total_pairs(dyads, key="doctype", expand=True):
    """Get the total count of pairs for a list of dyads. Order does not matter.
        E.g., the total count means that the individual counts
              for "foxnews-breitbart" and "breitbart-foxnews" are combined together.

    Args:
        dyads (list of tuples): Each 2-item tuple is made up of dicts. Each dict is a document.
        key (str): element type; "doctype" or "doctype_ideo"
        expand (bool):

    Returns:
        summary (dict):
            Keys are tuples representing doctype-pairs or ideo-pairs.
            Values are the count of instances (int).

    """

    # setup a template
    if key == "doctype":
        summary = get_pair_template(DOCTYPES, order_matters=False)
    elif key == "doctype_ideo":
        summary = get_pair_template(IDEOS.values(), order_matters=False)

    # get the actual counts
    pairs = [(dyad[0][key], dyad[1][key]) for dyad in dyads]
    # the sort makes pairs identical as long as they have the same elements
    sorted_pairs = [tuple(sorted(pair)) for pair in pairs]
    counter = Counter(sorted_pairs)

    # hydrate the template
    for k in counter:
        summary[k] = counter[k]

    if expand:
        summary = _expand_total_pairs(summary)

    return summary


def _expand_total_pairs(total_pairs):
    """Expands total_pairs so that it has one key per direction.
    e.g., 'breitbart-foxnews' and 'foxnews-breitbart' exist as keys.

    If expansion is skipped, then total_pairs only has one key per pair of (unordered) elements.
    e.g., 'breitbart-foxnews' exists as a key but 'foxnews-breitbart' does not.

    The total per element-pair is the same value for both directions.
    e.g., 'breitbart-foxnews' and 'foxnews-breitbart' are assigned the same total count.

    """

    total_pairs_expanded = {}
    for k, v in total_pairs.items():
        total_pairs_expanded[(k[0], k[1])] = v
        total_pairs_expanded[(k[1], k[0])] = v
    total_pairs_expanded = dict(sorted(total_pairs_expanded.items()))

    return total_pairs_expanded


def proportion_pairs(dyads, key="doctype"):
    """Get the proportion of directional pairs involving the same two elements for a list of dyads.
        E.g., the proportion of "foxnews-breitbart" is separate from "breitbart-foxnews".

    Args:
        dyads (list of tuples): Each 2-item tuple is made up of dicts. Each dict is a document.
        key (str): element type; "doctype" or "doctype_ideo"

    Returns:
        proportions (dict):
            Keys are tuples representing doctype-pairs or ideo-pairs.
            Values are the count of instances (int).

    """

    # the order of elements within a dyad matters
    counts = count_pairs(dyads, key=key)

    # the order of elements within a dyad does not matter
    # expand=True so counts and totals have matching keys
    totals = total_pairs(dyads, key=key, expand=True)

    # https://stackoverflow.com/a/18554039
    shared_pairs = counts.keys() & totals.keys()

    # https://stackoverflow.com/a/11840128
    proportions = {}
    for pair in shared_pairs:
        try:
            proportions[pair] = counts[pair] / totals[pair]
        except ZeroDivisionError:
            proportions[pair] = 0

    return proportions


def summarize_pairs(dyads, key="doctype", flatten_index=True):
    """Get a dataframe summary with 'count', 'proportion', and 'total' columns per directed element-pair.
        Note: 'total' refers to count of the element-pair in both directions.

    Args:
        dyads (list of tuples): Each 2-item tuple is made up of dicts. Each dict is a document.
        key (str): element type; "doctype" or "doctype_ideo"
        flatten_index (bool): If True, the index values are 2-item tuples such as (breitbart, foxnews).
                              If False, a multi-index is returned where the first item in the tuple
                                        is higher in the hierarchy than the second item.

    Returns:
        df_summary (dataframe)

    """

    counts = count_pairs(dyads, key=key)
    proportions = proportion_pairs(dyads, key=key)
    totals = total_pairs(dyads, key=key, expand=True)

    df_counts = pd.DataFrame.from_dict(
        counts, orient="index", columns=["count"]
    )  # count of directional pairs
    df_proportions = pd.DataFrame.from_dict(
        proportions, orient="index", columns=["proportion"]
    )  # proportion of directional pairs over total pairs
    df_totals = pd.DataFrame.from_dict(
        totals, orient="index", columns=["total"]
    )  # total pairs (non-directional)

    # https://stackoverflow.com/a/45383919
    # after pd.concat, the index splits the 2-item tuple into a hierarchical index
    df_summary = pd.concat([df_counts, df_proportions, df_totals], axis=1)
    if flatten_index:
        df_summary.index = df_summary.index.to_series()
    df_summary = df_summary.sort_index(axis=0, ascending=True)

    return df_summary


# =============================================================================================================
# DYADIC COMPARISON

# -------------------------------------------------------------------------------------------------------------
# dyad-level: public functions


def make_dyadic_comparison(dyads, key="doctype", version="count"):
    """Use a pivot table to summarize the element-pairs.

    Args:
        dyads (list of tuples): Each 2-item tuple is made up of dicts. Each dict is a document.
        key (str): element type; "doctype" or "doctype_ideo"
        version (str): "count" or "proportion"
        margins (bool): "add all row / columns (e.g. for subtotal / grand totals)"
                        https://pandas.pydata.org/docs/reference/api/pandas.pivot_table.html

    Returns:
        dyadic_comparison (dataframe): "count" or "proportion" version of dyadic comparison


    """

    summary = summarize_pairs(dyads, key=key, flatten_index=True)
    summary = summary.reset_index()
    summary["pair0"] = summary["index"].map(lambda pair: pair[0])
    summary["pair1"] = summary["index"].map(lambda pair: pair[1])
    summary = summary[["pair0", "pair1", "count", "proportion"]]

    # df_count is used for both "count" and "proportion" versions
    df_count = summary.pivot_table(
        values="count",
        index="pair0",
        columns="pair1",
        aggfunc="sum",
        margins=True,
    )

    if version == "count":
        dyadic_comparison = df_count

    elif version == "proportion":
        df_proportion = summary.pivot_table(
            values="proportion",
            index="pair0",
            columns="pair1",
            aggfunc="sum",  # placeholder margins
            margins=True,
        )

        # df_pair0: row totals from "count" version
        df_pair0 = (
            pd.DataFrame(df_count.loc[:, "All"])
            .reset_index()
            .rename(columns={"All": "pair0_total"})
        )

        # df_pair1: column totals from "count" version
        df_pair1 = (
            pd.DataFrame(df_count.loc["All", :])
            .reset_index()
            .rename(columns={"All": "pair1_total"})
        )

        # calculate the proportions with a helper dataframe (df_pair)
        df_pair = df_pair0.merge(
            right=df_pair1,
            how="inner",
            left_on="pair0",
            right_on="pair1",
            validate="one_to_one",
        )
        df_pair["pair_total"] = df_pair["pair0_total"] + df_pair["pair1_total"]
        df_pair["pair0_proportion"] = df_pair["pair0_total"] / df_pair["pair_total"]
        df_pair["pair1_proportion"] = df_pair["pair1_total"] / df_pair["pair_total"]

        df_proportion.loc[:, "All"] = df_pair["pair0_proportion"].values
        df_proportion.loc["All", :] = df_pair["pair1_proportion"].values

        # replace NaNs with 0
        # NaNs occur when 'pair_total' is zero
        df_proportion = df_proportion.fillna(0)

        dyadic_comparison = df_proportion

    # tidy up the output
    dyadic_comparison = (
        dyadic_comparison.sort_index(axis=0, ascending=True)
        .sort_index(axis=1, ascending=True)
        .rename_axis(None, axis=0)
        .rename_axis(None, axis=1)
    )

    return dyadic_comparison


# -------------------------------------------------------------------------------------------------------------
# dataframe-level: helper functions


def add_ideo_hierarchical_axes(doctype_dyadic_comparison, flatten_axes=[]):
    """Adds doctype_ideo as parent hierarchy to doctype.
    Only used with dyadic comparison where key="doctype" and version="count".

    Based on cxrodgers's post at https://stackoverflow.com/a/56278736

    Args:
        doctype_dyadic_comparison

    Returns:
        dyadic_comparison with hierarchical index

    """

    # leave the original comparison unchanged
    dyadic_comparison = doctype_dyadic_comparison.copy(deep=True)

    # add multi-index hierarchy with doctype_ideo_subcategory
    dict_index = {
        key: get_ideo_subcategory(key) if key in list(df_ideo["outlet_std"]) else "All"
        for key in dyadic_comparison.index
    }
    dict_columns = {
        key: get_ideo_subcategory(key) if key in list(df_ideo["outlet_std"]) else "All"
        for key in dyadic_comparison.columns
    }

    # Convert indices to dataframes
    old_idx = dyadic_comparison.index.to_frame()
    old_cols = dyadic_comparison.columns.to_frame()
    # Insert new levels
    old_idx.insert(0, "pair0_ideo", dict_index.values())
    old_cols.insert(0, "pair1_ideo", dict_columns.values())
    # Convert back to MultiIndex
    dyadic_comparison.index = pd.MultiIndex.from_frame(old_idx)
    dyadic_comparison.columns = pd.MultiIndex.from_frame(old_cols)

    # sort rows and columns by ideo
    dyadic_comparison = dyadic_comparison.sort_index(axis=0, ascending=True).sort_index(
        axis=1, ascending=True
    )

    if len(flatten_axes) > 0:

        if 0 in flatten_axes and 1 in flatten_axes:
            # flatten axis 0 and axis 1
            dyadic_comparison = (
                dyadic_comparison.groupby(level=["pair0_ideo"], axis=0)
                .sum()
                .groupby(level=["pair1_ideo"], axis=1)
                .sum()
            )

        elif 0 in flatten_axes and 1 not in flatten_axes:
            # flatten axis 0 only
            dyadic_comparison = dyadic_comparison.groupby(
                level=["pair0_ideo"], axis=0
            ).sum()

        elif 0 not in flatten_axes and 1 in flatten_axes:
            # flatten axis 1 only
            dyadic_comparison = dyadic_comparison.groupby(
                level=["pair1_ideo"], axis=1
            ).sum()

    return dyadic_comparison


# -------------------------------------------------------------------------------------------------------------
# dyad-level: plotting functions


def plot_yearly_dyadic_comparison(
    dyads, title="", display_pair="doctype_ideo_to_doctype_ideo"
):
    """Chart for dyadic comparison.

    Args:
        dyads (list of 2-item tuples): each item is a dict representing a document
        title (string)
        display_pair (string): "doctype_ideo_to_doctype_ideo" or "doctype_to_doctype"

    Returns:
        plot (plotnine chart)

    """

    # prep data
    df_tidy_pairs = get_df_tidy_pairs(dyads)

    df_yearly_totals = (
        df_tidy_pairs.groupby(["publish_year"])
        .size()
        .to_frame()
        .rename(columns={0: "total_year"})
    )

    p9_data = (
        df_tidy_pairs.groupby(["publish_year", display_pair])
        .size()
        .to_frame()
        .reset_index()
        .rename(columns={0: "count_year"})
    )
    p9_data["total_year"] = p9_data["publish_year"].map(
        lambda r: df_yearly_totals.loc[r]["total_year"]
    )
    p9_data["prop_year"] = p9_data["count_year"] / p9_data["total_year"]
    p9_data["percent_year_str"] = p9_data["prop_year"].map(
        lambda r: f"{round(r*100, 0)}%"
    )

    # prep plot labels (yearly total counts displayed at top of plot)
    yearly_totals = list(df_yearly_totals["total_year"])
    n_padding = len(p9_data) - len(yearly_totals)
    yearly_totals.extend([None] * n_padding)

    # prep plot colors
    if display_pair == "doctype_to_doctype":
        doctypes = p9_data["doctype_to_doctype"].unique()[0].split("_")
        doctype0 = doctypes[0]
        doctype1 = doctypes[1]

        # color is assigned alphabetically
        default_fill = {
            f"{doctype0}_{doctype1}": "#fecc5c",
            f"{doctype1}_{doctype0}": "#e31a1c",
        }

    elif display_pair == "doctype_ideo_to_doctype_ideo":
        default_fill = {
            "alt_alt": "#ffffb2",
            "alt_est": "#fecc5c",
            "est_alt": "#fd8d3c",
            "est_est": "#e31a1c",
        }

    plot_fill = {
        k: default_fill[k] for k in p9_data[display_pair].unique() if k in default_fill
    }

    # prep plot components
    chart = p9.ggplot(
        data=p9_data,
        mapping=p9.aes(
            x="publish_year", y="prop_year", color=display_pair, fill=display_pair
        ),
    )

    area = p9.geom_area(alpha=0.5, color=None, position="stack")
    hline = p9.geom_hline(yintercept=0.5, linetype="dashed", size=0.5)
    text = p9.geom_text(
        mapping=p9.aes(label="percent_year_str"),
        position="stack",
        color="black",
        va="center",
        size=9,
        show_legend=False,
    )
    label = p9.geom_label(
        mapping=p9.aes(x="publish_year", label="total_year", y=1.15),
        color="black",
        fill="white",
        va="top",
        size=9,
        show_legend=False,
    )

    # combine plot components and modify scales
    plot = (
        chart
        + area
        + hline
        + text
        + label
        + p9.scale_y_continuous(
            breaks=(0, 0.5, 1), limits=(0, 1.15), labels=percent_format()
        )
        + p9.scale_x_datetime(
            breaks=date_breaks("1 year"), date_labels="%Y", expand=(0.1, 0)
        )
        + p9.scale_fill_manual(values=list(plot_fill.values()))
    )

    # chart labels
    plot = plot + p9.labs(
        title=f"{title} ({df_yearly_totals['total_year'].sum()} dyads)",
        color="",
        alpha="",
        fill="",
        x="year",
        y="percent of dyads",
    )

    return plot


def plot_filtered_yearly_dyadic_comparison(
    dyads,
    key0="doctype",
    key1="doctype",
    values0=DOCTYPES,
    values1=DOCTYPES,
):
    """Returns 2 dyadic comparison plots, one in each direction.
       Dyads can be filtered by doctype or doctype_ideo.

    Args:
        dyads (list of 2-item tuples): each item is a dict representing a document
        key0 (str): "doctype" or "doctype_ideo"
        key1 (str): "doctype" or "doctype_ideo"
        values0 (list of strings)
        values1 (list of strings)

    Returns:
        plots (list of plotnine charts):
                idx 0 is the plot for dyads_0_to_1
                idx 1 is the plot for dyads_1_to_0

    """

    title = "Dyadic comparison"

    dyads_0_to_1 = get_matched_dyads(
        dyads,
        d0_key=key0,
        d1_key=key1,
        d0_values=values0,
        d1_values=values1,
    )

    dyads_1_to_0 = get_matched_dyads(
        dyads,
        d0_key=key1,
        d1_key=key0,
        d0_values=values1,
        d1_values=values0,
    )

    if (
        key0 == "doctype"
        and key1 == "doctype"
        and len(values0) == 1
        and len(values1) == 1
    ):

        doctype_dyads = dyads_0_to_1 + dyads_1_to_0

        # shows doctype_to_doctype in both directions
        plot = plot_yearly_dyadic_comparison(
            doctype_dyads, title=title, display_pair="doctype_to_doctype"
        )

        plots = [plot]

    else:

        # when values0 is/are leader(s), they
        # lead alternative-right outlets __% of the time
        # and established-right outlets __% of the time
        plot_0_to_1 = plot_yearly_dyadic_comparison(
            dyads_0_to_1, title=title, display_pair="doctype_ideo_to_doctype_ideo"
        )

        # when values0 is/are follower(s), they
        # follow alternative-right outlets __% of the time
        # and established-right outlets __% of the time
        plot_1_to_0 = plot_yearly_dyadic_comparison(
            dyads_1_to_0, title=title, display_pair="doctype_ideo_to_doctype_ideo"
        )

        plots = [plot_0_to_1, plot_1_to_0]

    return plots
