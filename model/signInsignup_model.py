from mongoengine import Document, StringField, EmailField,DictField,ListField,DynamicField
from flask import Flask
from flask_mongoengine import MongoEngine
from mongoengine import connect,disconnect
from pydantic import ValidationError
 


app = Flask(__name__)

db_uri = "mongodb+srv://akashh2151:aOSefZ@cluster0.25xmos0.mongodb.net/emc_project2151?retryWrites=true&w=majority"
connect(host=db_uri, db="emc_project2151")
disconnect()


def validate_non_empty(value):
    if isinstance(value, (str,)):
        if not value.strip():
            raise ValidationError("Field cannot be empty.")
    elif isinstance(value, (int, float)):
        # You can customize this part based on your requirements for numeric fields
        pass

# Define the User model
class User(Document):
    name = StringField(max_length=24)
    mobile = StringField(required=True, max_length=10, unique=True)  # Unique mobile field
    email = EmailField(unique=True, required=True)  # Unique email field
    password = StringField(required=True, max_length=100)
    businessName = StringField(max_length=24)
    businessMobile = StringField(max_length=10, unique=True)  # Unique businessMobile field
    businessEmail = EmailField(unique=True, required=True)  # Unique businessEmail field
    businessAddress = StringField(max_length=100)
    businessType = StringField(max_length=100)
    restoBundle = ListField(DynamicField())