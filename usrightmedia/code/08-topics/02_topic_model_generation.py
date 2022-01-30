# Script for computing topic models
# docker exec -it --user root inca-wailam /bin/bash
# cd /home/jovyan/work/us-right-media/usrightmedia/code/08-topics
# tmux new -s lda_topic_models
# conda activate usrightmedia 
# python 02_topic_model_generation.py & 
# Detach from a tmux terminal: Ctrl-b + d
# tmux attach -t lda_topic_models

import itertools
import os

from usrightmedia.shared.topics_utils import *

docs_types = ["leads", "titles","texts"]
corpus_types = ["count", "tfidf"]

model_combos = list(itertools.product(docs_types, corpus_types))
# [('leads', 'count'),
#  ('leads', 'tfidf'),
#  ('titles', 'count'),
#  ('titles', 'tfidf'),
#  ('texts', 'count'),
#  ('texts', 'tfidf')]

for combo in model_combos:
    docs_type = combo[0]
    corpus_type = combo[1]
    compute_topic_models(corpus_type=corpus_type, docs_type=docs_type, min_topics=30, max_topics=55, step_topics=5)