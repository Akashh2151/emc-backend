from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from controller.signInsignUp import signUp_bp  
from controller.signInsignUp import login_bp
from flask_cors import CORS
from controller.shop import shopapp
from controller.shop import newfrom
from controller.rating import rating
from controller.resto import restoapp
from controller.master import master

app = Flask(__name__)
app.config['SECRET_KEY'] = '98c5bc0a178ff2d6c0c1471c6f3dc5e4'

app.register_blueprint(signUp_bp)
app.register_blueprint(login_bp)
app.register_blueprint(shopapp)
app.register_blueprint(newfrom)
app.register_blueprint(rating)
app.register_blueprint(restoapp)
app.register_blueprint(master)
 


# Configure the JWT token location
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 1
 


app.config['SECRET_KEY'] = '98c5bc0a178ff2d6c0c1471c6f3dc5e4'# Set your secret key
app.config['JWT_ALGORITHM'] = 'HS256'  # Choose an appropriate algorithm
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False  # Set your token expiration as needed

# Initialize the Flask-JWT-Extended extension
jwt = JWTManager(app)

# Enable CORS for all routes
CORS(app)
CORS(app, origins=['http://localhost:3000', 'https://my-digital-ocean-app.com'])


# Enable CORS for all routes with wildcard *
# CORS(app, origins='*')

 

@app.route('/')
def hello_world():
      return jsonify({'message': 'hi All team'}), 200
 


# main driver function
if __name__ == '__main__':
    app.run()
