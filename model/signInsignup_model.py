from mongoengine import Document, StringField, EmailField, IntField, BooleanField
from flask import Flask
from flask_mongoengine import MongoEngine
# from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

from mongoengine import connect
# Replace the values with your username, password, and cluster name
# db_uri = "mongodb+srv://akashh2151:aOSefZ94SgQEkzmg@cluster0.25xmos0.mongodb.net/?retryWrites=true&w=majority"
# Replace the value with your database name
# connect(host=db_uri, db="emc_project2151")


connect(
    db='emc_project2151',
    host='mongodb+srv://akashh2151:aOSefZ94SgQEkzmg@cluster0.25xmos0.mongodb.net/test?retryWrites=true&w=majority',
)

# app.config['MONGODB_SETTINGS'] = {
#     'db': 'emc_project2151',  # Use the specified MongoDB database
#     'host': 'localhost',
#     'port': 27017
# }
# db = MongoEngine()
# db.init_app(app)


# class User(Document):
    # name = StringField(required=True, max_length=100)
    # email = EmailField(unique=True, required=True)
    # password = StringField(required=True, max_length=100)
    # age = IntField()
    # is_active = BooleanField(default=True)
    
# class User(db.Document):
#     name = db.StringField(required=True, max_length=100)
#     email = db.EmailField(unique=True, required=True)
#     password = db.StringField( required=True)
    
class User(Document):
    name = StringField(required=True, max_length=100)
    email = EmailField(unique=True, required=True)
    password = StringField(required=True, max_length=100)
    role = StringField(required=True, choices=("user", "admin"))

    
    # age = IntField()
    # is_active = BooleanField(default=True)

    # def set_password(self, password):
    #     self.password = generate_password_hash(password)

    # def check_password(self, password):
    #     return check_password_hash(self.password, password)    