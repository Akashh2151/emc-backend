from attr import validate
from mongoengine import Document, StringField, BooleanField,ListField,ValidationError,IntField,URLField,EmbeddedDocumentField,EmbeddedDocument,FloatField
# from pydantic import ValidationError
from pymongo import MongoClient

from mongoengine import connect
from wtforms import EmailField
# disconnect
# Replace the values with your username, password, and cluster name
db_uri = "mongodb+srv://akashh2151:aOSefZ94SgQEkzmg@cluster0.25xmos0.mongodb.net/?retryWrites=true&w=majority"
# Replace the value with your database name
connect(host=db_uri, db="emc_project2151")
# connect(host=db_uri, db="emc_project2151")






class Order(Document):
    vendorCode = StringField(required=True, unique=True)
    vendorName = StringField(required=True)
    vendorEmail = EmailField(required=True)
    vendorMobile = StringField(required=True, regex=r'^\d{10}$')
    vendorAddr =StringField(required=True)
    
    
# Define RestoMenuMaster document
class RestoMenuMaster(Document):
    showName = StringField(required=True, null=False)
    path = StringField(required=True, null=False)
    subMenu = ListField(EmbeddedDocumentField('SubMenu'))  # Add the new field
    
    

# Define SubMenu embedded document
class SubMenu(EmbeddedDocument):
    showName = StringField(required=True, null=False)
    connectedTo = StringField(required=True, null=False)
    path = StringField(required=True, null=False)
    
    
    
# Define RestoSellMaster document
class RestoSellMaster(Document):
    showName = StringField(required=True, null=False)
    status = StringField(required=True, null=False)
    sellUnits = ListField(StringField(required=True, null=False))
    printers = ListField(StringField(required=True, null=False))
    sellType = ListField(StringField(required=True, null=False))    
    
    
    
# Define GeneralMaster document
class GeneralMaster(Document):
    billId = EmbeddedDocumentField('BillId')
    language = StringField()
    theme = StringField()
    shopName = StringField()
    sources = ListField(StringField())
    shopAddress = StringField()
    role = EmbeddedDocumentField('Role')
    name = StringField()
    userPic = StringField()
    businessSummaryStatus = StringField()
    businessSummary = ListField(EmbeddedDocumentField('BusinessSummary'))
    orderTypes = EmbeddedDocumentField('OrderTypes')

# Define embedded documents
class BillId(EmbeddedDocument):
    startString = StringField()
    endString = IntField()

class Role(EmbeddedDocument):
    title = StringField()
    accessTo = ListField(StringField())

class BusinessSummary(EmbeddedDocument):
    businessURL = StringField()
    businessName = StringField()
    businessAddress = StringField()
    businessMobile = ListField(StringField())
    businessEmail = EmailField()
    businessDescription = StringField()

class OrderTypes(EmbeddedDocument):
    showName = StringField()
    properties = ListField(StringField())  