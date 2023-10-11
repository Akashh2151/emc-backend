import hashlib
from flask import Blueprint, Flask, request, jsonify, session
from pymongo import MongoClient
import random
import string
from model.forgetpassword_model import send_email

app = Flask(__name__)
 
forgetpassword_app = Blueprint('forgetpassword', __name__)
# app.config['SESSION_TYPE'] = 'null'  # Disable sessions for this blueprint


# MongoDB Configuration
client = MongoClient("mongodb+srv://akashh2151:aOSefZ94SgQEkzmg@cluster0.25xmos0.mongodb.net/?retryWrites=true&w=majority")
db = client["emc_project"]
collection = db["signup"]

 

# Generate a random OTP
def generate_otp():
    otp = ''.join(random.choices(string.digits, k=6))
    return otp

@forgetpassword_app.route('/send_otp', methods=['POST'])
def send_otp():
    data = request.json
    email = data.get('email')

    user = collection.find_one({"email": email})

    if user:
        otp = generate_otp()
        session['otp'] = otp  # Store OTP in the session

        message = f"Your OTP for password reset is: {otp}"
        
        send_email("Password Reset OTP", email, message)
        return jsonify({"message": "OTP sent successfully"}), 200
    else:
        return jsonify({"message": "User not found"}), 404


@forgetpassword_app.route('/validate_otp', methods=['POST'])
def validate_otp():
    data = request.json
    entered_otp = data.get('otp')

    # Check if the entered OTP matches the one stored in the session
    if 'otp' in session and session['otp'] == entered_otp:
        return jsonify({"message": "OTP is valid"}), 200
    else:
        return jsonify({"message": "Invalid OTP"}), 400



@forgetpassword_app.route('/change_password', methods=['POST'])
def change_password():
    data = request.json
    email = data.get('email')
    new_password = data.get('new_password')
    confirm_password = data.get('confirm_password')
    entered_otp = data.get('otp')

    # Check if the entered OTP matches the one stored in the session
    if 'otp' in session and session['otp'] == entered_otp:
        if new_password != confirm_password:
            session.pop('otp',None)
            return jsonify({"message": "Password and confirmation do not match"}), 400

        # Hash the new password
        hashed_password = hashlib.sha256(new_password.encode()).hexdigest()

        # Update the user's password in the database
        user = collection.find_one({"email": email})
        if user:
            collection.update_one(
                {"email": email},
                {"$set": {"password": hashed_password}}
            )
            return jsonify({"message": "Password changed successfully"}), 200
        else:
            return jsonify({"message": "User not found"}), 404
    else:
        return jsonify({"message": "Invalid OTP"}), 400