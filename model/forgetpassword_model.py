import pymongo
from pymongo import MongoClient
from flask import current_app

client = MongoClient("mongodb://localhost:27017/")
db = client["emc_project"]
users_collection = db["signup"]

class ForgotPasswordModel:
    def get_user_by_email(self, email):
        return users_collection.find_one({"email": email})


    def update_user(self, user_data):
        users_collection.update_one(
            {"email": user_data["email"]},
            {"$set": {"password": user_data["password"]}}
        )
