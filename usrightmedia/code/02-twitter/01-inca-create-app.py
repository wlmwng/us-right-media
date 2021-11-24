# Purpose: create a Twitter app (API v2) in INCA to collect politicians' timelines.

# 1) clone the (modified) INCA repo into a directory
# git clone git@github.com:wlmwng/inca-dev.git

# 2) navigate to the directory
# e.g., cd ~/Documents/github/inca-dev

# activate your virtual environment

# 3) install INCA
# pip install -r requirements.txt
# pip install -e . (develop mode)

# 4) check that Elasticsearch is running
# service elasticsearch status

# 5) run this script in terminal
# e.g., python ~/Documents/github/us-right-media/usrightmedia/code/02-twitter/01-inca-create-app.py

# NOTES:
# to check Elasticsearch indices
# curl http://localhost:9200/_cat/indices?v

# INCA only allows 1 client app at a time.
# To start fresh with INCA, delete the Elasticsearch indices:
# curl -X DELETE "localhost:9200/inca?pretty"
# curl -X DELETE "localhost:9200/.credentials?pretty"
# curl -X DELETE "localhost:9200/.apps?pretty"

# IMPORTANT:
# INCA will fail to create tasks if Celery >= 4.x
# Elasticsearch == 6.8.1
# INCA relies on ES mapping types, which are deprecated in ES 7.x

from inca import Inca
from time import sleep

myinca = Inca()

# answer the prompts: 'usrightmedia', [your twitter ID], [your bearer token]
myinca.clients.twitter2_create_app()
myinca.clients.twitter2_create_credentials(appname="usrightmedia")

# check that the app was registered in INCA:
# wait a few seconds for Elasticsearch to update
sleep(5)
print(myinca.database.list_apps())
