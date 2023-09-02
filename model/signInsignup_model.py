# Initialize MongoDB connection
# import datetime
from pymongo import MongoClient
from werkzeug.security import check_password_hash,generate_password_hash
from datetime import datetime




client = MongoClient("mongodb://localhost:27017/")
db = client["emc_project"]
collection = db["signup"]


class AuthModel:
    def login_user(self, email, password):
        # Find the user by email
        user = collection.find_one({"email": email})

        # Check if the user exists and the provided password matches
        if user and check_password_hash(user["password"], password):
            return user
        else:
            return None




# Import statements...

class SignupModel:
    
    def find_user_by_email(self, email):
        return collection.find_one({"email": email})

    def register_user(self, auth_data):
        # Check if the email already exists
        existing_user = self.find_user_by_email(auth_data["email"])
        if existing_user:
            return {'error': 'Email already registered'}
    
    def register_user(self, auth_data):
        # Check if the email already exists
        if collection.find_one({"auth.email": auth_data["email"]}):
            return {'error': 'Email already registered'}

        # Hash the password
        hashed_password = generate_password_hash(auth_data["password"], method='scrypt')

        # Add registrationDate field with the current date and time
        auth_data["registrationDate"] = datetime.utcnow()

        # Create user document with additional fields
        user = {
            "firstName": auth_data["firstName"],
            "lastName": auth_data["lastName"],
            "email": auth_data["email"],
            "password": hashed_password,
            "userName": auth_data["userName"],
            "role": auth_data["role"],
            "company": auth_data["company"],
            "businessCategory": auth_data["businessCategory"],
            "bundle": auth_data["bundle"],
            "emailverified": auth_data.get("emailverified", False),
            "locale": auth_data.get("locale", "en-US"),
            "picture": auth_data.get("picture", ""),
            "expirydate": auth_data.get("expirydate"),
            "registrationDate": auth_data["registrationDate"],  # Add registrationDate here
        }

        # Insert user document into the database
        result = collection.insert_one(user)

        # Convert the ObjectId to a string
        user_id = str(result.inserted_id)

        # Return the user data including the generated ObjectId as a string
        user['_id'] = user_id
        return user
