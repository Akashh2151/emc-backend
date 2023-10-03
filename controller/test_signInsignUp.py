import pytest
from model.signInsignup_model import AuthModel, SignupModel
from controller.signInsignUp import auth_model, signup_model

# Initialize test instances of AuthModel and SignupModel with a test database
@pytest.fixture
def auth_model_instance():
    return AuthModel(database_url="your_test_database_url")

@pytest.fixture
def signup_model_instance():
    return SignupModel(database_url="your_test_database_url")

# Test the AuthModel class
def test_auth_model(auth_model_instance):
    # Write test cases for AuthModel methods
    pass

# Test the SignupModel class
def test_signup_model(signup_model_instance):
    # Write test cases for SignupModel methods
    pass

# You can also write integration tests for your Flask routes using a test client
@pytest.fixture
def test_client():
    from flaskapp import app  # Replace with your Flask app import
    app.config['TESTING'] = True
    return app.test_client()

def test_register_route(test_client):
    # Write test cases for the /register route
    pass

def test_login_route(test_client):
    # Write test cases for the /login route
    pass
