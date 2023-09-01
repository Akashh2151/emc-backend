from flaskapp import app
from flask import Flask, request, jsonify
from pymongo import MongoClient
from werkzeug.security import check_password_hash,generate_password_hash
import datetime

# Initialize MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["emc_project"]
collection = db["signup"]

class AuthModel:
    def login_user(self, email, password):
        user = collection.find_one({"email": email})
        
        if user and check_password_hash(user["password"], password):
            return user
        else:
            return None





class SignupModel:
    def register_user(self, user_data):
        # Check if the email already exists
        if collection.find_one({"email": user_data["email"]}):
            return {'error': 'Email already registered'}

        # Hash the password
        hashed_password = generate_password_hash(user_data["password"], method='sha256')

        # Create user document with new fields
        user = {
            "firstName": user_data["firstName"],
            "lastName": user_data["lastName"],
            "email": user_data["email"],
            "password": hashed_password,
            "userName": user_data["userName"],
            "role": user_data["role"],
            "company": user_data["company"],
            "businessCategory": user_data["businessCategory"],
            "bundle": user_data["bundle"],
            "emailverified": user_data.get("emailverified", False),  # Default to False
            "locale": user_data.get("locale", ""),  # Default to an empty string
            "picture": user_data.get("picture", ""),  # Default to an empty string
            "expirydate": user_data.get("expirydate", None),  # Default to None
            "registrationDate": datetime.datetime.utcnow()
        }

        # Insert user document into the database
        collection.insert_one(user)
        return {'message': 'Registration successful'}

