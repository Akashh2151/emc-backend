from flask import Flask, Response, make_response
from flask_jwt_extended import JWTManager
from controller.signInsignUp import signUp_bp  
from controller.signInsignUp import login_bp
from flask_cors import CORS
from controller.shop import shopapp
 
 
app = Flask(__name__)
app.config['SECRET_KEY'] = '98c5bc0a178ff2d6c0c1471c6f3dc5e4'


app.register_blueprint(signUp_bp)
app.register_blueprint(login_bp)
# app.register_blueprint(forgetpassword_app)
app.register_blueprint(shopapp)
# app.register_blueprint(restoapp)



# Configure the JWT token location
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 1

# Other Flask-JWT-Extended configuration options
# secret_key = secrets.token_hex(32)  # Generates a 64-character (256-bit) hexadecimal secret key
app.config['SECRET_KEY'] = '98c5bc0a178ff2d6c0c1471c6f3dc5e4'# Set your secret key
app.config['JWT_ALGORITHM'] = 'HS256'  # Choose an appropriate algorithm
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False  # Set your token expiration as needed

# Initialize the Flask-JWT-Extended extension
jwt = JWTManager(app)

# Enable CORS for all routes
# CORS(app)
# CORS(app, origins=['http://localhost:3000', 'https://my-digital-ocean-app.com'])
# Enable CORS for all routes
CORS(app, origins=['http://localhost:3000', 'https://my-digital-ocean-app.com'], supports_credentials=True)



@app.route('/')
def hello_world():
    resp = make_response('Hello World Again')
    
    # Set the cookie with SameSite=None and Secure flag
    resp.set_cookie('my_cookie', 'cookie_value', secure=True, samesite='None')
    
    return resp


@app.route('/')
def hello_world():
    return 'Hello World Again'
 


# main driver function
if __name__ == '__main__':
    app.run()
