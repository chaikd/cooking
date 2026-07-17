import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGODB_URI = os.getenv('MONGODB_URI')
DB_NAME = os.getenv('DB_NAME')
mongo_client = MongoClient(MONGODB_URI)
checkpoint_db = mongo_client[DB_NAME]

# 聊天记录
SESSIONS = checkpoint_db['sessions']
