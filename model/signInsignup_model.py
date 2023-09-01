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
        user = collection.find_one({"auth.email": email})
        
        if user and check_password_hash(user["auth"]["password"], password):
            return user
        else:
            return None



class SignupModel:
    def register_user(self, auth_data):
        # Check if the email already exists
        if collection.find_one({"auth.email": auth_data["email"]}):
            return {'error': 'Email already registered'}

        # Hash the password
        hashed_password = generate_password_hash(auth_data["password"], method='sha256')

        # Create user document
        user = {
            "auth": {
                "firstName": auth_data["firstName"],
                "lastName": auth_data["lastName"],
                "email": auth_data["email"],
                "password": hashed_password,
                "userName": auth_data["userName"],
                "role": auth_data["role"],
                "company": auth_data["company"],
                "businessCategory": auth_data["businessCategory"],
                "bundle": auth_data["bundle"]
            },
            "registrationDate": datetime.datetime.utcnow()
        }

        # Insert user document into the database
        collection.insert_one(user)
        return {'message': 'Registration successful'}

