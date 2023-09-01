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
    result = signup_model.register_user(data["auth"])
    return jsonify(result)



@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    
    user = auth_model.login_user(email, password)
    if user:
        role = user["auth"]["role"]
        response = {'message': 'Login successful'}
        if "owner" in role:
            response["role_info"] = "Welcome Owner"
        elif "managerOne" in role:
            response["role_info"] = "Welcome Manager"
        elif "staffOne" in role:
            response["role_info"] = "Welcome Staff"
        return jsonify(response)
    else:
        return jsonify({'error': 'Invalid email or password'}), 404

if __name__ == "__main__":
    app.run(debug=True)