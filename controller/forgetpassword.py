# import hashlib
# import random
# import string
# from flask import Blueprint, Flask, request, jsonify, session
# from pymongo import MongoClient
# from model.forgetpassword_model import send_email

# app = Flask(__name__)
# forgetpassword_app = Blueprint('forgetpassword', __name__)
 
 

# def generate_otp():
#     otp = ''.join(random.choices(string.digits, k=6))
#     return otp



# @forgetpassword_app.route('/send_otp', methods=['POST'])
# def send_otp():
#     try:
#         data = request.json
#         email = data.get('email')
#         user = collection.find_one({"email": email})

#         if user:
#             otp = generate_otp()
#             session['otp'] = otp  # Store OTP in the session
#             message = f"Your OTP for password reset is: {otp}"
#             send_email("Password Reset OTP", email, message)
#             return jsonify({"message": "OTP sent successfully"}), 200
#         else:
#             return jsonify({"message": "User not found"}), 404
#     except Exception as e:
#         return jsonify({"message": "An error occurred"}), 500



# @forgetpassword_app.route('/validate_otp', methods=['POST'])
# def validate_otp():
#     try:
#         data = request.json
#         entered_otp = data.get('otp')

#         if 'otp' in session and session['otp'] == entered_otp:
#             return jsonify({"message": "OTP is valid"}), 200
#         else:
#             return jsonify({"message": "Invalid OTP"}), 400
#     except Exception as e:
#         return jsonify({"message": "An error occurred"}), 500




# @forgetpassword_app.route('/change_password', methods=['POST'])
# def change_password():
#     try:
#         data = request.json
#         email = data.get('email')
#         new_password = data.get('new_password')
#         confirm_password = data.get('confirm_password')
#         entered_otp = data.get('otp')

#         if 'otp' in session and session['otp'] == entered_otp:
#             if new_password != confirm_password:
#                 session.pop('otp', None)
#                 return jsonify({"message": "Password and confirmation do not match"}), 400

#             hashed_password = hashlib.sha256(new_password.encode()).hexdigest()

#             user = collection.find_one({"email": email})
#             if user:
#                 collection.update_one({"email": email}, {"$set": {"password": hashed_password}})
#                 return jsonify({"message": "Password changed successfully"}), 200
#             else:
#                 return jsonify({"message": "User not found"}), 404
#         else:
#             return jsonify({"message": "Invalid OTP"}), 400
#     except Exception as e:
#         return jsonify({"message": "An error occurred"}), 500
