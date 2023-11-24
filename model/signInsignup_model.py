from mongoengine import Document, StringField, EmailField, IntField, BooleanField,ReferenceField,DictField
from flask import Flask
from flask_mongoengine import MongoEngine
# from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

from mongoengine import connect
# # Replace the values with your username, password, and cluster name
db_uri = "mongodb+srv://akashh2151:aOSefZ94SgQEkzmg@cluster0.25xmos0.mongodb.net/?retryWrites=true&w=majority"
# Replace the value with your database name
connect(host=db_uri, db="emc_project2151")



# disconnect()

# local_db_uri = "mongodb://localhost:27017"
# local_db_name = "emc_project_local"
# db = MongoEngine()
# connect(host=local_db_uri, db=local_db_name)


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
#  _________________________________________________________________________________________  
class User(Document):
    name = StringField(required=True, max_length=100)
    email = EmailField(unique=True, required=True)
    password = StringField(required=True, max_length=100)
    role = StringField(required=True, choices=("user", "admin")) 
    
    
# json bundle sending model      
# Define the User model
# class User(Document):
#     name = StringField(required=True)
#     email = EmailField(unique=True, required=True)
#     password = StringField(required=True)
#     role = StringField(choices=('admin', 'user'), required=True)

# # Define the UserData model to store additional JSON data
# class UserData(Document):
#     user = ReferenceField(User)
#     data = DictField()
    
# class Shop(db.Document):
#     user = db.ReferenceField(User, reverse_delete_rule=db.CASCADE)
#     shop_data = db.DictField()

# class Resto(db.Document):
#     user = db.ReferenceField(User, reverse_delete_rule=db.CASCADE)
#     resto_data = db.DictField()    
    
# ______________________________________________________________________________  
    # age = IntField()
    # is_active = BooleanField(default=True)

    # def set_password(self, password):
    #     self.password = generate_password_hash(password)

    # def check_password(self, password):
    #     return check_password_hash(self.password, password)    