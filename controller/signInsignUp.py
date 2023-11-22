import re
import hashlib
import datetime
import uuid
from flask import Blueprint, current_app, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
import jwt
from model.signInsignup_model import  User
# from model.signInsignup_model import Resto, Shop, UserData


email_regex = r'^\S+@\S+\.\S+$' 
password_regex = r'^.{8,}$'
 
signUp_bp = Blueprint('signUp', __name__)
@signUp_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        print("email:",email)
        print("password:",password)
        role = data.get('role')  # Get the role from the request
        
        # Check if the email is already registered
        existing_user = User.objects(email=email).first()
        if existing_user:
            response = { "Body": None,"status": "error","statusCode": 400,"message": 'Email already registered'}
            return jsonify(response), 400

        if not name or not email or not password:
            response = {"Body": None,"status": "error","statusCode": 400,"message": 'Name, email, and password are required'}
            return jsonify(response), 400

        if not re.match(email_regex, email):
            response = {"Body": None, "status": "error", "statusCode": 400, "message": 'Invalid email format'}
            return jsonify(response), 400

        if not re.match(password_regex, password):
            response = {"Body": None,"status": "error","statusCode": 400,"message": 'Password must have at least 8 characters'}
            return jsonify(response), 400

        password_hash = hashlib.sha256(password.encode()).hexdigest()

        user = User(name=name, email=email, password=password_hash,role=role)
        user.save()

        response = {"Body": None,"status": "success","statusCode": 200,"message": 'Registration successful'}
        return jsonify(response), 200

    except Exception as e:
        response = { "Body": None,"status": "error","statusCode": 500,"message": str(e)}
        return jsonify(response), 500
# __________________________________________________________________________________________________________________________
# sending json  bundale ragister api

# @signUp_bp.route('/register', methods=['POST'])
# def register():
#     try:
#         data = request.json
#         name = data.get('name')
#         email = data.get('email')
#         password = data.get('password')
#         role = data.get('role')
#         json_data = data.get('json_data')

#         # Check if the email is already registered
#         existing_user = User.objects(email=email).first()
#         if existing_user:
#             response = {"Body": None, "status": "error", "statusCode": 400, "message": 'Email already registered'}
#             return jsonify(response), 400

#         if not name or not email or not password:
#             response = {"Body": None, "status": "error", "statusCode": 400, "message": 'Name, email, and password are required'}
#             return jsonify(response), 400

#         if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
#             response = {"Body": None, "status": "error", "statusCode": 400, "message": 'Invalid email format'}
#             return jsonify(response), 400

#         if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$", password):
#             response = {"Body": None, "status": "error", "statusCode": 400, "message": 'Password must have at least 8 characters, one uppercase letter, and one digit'}
#             return jsonify(response), 400

#         password_hash = hashlib.sha256(password.encode()).hexdigest()

#         user = User(name=name, email=email, password=password_hash, role=role)
#         user.save()

#         # Store additional JSON data in UserData collection
#         user_data = UserData(user=user, data=json_data)
#         user_data.save()

#         response = {"Body": None, "status": "success", "statusCode": 200, "message": 'Registration successful'}
#         return jsonify(response), 200

#     except Exception as e:
#         response = {"Body": None, "status": "error", "statusCode": 500, "message": str(e)}
#         return jsonify(response), 500
    
    
# @signUp_bp.route('/user/<user_id>', methods=['GET'])
# def get_user_json_data(user_id):
#     try:
#         # Find the user by user_id
#         user = User.objects.get(id=user_id)

#         # Find associated JSON data in UserData collection
#         user_data = UserData.objects(user=user).first()

#         if user_data:
#             # Include only JSON data in the response
#             response = user_data.data
#             return jsonify(response), 200
#         else:
#             response = {"Body": None, "status": "error", "statusCode": 404, "message": 'User data not found'}
#             return jsonify(response), 404

#     except Exception as e:
#         response = {"Body": None, "status": "error", "statusCode": 500, "message": str(e)}
#         return jsonify(response), 500

# __________________________________________________________________________________________________________________________




login_bp = Blueprint('login', __name__)
@login_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        
        # Validate the presence of 'name', 'email', and 'password'
        if email is None:
                   return jsonify({'error': 'Email is required', 'status_code': 400}), 400

        if password is None:
                  return jsonify({'error': 'Password is required', 'status_code': 400}), 400

 
        user = User.objects(email=email).first()

        if user:
            provided_password_hash = hashlib.sha256(password.encode()).hexdigest()

            if provided_password_hash == user.password:
                payload = {
                    'user_id': str(user.id),
                    'sub': '1', 
                    'jti': str(uuid.uuid4()),  # Generate a unique identifier
                    'identity': user.email, 
                    # 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=50),
                    'role': user.role , # Include the 'role' claim here
                    'type': 'access',
                    'fresh': True
                }
                token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

                return jsonify({'message': 'Login successful', 'access_token': token}), 200

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






# @login_bp.route('/login', methods=['POST'])
# @jwt_required(optional=True)  # Use optional=True to allow both authenticated and unauthenticated requests
# def login():
#     try:
#         if request.method == 'POST':
#             data = request.json
#             email = data.get('email')
#             password = data.get('password')
            
#             # Validate the presence of 'name', 'email', and 'password'
#             if email is None:
#                 return jsonify({'error': 'Email is required', 'status_code': 400}), 400

#             if password is None:
#                 return jsonify({'error': 'Password is required', 'status_code': 400}), 400

#             user = User.objects(email=email).first()

#             if user:
#                 provided_password_hash = hashlib.sha256(password.encode()).hexdigest()

#                 if provided_password_hash == user.password:
#                     payload = {
#                         'user_id': str(user.id),
#                         'sub': '1', 
#                         'jti': str(uuid.uuid4()),  # Generate a unique identifier
#                         'identity': user.email, 
#                         'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=50),
#                         'role': user.role,  # Include the 'role' claim here
#                         'type': 'access',
#                         'fresh': True
#                     }
#                     token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

#                     return jsonify({'message': 'Login successful', 'access_token': token}), 200

#             return jsonify({'error': 'Invalid email or password'}), 401

#         elif request.method == 'GET':
#             # Handle the logic for the role based on the authenticated user
#             current_user = get_jwt_identity()
#             current_user_role = get_jwt_claims().get('role')

#             if current_user_role == 'admin':
#                 return jsonify({'status_code': 200, 'message': 'success', 'role': 'admin'}), 200
#             elif current_user_role == 'user':
#                 return jsonify({'status_code': 200, 'message': 'success', 'role': 'user'}), 200
#             else:
#                 return jsonify({'status_code': 403, 'message': 'Permission denied'}), 403

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500