"""This module contains functions for using LDA topic modeling."""

import os
import datetime
import pandas as pd
import pickle
import json
from gensim.models import Phrases
from gensim.corpora import Dictionary
from gensim.models import TfidfModel, LdaModel
from gensim.models.coherencemodel import CoherenceModel
from gensim.models.callbacks import PerplexityMetric, ConvergenceMetric, CoherenceMetric
from gensim.corpora.mmcorpus import MmCorpus
import spacy

import logging
from usrightmedia.shared.loggers import get_logger

# python -m spacy download en_core_web_lg
nlp = spacy.load("en_core_web_lg")

INPUTS_DIR = os.path.join(
    "..", "..", "data", "02-intermediate", "08-topic-models", "01-inputs"
)
MODELS_DIR = os.path.join(
    "..", "..", "data", "02-intermediate", "08-topic-models", "02-models"
)

from usrightmedia.shared.loggers import get_logger

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
    """
    citation: based off of https://github.com/RaRe-Technologies/gensim/blob/develop/docs/notebooks/atmodel_tutorial.ipynb
    """
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
        
        # pre-processing can result in some docs having no tokens (i.e., length is 0)
        if len(doc) > 0:
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
    """Load inputs for computing topic model.
    
    Args:
        corpus_type (str): "count", "tfidf"
        docs_type (str): "leads", "titles", "texts"
        
    Returns:
        inputs (dict): keys - "dictionary", "corpus", "docs", "corpus_type", "docs_type"
    
    """
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


def compute_topic_models(corpus_type, docs_type, min_topics, max_topics, step_topics):
    """Compute topic model by corpus type and document type.
    
    Args:
        corpus_type (str): "count", "tfidf"
        docs_type (str): "leads", "titles", "texts"    
        min_topics (int): minimum number of topics
        max_topics (int): maximum number of topics
        step_topics (int): number of topics to increment by between each model
    
    Returns:
        None
        
    Output:
        One subdirectory of files per model (f'{corpus_type}_{docs_type}_{topics_n}')
        
    References:
        https://www.machinelearningplus.com/nlp/topic-modeling-gensim-python/#17howtofindtheoptimalnumberoftopicsforlda
        https://radimrehurek.com/gensim/auto_examples/tutorials/run_lda.html
        https://markroxor.github.io/gensim/static/notebooks/lda_training_tips.html
        https://www.meganstodel.com/posts/callbacks/
        https://miningthedetails.com/blog/python/lda/GensimLDA/
        https://groups.google.com/g/gensim/c/ojySenxQHi4
    """
   
    
    # 1. load inputs
    inputs = load_inputs(corpus_type, docs_type, INPUTS_DIR)
    dictionary = inputs['dictionary']
    corpus = inputs['corpus']
    docs = inputs["docs"]
    
    # 2. set LDA model arguments
    distributed=False # default
    chunksize=100000
        
    # check logs: passes and iterations should be adjusted if convergence is low
    # https://groups.google.com/g/gensim/c/ojySenxQHi4/m/jjX1RbbHERgJ
    # `passes` is the number of training passes through the corpus.
    # For example, if the training corpus has 50,000 documents, chunksize is 10,000, passes is 2, then online training is done in 10 updates
    passes = 5
    
    # https://groups.google.com/g/gensim/c/ojySenxQHi4/m/Ctny4H5lZXAJ
    # By default, update_every=1, so that the update happens after each batch of `chunksize` documents.
    update_every = 1
        
    # Computational Analysis of Communication (p. 275 in book draft)
    # we would generally recommend a relatively low and asymmetric alpha, and in fact Gensim by default uses an algorithm to find an alpha that corresponds to this recommendation.
    # http://dirichlet.net/pdf/wallach09rethinking.pdf
    # "Since the priors we advocate (an asymmetric Dirichlet over the document–topic distributions and a
    # symmetric Dirichlet over the topic–word distributions) have significant modeling benefits and can
    # be implemented using highly efficient algorithms, we recommend them as a new standard for LDA."
    alpha="asymmetric"
    eta="symmetric"
    
    decay = 0.5 # default
    offset = 1.0 # default
    
    # Log perplexity is estimated every that many updates. Setting this to one slows down training by ~2x.
    eval_every = 10

    iterations = 50 # default
    gamma_threshold = 0.001 # default
    minimum_probability = 0.01 # default
    
    # reproducibility
    random_state=42
    
    ns_conf = None # default
    minimum_phi_value = 0.01 # default
    per_word_topics = False # default
    
    # 3. compute models
    for n_topics in range(min_topics, max_topics, step_topics):
        
        model_name = f'lda_corpus_{corpus_type}_docs_{docs_type}_topics_{n_topics}'
       
        # Set up the callbacks loggers
        LOGGER = get_logger(filename = f'{model_name}', logger_type='main')
        convergence_logger = ConvergenceMetric(logger='shell')
        coherence_cv_logger = CoherenceMetric(corpus=corpus, logger='shell', coherence = 'c_v', texts = docs)
        perplexity_logger = PerplexityMetric(corpus=corpus, logger='shell')
        
        LOGGER.debug(f'Start of LDA model: {model_name}')
        LOGGER.debug(f'n_topics: {n_topics}')
        LOGGER.debug(f'distributed: {distributed}')
        LOGGER.debug(f'chunksize: {chunksize}')
        LOGGER.debug(f'passes: {passes}')
        LOGGER.debug(f'update_every: {update_every}')
        LOGGER.debug(f'alpha: {alpha}')
        LOGGER.debug(f'eta: {eta}')
        LOGGER.debug(f'decay: {decay}')
        LOGGER.debug(f'offset: {offset}')
        LOGGER.debug(f'eval_every: {eval_every}')
        LOGGER.debug(f'iterations: {iterations}')
        LOGGER.debug(f'gamma_threshold: {gamma_threshold}')
        LOGGER.debug(f'minimum_probability: {minimum_probability}')
        LOGGER.debug(f'random_state: {random_state}')
        LOGGER.debug(f'ns_conf: {ns_conf}')
        LOGGER.debug(f'minimum_phi_value: {minimum_phi_value}')
        LOGGER.debug(f'per_word_topics: {per_word_topics}')        

        # Create model
        model = LdaModel(corpus=corpus,
                         num_topics=n_topics,
                         id2word=dictionary,
                         distributed=distributed,
                         chunksize=chunksize,
                         passes=passes,
                         update_every=update_every,
                         alpha=alpha,
                         eta=eta,
                         decay=decay,
                         offset=offset,
                         eval_every=eval_every,
                         iterations=iterations,
                         gamma_threshold=gamma_threshold,
                         random_state=random_state,
                         ns_conf=ns_conf,
                         minimum_phi_value=minimum_phi_value,
                         per_word_topics=per_word_topics,
                         callbacks=[convergence_logger, coherence_cv_logger, perplexity_logger])


        # 4. Save model
        if not os.path.exists(os.path.join(MODELS_DIR, f"{model_name}/")):
            os.makedirs(os.path.join(MODELS_DIR, f"{model_name}/"))

        model.save(os.path.join(MODELS_DIR, model_name, f"{model_name}.model"))
        LOGGER.debug(f'End of LDA model: {model_name}')
        
        LOGGER.debug(f'Start of coherence model: {model_name}')
        coherence_c_v = CoherenceModel(model=model, texts=docs, dictionary=dictionary, coherence='c_v')
        with open(os.path.join(MODELS_DIR, model_name, f"{model_name}_coherence_c_v.pkl"), "wb") as fn:
            pickle.dump(coherence_c_v, fn)
            
        LOGGER.debug(f'End of coherence model: {model_name}')
        
        
def compute_coherence_values(corpus_type, docs_type, min_topics, max_topics, step_topics):
    """Compute coherence values for models.
    
    Args:
        corpus_type (str): "count", "tfidf"
        docs_type (str): "leads", "titles", "texts"    
        min_topics (int): minimum number of topics
        max_topics (int): maximum number of topics
        step_topics (int): number of topics to increment by between each model
    
    Returns:
        None (writes to jsonl file)
        
    """
    
    try:
        for n_topics in range(min_topics, max_topics, step_topics):
            model_name = f"lda_corpus_{corpus_type}_docs_{docs_type}_topics_{n_topics}"
            LOGGER = get_logger(filename = f'{model_name}_coherence_c_v', logger_type='main')
            
            json_file = os.path.join(MODELS_DIR, "coherence_c_v_summary", "coherence_c_v_summary.jsonl")
            coherence_dicts = []
            if json_file and os.path.exists(json_file):
                with open(file=json_file, mode="r", encoding="utf-8") as file:
                    for line in file:
                        coherence_dicts.append(json.loads(line))
                        
            # only compute coherence value for a model if it doesn't exist in the json file
            if len([d for d in coherence_dicts if d['model_name']==model_name]) == 0:
                LOGGER.info(f"{model_name} with {n_topics} topics does not exist in the json file")
                # create dict to hold model info
                d = {}
                d["model_name"] = model_name
                d["corpus_type"] = corpus_type
                d["docs_type"] = docs_type
                d["model_group"] = d["docs_type"] + "_" + d["corpus_type"]
                d["n_topics"] = n_topics

                # Compute coherence using c_v
                with open(os.path.join(MODELS_DIR, model_name, f"{model_name}_coherence_c_v.pkl"), "rb") as handle:
                    coherence_c_v = pickle.load(handle)

                LOGGER.info(f"Starting coherence calculation for {model_name} with {n_topics} topics")
                coherence_score_c_v = coherence_c_v.get_coherence()
                d["coherence_score_c_v"] = coherence_score_c_v
                LOGGER.info(f"Completed coherence calculation for {model_name} with {n_topics} topics: coherence_score_c_v = {coherence_score_c_v}")

                d_json = json.dumps(d)

                with open(file=os.path.join(MODELS_DIR, "coherence_c_v_summary", "coherence_c_v_summary.jsonl"), mode="a", encoding="utf-8") as f_out:
                    f_out.write(d_json + "\n")
                LOGGER.info(f"Wrote coherence calculation for {model_name} with {n_topics} topics to {os.path.join(MODELS_DIR, 'coherence_c_v_summary', 'coherence_c_v_summary.jsonl')}")
            
    except FileNotFoundError as e:
        LOGGER.info(f"Combo ({docs_type}, {corpus_type}) with n_topics {n_topics} has not been computed yet.")
                
        
# adapted from https://www.machinelearningplus.com/nlp/topic-modeling-gensim-python/
def extract_top_topic_per_doc(model, corpus, docs):
    """For each document, extract the topic with the highest probability.
    
    Args:
        model (obj): gensim LDA model
        corpus (obj): gensim corpus
        docs (list): list of texts
    
    Returns:
        df_topics (dataframe): dataframe where each row is a document.
            - columns: 'top_topic', 'top_topic_pct', 'topic_tokens', 'doc_tokens'
       
    Reference: https://nlp.stanford.edu/events/illvi2014/papers/sievert-illvi2014.pdf
    - LDAvis: A method for visualizing and interpreting topics
    - Terms are sorted by pyLDAvis' method of relevance
  
    (p. 66) we define the relevance of a term w to a topic k given a weight parameter λ (where 0  λ  1) as:

    r(w, k | λ) = λlog(Φkw) + (1 - λ) log(Φkw/pw)

    Let Φkw/pw denote the probability of term w ∈ {1, ..., V} for topic k ∈ {1, ..., K}, where V denotes the number of terms in the vocabulary, and let pw denote the marginal probability of term w in the corpus.
    λ determines the weight given to the probability of term w under topic k relative to its lift (measuring both on the log scale).
    Setting λ = 1 results in the familiar ranking of terms in decreasing order of their topic-specific probability,
    and setting λ = 0 ranks terms solely by their lift.
    
    (p. 65): Taddy (2011) uses an intrinsic measure to rank terms within topics: a quantity called lift, defined as the ratio of a term’s probability within a topic to its marginal probability across the corpus.
    This generally decreases the rankings of globally frequent terms, which can be helpful.
    We find that it can be noisy, however, by giving high rankings to very rare terms that occur in only a single topic, for instance.
    While such terms may contain useful topical content, if they are very rare the topic may remain difficult to interpret.
    
    """
    
    model_name = f"lda_corpus_{corpus}_docs_{docs}_topics_{model.num_topics}"
    
    LOGGER = get_logger(filename = f'{model_name}_top_topic', logger_type='main')
    
    # Init output
    df_topics = pd.DataFrame()

    # Get main topic in each document
    for i, row in enumerate(model.get_document_topics(corpus)):
        if i % 10000 == 0:
            LOGGER.info(f"processing top topic for document {i}")
            
        row = sorted(row, key=lambda x: (x[1]), reverse=True)
        # Get the Dominant topic, Perc Contribution and Keywords for each document
        for j, (topic_num, prop_topic) in enumerate(row):
            if j == 0:  # => dominant topic
                wp = model.show_topic(topic_num)
                topic_keywords = ", ".join([word for word, prop in wp])
                df_topics = df_topics.append(pd.Series([int(topic_num), round(prop_topic,4), topic_keywords]), ignore_index=True)
            else:
                break

    # Add original text to the end of the output
    contents = pd.Series(docs)
    df_topics = pd.concat([df_topics, contents], axis=1)
    df_topics.columns = ['top_topic', 'top_topic_pct', 'topic_tokens', 'doc_tokens']
    
    with open(os.path.join(MODELS_DIR, model_name, f"{model_name}_top_topic.pkl"), "wb") as fn:
        pickle.dump(df_topics, fn)
            
    return df_topics