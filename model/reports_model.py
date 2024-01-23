from flask import Flask, jsonify, request
from mongoengine import Document, StringField, FloatField, ListField, DateTimeField, EmbeddedDocumentField, EmbeddedDocument
# import datetime
from datetime import datetime
from attr import validate
from mongoengine import Document,EmbeddedDocument, DateTimeField, StringField,ReferenceField, EmailField,ListField,DecimalField,DateTimeField,IntField,URLField,EmbeddedDocumentField,EmbeddedDocument,FloatField
# from pydantic import ValidationError
# from pydantic import ValidationError
from pymongo import MongoClient
from mongoengine import EmbeddedDocument, StringField
 

from mongoengine.fields import DateTimeField

 
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



# MongoDB Models
class PurchaseHistoryEntry(EmbeddedDocument):
    date = DateTimeField()
    action = StringField()

class SaleHistoryEntry(EmbeddedDocument):
    action = StringField(required=True)  # 'purchase', 'sale', 'cancel'
    type = StringField(required=True)  # 'sale' or 'purchase'
    date = DateTimeField(required=True)
    amount = DecimalField(precision=2)


class ExpenseEntry(EmbeddedDocument):
    date = DateTimeField()
    amount = FloatField()


class Expense(Document):
    amount = DecimalField(precision=2, required=True)
    date = DateTimeField(required=True)