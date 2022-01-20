"""This module contains functions for using LDA topic modeling."""

import os
import datetime
import pandas as pd
import pickle
from gensim.models import Phrases
from gensim.corpora import Dictionary
from gensim.models import TfidfModel, LdaModel, CoherenceModel
from gensim.corpora.mmcorpus import MmCorpus
import spacy

import logging

LOGGER = logging.getLogger("topics_utils")

# python -m spacy download en_core_web_lg
nlp = spacy.load("en_core_web_lg")

INPUTS_DIR = os.path.join(
    "..", "..", "data", "02-intermediate", "08-topic-models", "01-inputs"
)
MODELS_DIR = os.path.join(
    "..", "..", "data", "02-intermediate", "08-topic-models", "02-models"
)

# =============================================================================================================
# PREPARE INPUTS: TEXT PRE-PROCESSING

"""
https://explosion.ai/demos/displacy-ent https://github.com/explosion/spaCy/blob/ed561cf428494c2b7a6790cd4b91b5326102b59d/spacy/glossary.py

# POS tags
    # Universal POS Tags
    # http://universaldependencies.org/u/pos/
    "ADJ": "adjective",
    "ADP": "adposition",
    "ADV": "adverb",
    "AUX": "auxiliary",
    "CONJ": "conjunction",
    "CCONJ": "coordinating conjunction",
    "DET": "determiner",
    "INTJ": "interjection",
    "NOUN": "noun",
    "NUM": "numeral",
    "PART": "particle",
    "PRON": "pronoun",
    "PROPN": "proper noun",
    "PUNCT": "punctuation",
    "SCONJ": "subordinating conjunction",
    "SYM": "symbol",
    "VERB": "verb",
    "X": "other",
    "EOL": "end of line",
    "SPACE": "space",

 # Named Entity Recognition
    # OntoNotes 5
    # https://catalog.ldc.upenn.edu/docs/LDC2013T19/OntoNotes-Release-5.0.pdf
    "PERSON": "People, including fictional",
    "NORP": "Nationalities or religious or political groups",
    "FACILITY": "Buildings, airports, highways, bridges, etc.",
    "FAC": "Buildings, airports, highways, bridges, etc.",
    "ORG": "Companies, agencies, institutions, etc.",
    "GPE": "Countries, cities, states",
    "LOC": "Non-GPE locations, mountain ranges, bodies of water",
    "PRODUCT": "Objects, vehicles, foods, etc. (not services)",
    "EVENT": "Named hurricanes, battles, wars, sports events, etc.",
    "WORK_OF_ART": "Titles of books, songs, etc.",
    "LAW": "Named documents made into laws.",
    "LANGUAGE": "Any named language",
    "DATE": "Absolute or relative dates or periods",
    "TIME": "Times smaller than a day",
    "PERCENT": 'Percentage, including "%"',
    "MONEY": "Monetary values, including unit",
    "QUANTITY": "Measurements, as of weight or distance",
    "ORDINAL": '"first", "second", etc.',
    "CARDINAL": "Numerals that do not fall under another type",
    # Named Entity Recognition
    # Wikipedia
    # http://www.sciencedirect.com/science/article/pii/S0004370212000276
    # https://pdfs.semanticscholar.org/5744/578cc243d92287f47448870bb426c66cc941.pdf
    "PER": "Named person or family.",
    "MISC": "Miscellaneous entities, e.g. events, nationalities, products or works of art",
    # https://github.com/ltgoslo/norne
    "EVT": "Festivals, cultural events, sports events, weather phenomena, wars, etc.",
    "PROD": "Product, i.e. artificially produced entities including speeches, radio shows, programming languages, contracts, laws and ideas",
    "DRV": "Words (and phrases?) that are dervied from a name, but not a name in themselves, e.g. 'Oslo-mannen' ('the man from Oslo')",
    "GPE_LOC": "Geo-political entity, with a locative sense, e.g. 'John lives in Spain'",
    "GPE_ORG": "Geo-political entity, with an organisation sense, e.g. 'Spain declined to meet with Belgium'",
}
"""


def preprocess_docs(docs, label, INPUTS_DIR):
    processed_docs = []
    for doc in nlp.pipe(docs):
        # Process document using Spacy NLP pipeline

        # Lemmatize tokens, remove punctuation, remove stopwords, remove certain entity types
        doc = [
            token.lemma_.lower()
            for token in doc
            if token.is_alpha
            and not token.is_stop
            and token.pos_ in ["NOUN", "ADJ", "ADV"]
            and token.ent_type_ not in ["PERSON", "DATE", "TIME", "PERCENT", "QUANTITY"]
            and token.text not in ["trump", "Trump"]
        ]

        processed_docs.append(doc)

    docs = processed_docs
    del processed_docs

    # Add bigrams to docs (only ones that appear 20 times or more).
    bigram = Phrases(docs, min_count=20)
    for idx in range(len(docs)):
        for token in bigram[docs[idx]]:
            if "_" in token:
                # Token is a bigram, add to document.
                docs[idx].append(token)

    with open(os.path.join(INPUTS_DIR, "docs", f"docs_{label}.pkl"), "wb") as handle:
        pickle.dump(docs, handle)

    return docs


# Create a dictionary representation of the documents, and filter out frequent and rare words.
def save_dictionary(docs, label, INPUTS_DIR):
    dictionary = Dictionary(docs)

    # https://radimrehurek.com/gensim/corpora/dictionary.html#gensim.corpora.dictionary.Dictionary.filter_extremes
    # Filter out words that occur too frequently or too rarely
    dictionary.filter_extremes(
        no_below=10, no_above=0.5, keep_n=100000, keep_tokens=None
    )
    dictionary.compactify()

    dictionary.save(
        os.path.join(INPUTS_DIR, "dictionaries", f"dictionary_{label}.dict")
    )
    return dictionary


def save_corpus(dictionary, docs, label, INPUTS_DIR):
    # Vectorize data: bag-of-words representation of the documents.
    corpus = [dictionary.doc2bow(doc) for doc in docs]

    tfidf = TfidfModel(corpus)
    tc = tfidf[corpus]
    corpus_tfidf = [bow for bow in tc]

    MmCorpus.serialize(
        os.path.join(INPUTS_DIR, "corpora", f"corpus_count_{label}.mm"), corpus
    )
    MmCorpus.serialize(
        os.path.join(INPUTS_DIR, "corpora", f"corpus_tfidf_{label}.mm"), corpus_tfidf
    )

    return corpus, corpus_tfidf


# =============================================================================================================
# LDA TOPIC MODELING


def load_inputs(corpus_type, docs_type, INPUTS_DIR):
    inputs = {}
    inputs["dictionary"] = Dictionary.load(
        os.path.join(INPUTS_DIR, "dictionaries", f"dictionary_{docs_type}.dict")
    )
    inputs["corpus"] = MmCorpus(
        os.path.join(INPUTS_DIR, "corpora", f"corpus_{corpus_type}_{docs_type}.mm")
    )
    with open(os.path.join(INPUTS_DIR, "docs", f"docs_{docs_type}.pkl"), "rb") as handle:
        inputs["docs"] = pickle.load(handle)
    inputs["corpus_type"] = corpus_type
    inputs["docs_type"] = docs_type
    return inputs
