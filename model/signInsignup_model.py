from pymongo import MongoClient
from datetime import datetime
import hashlib

# Initialize MongoDB connection
client = MongoClient("mongodb+srv://akashh2151:aOSefZ94SgQEkzmg@cluster0.25xmos0.mongodb.net/?retryWrites=true&w=majority")

# Select the "emc_project" database
db = client["emc_project"]

# Select the "signup" collection within the "emc_project" database
collection = db["signup"]

# class AuthModel:
#     def login_user(self, email, password):
#         try:
#             # Find the user by email
#             user = collection.find_one({"email": email})

#             # Check if the user exists
#             if user:
#                 # Hash the provided password using the same method as during registration
#                 provided_password = password.encode('utf-8')  # Convert to bytes
#                 hashed_provided_password = hashlib.sha256(provided_password).hexdigest()

#                 # Compare the hashed provided password with the stored hashed password
#                 if hashed_provided_password == user["password"]:
#                     return user

#             return None
#         except Exception as e:
#             # Handle the exception, log the error, and return an error response
#             print(f"Error in login_user: {str(e)}")
#             return None

class SignupModel:
    def find_user_by_email(self, email):
        try:
            return collection.find_one({"email": email})
        except Exception as e:
            # Handle the exception, log the error, and return an error response
            print(f"Error in find_user_by_email: {str(e)}")
            return None

    def register_user(self, auth_data):
        try:
            # Check if the email already exists
            existing_user = self.find_user_by_email(auth_data["email"])
            if existing_user:
                return {'error': 'Email already registered'}

            # Hash the password using SHA-256
            password = auth_data["password"].encode('utf-8')  # Convert to bytes
            hashed_password = hashlib.sha256(password).hexdigest()

            # Add registrationDate field with the current date and time
            auth_data["registrationDate"] = datetime.utcnow()

            # Create user document with additional fields
            user = {
                "firstName": auth_data["firstName"],
                "lastName": auth_data["lastName"],
                "email": auth_data["email"],
                "password": hashed_password,  # Store the hashed password
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
        except Exception as e:
            # Handle the exception, log the error, and return an error response
            print(f"Error in register_user: {str(e)}")
            return {'error': str(e)}
