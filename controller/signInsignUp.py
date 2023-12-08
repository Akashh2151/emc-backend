import hashlib
import datetime
import re
import uuid
from bson import ObjectId
from flask import Blueprint, current_app, request, jsonify
from flask_jwt_extended import jwt_required
import jwt
from model.signInsignup_model import  User
from configurations.configuration import shop_data,resto_data
from security.security import email_regex,password_regex



signUp_bp = Blueprint('signUp', __name__)
# Step 1: Register user with basic information
@signUp_bp.route('/register/step1', methods=['POST'])
def register_step1():
    try:
        data = request.json
        userName = data.get('userName')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role')
        
        userpassword=hashlib.sha256(password.encode()).hexdigest()

 
        # Check if the email is already registered
        if User.objects(email=email).first():
            response = {"Body": None, "status": "error", "statusCode": 400, "message": 'Email is already registered'}
            return jsonify(response), 400
        
            
        if not userName or not email or not password or not role:
            response = {"Body": None, "status": "error", "statusCode": 400, "message": 'userName, email, password, and role are required'}
            return jsonify(response), 400
        
        # Define your password requirements
        if not re.match(password_regex, password):
            response = {'Body': None, 'status': 'error', 'statusCode': 422, 'message': 'Password requirements not met'}
            return jsonify(response)
        
        # Define your email requirements
        if not re.match(email_regex,email):
                response = {'Body': None, 'status': 'error', 'statusCode': 422, 'message': 'Email requirement not met'}
                return jsonify(response)
        
        user = User(
            userName=userName,
            email=email,
            password=userpassword,
            role=role,
        )

        # Save the user to the database
        user.save()

        # Retrieve the user ID after saving to the database and convert to string
        user_id = str(user.id)      

        # Include user ID in the response
        response = {"Body": {"user_id": user_id}, "status": "success", "statusCode": 200, "message": 'Step 1 successful'}
        return jsonify(response), 200

    except Exception as e:
        response = {"Body": None, "status": "error", "statusCode": 500, "message": str(e)}
        return jsonify(response), 500




@signUp_bp.route('/register/step2', methods=['POST'])
def register_step2():
    try:
        data = request.json
        name = data.get('name')
        mobileNumber = data.get('mobileNumber')
        businessName = data.get('businessName')
        businessType = data.get('businessType')

        if not name or not mobileNumber or not businessName or not businessType:
            response = {"Body": None, "status": "error", "statusCode": 400, "message": 'userName, name, mobile number, business name, and business type are required'}
            return jsonify(response), 400

        # Get the user ID from the headers
        user_id_from_header = request.headers.get('id')

        if not user_id_from_header:
            response = {"Body": None, "status": "error", "statusCode": 400, "message": 'User ID is required in the header'}
            return jsonify(response), 400

        # Convert user ID to ObjectId
        user_id_object = ObjectId(user_id_from_header)

        # Get the user from the database
        user = User.objects(id=user_id_object).first()

        if not user:
            response = {"Body": None, "status": "error", "statusCode": 404, "message": 'User not found'}
            return jsonify(response), 404

        # Update the user with additional information
        user.name = name
        user.mobileNumber = mobileNumber
        user.businessName = businessName
        user.businessType = businessType
      
        

        # Perform additional validation if needed
        if businessType == "resto" or businessType == "shop":
            # Remove existing bundles if present
            user.shopBundle = None
            user.restoBundle = None
            if businessType == "shop":
                user.shopBundle = shop_data
                response=jwt.encode({'bundale':shop_data},current_app.config['SECRET_KEY'],algorithm='HS256')
            elif businessType == "resto":
                user.restoBundle = resto_data
                response=jwt.encode({'bundale':resto_data},current_app.config['SECRET_KEY'],algorithm='HS256')
        # Save the updated user to the database
        user.save()
        
        response = {"Body": response, "status": "success", "statusCode": 200, "message": 'Step 2 successful'}
        return jsonify(response), 200

    except Exception as e:
        response = {"Body": None, "status": "error", "statusCode": 500, "message": str(e)}
        return jsonify(response), 500

 


login_bp = Blueprint('login', __name__)
@login_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        businessType = data.get('businessType')

        # Validate the presence of 'email', 'password', and 'businessType'
        if email is None or password is None or businessType is None:
            return jsonify({'error': 'Email, password, and businessType are required', 'status_code': 400}), 400

        # Find the user by email
        user = User.objects(email=email).first()

        if user:
            # Check if the provided businessType matches the user's businessType
            if user.businessType == businessType:
                provided_password_hash = hashlib.sha256(password.encode()).hexdigest()
                # userpassword=hashlib.sha256(password.encode()).hexdigest()
                print(user.password)
                if provided_password_hash == user.password:
                    payload = {
                        'user_id': str(user.id),
                        'sub': '1',
                        'jti': str(uuid.uuid4()),
                        'identity': user.email,
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=50),
                        'role': user.role,
                        'type': 'access',
                        'fresh': True
                    }
                    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256') 

                    # Include user businessType in the response body based on its value
                    if user.businessType == 'resto':
                        encoded_resto_data = jwt.encode({'bundle':resto_data}, current_app.config['SECRET_KEY'], algorithm='HS256')
                        return jsonify({'Body': encoded_resto_data,
                                        'message': 'Login successful', 'access_token': token, 'status_code': 200})
                    elif user.businessType == 'shop':
                        encoded_shop_data = jwt.encode({'bundle': shop_data}, current_app.config['SECRET_KEY'], algorithm='HS256')
                        return jsonify({'Body': encoded_shop_data,
                                        'message': 'Login successful', 'access_token': token, 'status_code': 200})
                else:
                    return jsonify({'error':'password is worgn'}), 401
            else:
                return jsonify({'error': 'Invalid businessType'}), 401

        return jsonify({'error': 'Invalid email or password'}), 401

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
 