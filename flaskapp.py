from flask import Flask
from controller.signInsignUp import signUp_bp # Import your blueprint
from controller.signInsignUp import login_bp

app = Flask(__name__)

# Register the blueprint
app.register_blueprint(signUp_bp)
app.register_blueprint(login_bp)



@app.route('/')
def hello_world():
    return 'Hello World Again'

# main driver function
if __name__ == '__main__':
    app.run()
