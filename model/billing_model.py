from attr import validate
from mongoengine import Document, StringField,ReferenceField, EmailField,ListField,DecimalField,DateTimeField,IntField,URLField,EmbeddedDocumentField,EmbeddedDocument,FloatField
# from pydantic import ValidationError
# from pydantic import ValidationError
from pymongo import MongoClient

 
from mongoengine import connect
from wtforms import ValidationError
  

  
from model.signInsignup_model import User
# Replace the values with your MongoDB URI and other settings
db_uri = "mongodb+srv://akashh2151:aOSefZ94SgQEkzmg@cluster0.25xmos0.mongodb.net/?retryWrites=true&w=majority"
connect(host=db_uri, db="emc_project2151")
# connect(host=db_uri, db="emc_project2151")


def validate_non_empty(value):
    if isinstance(value, (str,)):
        if not value.strip():
            raise ValidationError("Field cannot be empty.")
    elif isinstance(value, (int, float)):
        # You can customize this part based on your requirements for numeric fields
        pass



class Billing(Document):
    itemCode = StringField()
    itemName = StringField()
    quantity = IntField()
    itemPrice = DecimalField()
    itemTotal = DecimalField()
    creator = ReferenceField(User)