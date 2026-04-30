from pymongo import MongoClient

MONGO_URL = "mongodb://localhost:27017"

client = MongoClient(MONGO_URL)

db = client["ai_business_copilot"]

users_collection = db["users"]
uploads_collection = db["uploads"]
chats_collection = db["chats"]
