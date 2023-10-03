import pytest
from model.signInsignup_model import AuthModel, SignupModel
from datetime import datetime

# Initialize test instances of AuthModel and SignupModel with a test database
@pytest.fixture
def auth_model_instance():
    return AuthModel(database_url="your_test_database_url")

@pytest.fixture
def signup_model_instance():
    return SignupModel(database_url="your_test_database_url")

# Test the AuthModel class
def test_auth_model(auth_model_instance):
    # Test case 1: Valid login
    user_data = {
        "email": "test@example.com",
        "password": "hashed_password_here"  # Replace with the actual hashed password
    }
    user = auth_model_instance.login_user(user_data["email"], user_data["password"])
    assert user is not None  # Assuming a user exists with the given email and password

    # Test case 2: Invalid login
    invalid_user_data = {
        "email": "nonexistent@example.com",
        "password": "invalid_password_here"  # Replace with an invalid password
    }
    user = auth_model_instance.login_user(invalid_user_data["email"], invalid_user_data["password"])
    assert user is None  # Assuming the user does not exist or the password is incorrect

# Test the SignupModel class
def test_signup_model(signup_model_instance):
    # Test case 1: Register a new user
    auth_data = {
        "firstName": "John",
        "lastName": "Doe",
        "email": "new_user@example.com",
        "password": "new_user_password",
        "userName": "johndoe",
        "role": "user",
        "company": "Example Corp",
        "businessCategory": "Tech",
        "bundle": "Basic",
        "emailverified": False,
        "locale": "en-US",
        "picture": "",
        "expirydate": None,
        "registrationDate": datetime.utcnow()
    }
    result = signup_model_instance.register_user(auth_data)
    assert "error" not in result  # Assuming the registration is successful

    # Test case 2: Attempt to register a duplicate email
    existing_user_data = {
        "firstName": "Jane",
        "lastName": "Smith",
        "email": "existing_user@example.com",
        "password": "existing_user_password",
        "userName": "janesmith",
        "role": "user",
        "company": "Example Corp",
        "businessCategory": "Tech",
        "bundle": "Basic",
        "emailverified": False,
        "locale": "en-US",
        "picture": "",
        "expirydate": None,
        "registrationDate": datetime.utcnow()
    }
    result = signup_model_instance.register_user(existing_user_data)
    assert "error" in result  # Assuming the email is already registered

# Add more test cases as needed

