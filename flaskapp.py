from flask import Flask
from controller.signInsignUp import signUp_bp # Import your blueprint
from controller.signInsignUp import login_bp
# from controller.forgetpassword import forgetpassword_app
# from controller.shop import shopapp
# from controller.resto import restoapp

app = Flask(__name__)
app.secret_key = '98c5bc0a178ff2d6c0c1471c6f3dc5e4'

app.register_blueprint(signUp_bp)
app.register_blueprint(login_bp)
app.register_blueprint(forgetpassword_app)
app.register_blueprint(shopapp)
app.register_blueprint(restoapp)



@app.route('/')
def hello_world():
    return 'Hello World Again'



# main driver function
if __name__ == '__main__':
    app.run()
