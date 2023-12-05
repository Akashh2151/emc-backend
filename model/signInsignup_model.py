from mongoengine import Document, StringField, EmailField,DictField,ListField
from flask import Flask
from flask_mongoengine import MongoEngine
from mongoengine import connect,disconnect
 


app = Flask(__name__)

db_uri = "mongodb+srv://akashh2151:aOSefZ@cluster0.25xmos0.mongodb.net/emc_project2151?retryWrites=true&w=majority"
connect(host=db_uri, db="emc_project2151")
disconnect()



class User(Document):
    username = StringField(required=True, max_length=100)
    email = EmailField(unique=True, required=True)
    password = StringField(required=True, max_length=100)
    role = StringField(required=True, choices=("user", "admin")) 
    name=StringField( max_length=100)
    mobilenumber = StringField(max_length=15)  # Assuming a reasonable max length for a phone number
    businessname = StringField(max_length=100)
    businesstype = StringField(max_length=100)
    shopbundale = ListField(DictField())
    restobundale = ListField(DictField()) # Assuming it's optional
    