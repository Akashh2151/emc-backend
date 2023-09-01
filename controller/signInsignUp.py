# import hashlib
from flask import jsonify, request
# import mysqlx
from flaskapp import app 
from model.signInsignup_model import AuthModel, SignupModel

# obj = SignupModel()


auth_model = AuthModel()
signup_model = SignupModel()

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    result = SignupModel().register_user(data)
    return jsonify(result)




@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    
    user = AuthModel().login_user(email, password)
    if user:
        role = user.get("role")
        response = {'message': 'Login successful'}
        if role == "owner":
            response["role_info"] = "Welcome Owner"
        elif role == "managerOne":
            response["role_info"] = "Welcome Manager"
        elif role == "staffOne":
            response["role_info"] = "Welcome Staff"
        return jsonify(response)
    else:
        return jsonify({'error': 'Invalid email or password'}), 404

if __name__ == "__main__":
    app.run(debug=True)