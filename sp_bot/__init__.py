import logging
import os
import sys
import telegram.ext as tg
from sp_bot.config import Config

from pymongo import MongoClient

# enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)

LOGGER = logging.getLogger(__name__)

# import ENV variables
TOKEN = Config.API_KEY
CLIENT_ID = Config.SPOTIFY_CLIENT_ID
CLIENT_SECRET = Config.SPOTIFY_CLIENT_SECRET
OWNER = Config.OWNER_USERNAME

MONGO_USR = Config.MONGO_USR
MONGO_PASS = Config.MONGO_PASS
COL = Config.MONGO_COLL

TEMP_CHANNEL = Config.TEMP_CHANNEL

updater = tg.Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher

SESSION = MongoClient(
    f"mongodb://{MONGO_USR}:{MONGO_PASS}@{COL}-shard-00-00.ibx7n.mongodb.net:27017,{COL}-shard-00-01.ibx7n.mongodb.net:27017,{COL}-shard-00-02.ibx7n.mongodb.net:27017/{COL}?ssl=true&replicaSet=atlas-lnda18-shard-0&authSource=admin&retryWrites=true&w=majority")
