import hashlib
import datetime
import json
import re
import uuid
from bson import ObjectId
from flask import Blueprint, current_app, request, jsonify
from flask_jwt_extended import jwt_required
import jwt
from model.signInsignup_model import  User
from configurations.configuration import resto_data,shop_data
from security.allSecurity import email_regex,password_regex,phone_number
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
signUp_bp = Blueprint('signUp', __name__)



# unsycronaycied 
# mulitipale worki doning in ne time
# sycronazed
# doing one wrok in one time 
# compiler working this all things

# login return in body bussiness type






# 1st
#  name 
#  maobaile 
#  email 
#  password 
# 2sd
# b name
# b mob
# b email
# b addres
# b type


# (
# need this unique
# 1st
# user email 
# user mobaile


# 2sd
# b email 
# b mobail
# return this all things in ragister response - user
# name  
# )


@signUp_bp.route('/v1/register', methods=['POST'])
def register_step1():
    try:
        data = request.json
        name = data.get('name')
        mobile = data.get('mobile')
        email = data.get('email')
        password = data.get('password')
        businessName = data.get('businessName')
        businessMobile = data.get('businessMobile')
        businessEmail = data.get('businessEmail')
        businessAddress = data.get('businessAddress')
        businessType = data.get('businessType')

        # Check if the email or mobile is already registered
        if User.objects(email=email).first() or User.objects(mobile=mobile).first():
            response = {"body": None, "status": "error", "statuscode": 403, "message": 'Email or mobile is already registered'}
            return jsonify(response),200
        
                # Check if the business email is already registered
        if User.objects(businessEmail=businessEmail).first():
            response = {"body": None, "status": "error", "statuscode": 400, "message": 'Business email is already registered'}
            return jsonify(response), 200

        # Check if the business email or business mobile is already registered
        if User.objects(businessMobile=businessMobile).first():
            response = {"body": None, "status": "error", "statuscode": 400, "message": 'Business mobile is already registered'}
            return jsonify(response), 200

        # Validate required fields
        required_fields = [name, email, password, mobile, businessName, businessMobile, businessType, businessEmail, businessAddress]
        if not all(required_fields):
            response = {"body": None, "status": "error", "statuscode": 400, "message": 'All required fields must be provided'}
            return jsonify(response), 200
        
        # Validate password and email format
        if not re.match(password_regex, password):
            response = {'body': None, 'status': 'error', 'statuscode': 422, 'message': 'Password must be at least 8 to 16 characters long'}
            return jsonify(response),200

        if not re.match(email_regex, email):
            response = {'body': None, 'status': 'error', 'statuscode': 422, 'message': 'Email requirement not met'}
            return jsonify(response),200
        
        if not re.match(phone_number,mobile):
            response = {'body': None, 'status': 'error', 'statuscode': 422, 'message': 'Mobile number must be exactly 10 digits long and should only contain numeric characters.'}
            return jsonify(response),200
       
        if not re.match(phone_number,businessMobile):
            response = {'body': None, 'status': 'error', 'statuscode': 422, 'message': 'Mobile number must be exactly 10 digits long and should only contain numeric characters.'}
            return jsonify(response),200
                    # password mast be atalet 8 to charater
        print("Business Name:", businessType)
        if not re.match(r'^(resto|shop)', businessType):
            response = {'body': None, 'status': 'error', 'statuscode': 422, 'message': 'businessType requirement not met'}
            return jsonify(response),200
            
        # Hash the password
        userpassword = hashlib.sha256(password.encode()).hexdigest()

        # Create the User object
        user = User(
            name=name,
            mobile=mobile,
            email=email,
            password=userpassword,
            businessName=businessName,
            businessMobile=businessMobile,
            businessEmail=businessEmail,
            businessAddress=businessAddress,
            businessType=businessType
        )

        # Perform additional validation and bundle setup if needed
        if businessType == "resto" or businessType == "shop":
            # Remove existing bundles if present
            user.shopBundle = []
            user.bundle = []

            if businessType == "shop":
                user.shopBundle = shop_data
                # response = jwt.encode({'bundle': shop_data}, current_app.config['SECRET_KEY'], algorithm='HS256')
            elif businessType == "resto":
                user.bundle = [resto_data]  # Wrap resto_data in a list
                # response = jwt.encode({'bundle': resto_data}, current_app.config['SECRET_KEY'], algorithm='HS256')

        # Save the user to the database
        user.save()

        response = {"body": {}, "status": "success", "statusCode": 200, "message": 'Registration successfully'}
        return jsonify(response), 200

    except Exception as e:
        response = {"body": None, "status": "error", "statusCode": 500, "message": str(e)}
        return jsonify(response), 500


# ____________________________________________________________________________________________________________
# all working 
# @signUp_bp.route('/register/step1', methods=['POST'])
# def register_step1():
#     try:
#         data = request.json
#         userName = data.get('userName')
#         email = data.get('email')
#         password = data.get('password')
#         role = data.get('role')
        
#         userpassword=hashlib.sha256(password.encode()).hexdigest()

 
#         # Check if the email is already registered
#         if User.objects(email=email).first():
#             response = {"Body": None, "status": "error", "statusCode": 400, "message": 'Email is already registered'}
#             return jsonify(response), 400
        
            
#         if not userName or not email or not password or not role:
#             response = {"Body": None, "status": "error", "statusCode": 400, "message": 'userName, email, password, and role are required'}
#             return jsonify(response), 400
        
#         # Define your password requirements
#         if not re.match(password_regex, password):
#             response = {'Body': None, 'status': 'error', 'statusCode': 422, 'message': 'Password requirements not met'}
#             return jsonify(response)
        
#         # Define your email requirements
#         if not re.match(email_regex,email):
#                 response = {'Body': None, 'status': 'error', 'statusCode': 422, 'message': 'Email requirement not met'}
#                 return jsonify(response)
        
#         user = User(
#             userName=userName,
#             email=email,
#             password=userpassword,
#             role=role,
#         )

#         # Save the user to the database
#         user.save()

#         # Retrieve the user ID after saving to the database and convert to string
#         user_id = str(user.id)      

#         # Include user ID in the response
#         response = {"Body": {"user_id": user_id}, "status": "success", "statusCode": 200, "message": 'Step 1 successful'}
#         return jsonify(response), 200

#     except Exception as e:
#         response = {"Body": None, "status": "error", "statusCode": 500, "message": str(e)}
#         return jsonify(response), 500


# @signUp_bp.route('/register/step2', methods=['POST'])
# def register_step2():
#     try:
#         data = request.json
#         name = data.get('name')
#         mobileNumber = data.get('mobileNumber')
#         businessName = data.get('businessName')
#         businessType = data.get('businessType')

#         if not name or not mobileNumber or not businessName or not businessType:
#             response = {"Body": None, "status": "error", "statusCode": 400, "message": 'userName, name, mobile number, business name, and business type are required'}
#             return jsonify(response), 400

#         # Get the user ID from the headers
#         user_id_from_header = request.headers.get('id')

#         if not user_id_from_header:
#             response = {"Body": None, "status": "error", "statusCode": 400, "message": 'User ID is required in the header'}
#             return jsonify(response), 400

#         # Convert user ID to ObjectId
#         user_id_object = ObjectId(user_id_from_header)

#         # Get the user from the database
#         user = User.objects(id=user_id_object).first()

#         if not user:
#             response = {"Body": None, "status": "error", "statusCode": 404, "message": 'User not found'}
#             return jsonify(response), 404

#         # Update the user with additional information
#         user.name = name
#         user.mobileNumber = mobileNumber
#         user.businessName = businessName
#         user.businessType = businessType
      
        

#         # Perform additional validation if needed
#         if businessType == "resto" or businessType == "shop":
#             # Remove existing bundles if present
#             # Remove existing bundles if present
#             user.shopBundle = []
#             user.Bundle = []

#             if businessType == "shop":
#                 user.shopBundle = shop_data
#                 response = jwt.encode({'bundle': shop_data}, current_app.config['SECRET_KEY'], algorithm='HS256')
#             elif businessType == "resto":
#                 user.Bundle = [resto_data]  # Wrap resto_data in a list
#                 response = jwt.encode({'bundle': resto_data}, current_app.config['SECRET_KEY'], algorithm='HS256')
#         # Save the updated user to the database
#         user.save()
        
#         response = {"Body": response, "status": "success", "statusCode": 200, "message": 'Step 2 successful'}
#         return jsonify(response), 200

#     except Exception as e:
#         response = {"Body": None, "status": "error", "statusCode": 500, "message": str(e)}
#         return jsonify(response), 500
# ___________________________________________________________________________________________________________________
 



# @login_bp.route('/login', methods=['POST'])
# def login():
#     try:
#         data = request.json
#         email = data.get('email')
#         password = data.get('password')
#         businessType = data.get('businessType')

#         # Validate the presence of 'email', 'password', and 'businessType'
#         if email is None or password is None or businessType is None:
#             return jsonify({'error': 'Email, password, and businessType are required', 'status_code': 400}), 400

#         # Find the user by email
#         user = User.objects(email=email).first()

#         if user:
#             # Check if the provided businessType matches the user's businessType
#             if user.businessType == businessType:
#                 provided_password_hash = hashlib.sha256(password.encode()).hexdigest()
#                 # userpassword=hashlib.sha256(password.encode()).hexdigest()
#                 print(user.password)
#                 if provided_password_hash == user.password:
#                     payload = {
#                         'user_id': str(user.id),
#                         'sub': '1',
#                         'jti': str(uuid.uuid4()),
#                         'identity': user.email,
#                         'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=50),
#                         'role': user.role,
#                         'type': 'access',
#                         'fresh': True
#                     }
#                     token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256') 

#                     # Include user businessType in the response body based on its value
#                     if user.businessType == 'resto':
#                         encoded_resto_data = jwt.encode({'bundle':resto_data}, current_app.config['SECRET_KEY'], algorithm='HS256')
#                         return jsonify({'Body': encoded_resto_data,
#                                         'message': 'Login successful', 'access_token': token, 'status_code': 200})
#                     elif user.businessType == 'shop':
#                         encoded_shop_data = jwt.encode({'bundle': shop_data}, current_app.config['SECRET_KEY'], algorithm='HS256')
#                         return jsonify({'Body': encoded_shop_data,
#                                         'message': 'Login successful', 'access_token': token, 'status_code': 200})
#                 else:
#                     return jsonify({'error':'password is Wrong'}), 401
#             else:
#                 return jsonify({'error': 'Invalid businessType'}), 401

#         return jsonify({'error': 'Invalid email or password'}), 401

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500





# login route
login_bp = Blueprint('login', __name__)
@login_bp.route('/v1/login', methods=['POST'])
def login():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')

        # Validate the presence of 'email' and 'password'
        if email is None or password is None:
            return jsonify({'body': {},"status": "error",'message': 'Email and password are required', 'statusCode': 401}), 200

        # Find the user by email
        user = User.objects(email=email).first()

        if user:
            provided_password_hash = hashlib.sha256(password.encode()).hexdigest()

            if provided_password_hash == user.password:
                payload = {
                    'user_id': str(user.id),
                    'sub': '1',
                    'jti': str(uuid.uuid4()),
                    'identity': user.email,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=50),
                    'type': 'access',
                    'fresh': True
                }
                token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
                

                # Check if a bundle is stored for the user
                if user.bundle:
                    encoded_bundle_data = jwt.encode({'bundle': user.bundle}, current_app.config['SECRET_KEY'], algorithm='HS256')
                                        # Prepare the response with the updated user details
                  
       
                    updated_user_detail = str(user.name)
                                        # Include other relevant user details here
                                    
                    updated_user_details = {
                        "bundle": encoded_bundle_data,
                         "name": updated_user_detail
                        # "updated_master_details": updated_master,
                        # "userName":userName
                         
                        # Include other relevant user details here
                    }
              
              
                    return jsonify({'body': updated_user_details,
                                    'message': 'Login successfully',"status": "success", 'access_token': token,"statusCode": 200,}),200
                else:
                    return jsonify({'body':{},'message': 'Login successfully', 'access_token': token, 'statusCode': 200}),200

            else:
                return jsonify({'body':{},'message': 'Incorrect password','statusCode': 401,"status": "error"}), 200

        return jsonify({'body': {},'message': 'Invalid email or password',"status": "error", 'statusCode': 401,}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500



    
    
@login_bp.route('/protected', methods=['GET'])
@jwt_required
def role_login():
    try:
        token = request.headers.get('Authorization').split()[1]
        decoded_token = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])

        user_role = decoded_token.get('role')

        if user_role == 'admin':
            return jsonify({'status_code': 200, 'message': 'success', 'role': 'admin'}), 200
        elif user_role == 'user':
            return jsonify({'status_code': 200, 'message': 'success', 'role': 'user'}), 200
        else:
            return jsonify({'status_code': 403, 'message': 'Permission denied'}), 403
    except UnicodeDecodeError as e:
        # Handle the specific error when the token payload cannot be decoded
        return jsonify({'status_code': 400, 'error': 'Invalid token payload'}), 400
    except Exception as e:
        return jsonify({'status_code': 500, 'error': str(e)}), 500
 