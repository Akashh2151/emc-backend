import secrets
from flask import Flask
from flask_jwt_extended import JWTManager
from controller.signInsignUp import signUp_bp # Import your blueprint
from controller.signInsignUp import login_bp
# from controller.forgetpassword import forgetpassword_app
# from controller.shop import shopapp
# from controller.resto import restoapp
# from security.errors import expired_token_callback



app = Flask(__name__)
# app.secret_key = '98c5bc0a178ff2d6c0c1471c6f3dc5e4'
app.config['SECRET_KEY'] = '98c5bc0a178ff2d6c0c1471c6f3dc5e4'

app.register_blueprint(signUp_bp)
app.register_blueprint(login_bp)
# app.register_blueprint(forgetpassword_app)
# app.register_blueprint(shopapp)
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




@app.route('/')
def hello_world():
    return 'Hello World Again'
 


# main driver function
if __name__ == '__main__':
    app.run()
