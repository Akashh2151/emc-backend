from flask import jsonify
from flask_jwt_extended import JWTManager
# from flask_jwt_extended import JWTManager



def email_already_registered_error():
    return jsonify({'status_code': 400, 'error': 'Email is already registered'}), 400

@JWTManager.expired_token_loader
def expired_token_callback(expired_token):
    return jsonify({'status_code': 401, 'error': 'Token has expired'}), 401

def unauthorized_error(e):
    return jsonify({'status_code': 401, 'error': 'Unauthorized'}), 401

def forbidden_error(e):
    return jsonify({'status_code': 403, 'error': 'Permission denied'}), 403

def invalid_token_format_error(e):
    return jsonify({'status_code': 400, 'error': 'Invalid token format'}), 400

def internal_server_error(e):
    return jsonify({'status_code': 500, 'error': 'Internal server error'}), 500