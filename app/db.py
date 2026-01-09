from pymongo import MongoClient
from app.settings import config

client = MongoClient(config.MONGO_URI)
db = client[config.DB_NAME]

# Collections
students = db["students"]
lab_knowledge = db["lab_knowledge"]
interactions = db["interactions"]