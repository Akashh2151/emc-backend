 
# import hashlib
# from flask_jwt_extended import JWTManager
# from flask import current_app
# import jwt
# from model.signInsignup_model import User

# # Define your regular expressions and other security-related constants here
# email_regex = r'^\S+@\S+\.\S+$'
# password_regex = r'^.{8,}$'

# # Create a JWTManager instance
# jwt = JWTManager()

# # Security-related helper functions
# # def hash_password(password):
# #     return hashlib.sha256(password.encode()).hexdigest()

# def encode_token(payload):
#     return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')