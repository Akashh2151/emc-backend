import hashlib  # Import the hashlib library
from model.signInsignup_model import AuthModel, SignupModel
from flask import jsonify, request

auth_model = AuthModel()
signup_model = SignupModel()

from flask import Blueprint

signUp_bp = Blueprint('signUp', __name__)

@signUp_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    # Check if the email already exists in the database
    existing_user = signup_model.find_user_by_email(data.get("email"))
    if existing_user:
        return jsonify({'error': 'Email already registered'}), 400

    result = signup_model.register_user(data)

    if "error" in result:
        return jsonify({'error': result['error']}), 400

    return jsonify({'message': 'Registration successful'})

login_bp = Blueprint('login', __name__)

@login_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = auth_model.login_user(email, password)

    if user:
        # Hash the provided password for comparison
        provided_password = password.encode('utf-8')
        hashed_provided_password = hashlib.sha256(provided_password).hexdigest()

        # Compare the hashed provided password with the stored hashed password
        if hashed_provided_password == user["password"]:
            role = user["role"]  # Update to use the "role" directly from the user
            response = {'message': 'Login successful'}
            if "owner" in role:
                response["role_info"] = "Welcome Owner"
            elif "managerOne" in role:
                response["role_info"] = "Welcome Manager"
            elif "staffOne" in role:
                response["role_info"] = "Welcome Staff"
            return jsonify(response)
    
    return jsonify({'error': 'Invalid email or password'}), 404
