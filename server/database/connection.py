from pymongo import MongoClient

from ..settings.database import MONGO_URL

client = MongoClient(MONGO_URL)
