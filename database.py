from pymongo import MongoClient
from config import settings

client = MongoClient(settings.database_url)
database = client.get_database("Cluster0")
user_collection = database.get_collection("users")
museum_collection = database.get_collection("museums")
comment_collection = database.get_collection("comments")
rating_collection = database.get_collection("ratings")
ticket_collection = database.get_collection("tickets")
