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

# Order model with creator field
class Order(Document):
    vendorCode = StringField(required=True, unique=True)
    vendorName = StringField(required=True)
    vendorEmail = EmailField(required=True)
    vendorMobile = StringField(required=True, regex=r'^\d{10}$')
    vendorAddr = StringField(required=True)
    creator = ReferenceField(User, reverse_delete_rule=2)  # Assuming User is the creator
    
    
class ItemMaster(Document):
    name = StringField(required=True)
    description = StringField()
    measureUnit = StringField()
    price = FloatField()
    category = StringField()
    subCategory = StringField()
    nutrition = StringField()
    creator = ReferenceField(User, reverse_delete_rule=2)

 

class Verification(EmbeddedDocument):
    date = DateTimeField()
    status = StringField()
    comments = StringField()
    
    
    
# Define TaxMaster model
class TaxMaster(Document):
    taxName = StringField(required=True)
    creator = ReferenceField(User, required=True)  # Assuming User is your User model

    

class History(EmbeddedDocument):
    date = DateTimeField(format='%Y-%m-%dT%H:%M:%S.%fZ')
    action = StringField()



class CustomerMaster(Document):
    customerName = StringField(required=True)
    customerMobile = StringField(required=True, regex=r'^\d{10}$')
    customerEmail = EmailField(required=True)
    customerLastVisit = DateTimeField(format='%Y-%m-%dT%H:%M:%S.%fZ')
    customerAddr = StringField()
    customerHistory = ListField(EmbeddedDocumentField(History))
    



# class EmployeeMaster(Document):
#     employeeName = StringField(required=True)
#     employeeMobile = StringField(required=True)
#     employeeEmail = EmailField(required=True)
#     employeeAddr = StringField()
#     employeeHistory = ListField(EmbeddedDocumentField(History))
#     employeeVerification = ListField(EmbeddedDocumentField(Verification))


class History(EmbeddedDocument):
    date = StringField()
    action = StringField()

class Verification(EmbeddedDocument):
    date = StringField()
    status = StringField()
    comments = StringField()

class EmployeeMaster(Document):
    employeeName = StringField(required=True)
    employeeMobile = StringField(required=True)
    employeeEmail = EmailField(required=True)
    employeeAddr = StringField()
    employeeHistory = ListField(EmbeddedDocumentField(History))
    employeeVerification = ListField(EmbeddedDocumentField(Verification))
    creator = ReferenceField(User, reverse_delete_rule=2) 
    
    
    
    
class Item(Document):
    itemCode = StringField(required=True, unique=True)
    itemName = StringField(required=True)
    itemCategory = StringField()
    itemSubCategory = StringField(validation=validate_non_empty)
    itemPrice = DecimalField(precision=2,required=True)
    ingredients = ListField()
    recipe = StringField()
    allergen = StringField()
    portionSize = StringField()
    status = StringField()
    tax = DecimalField()
    discount = DecimalField()
    # images = ListField(StringField())  # Assuming images are stored as file paths or URLs
    currentStock = IntField()
    barcode = StringField()
    creator = ReferenceField(User, reverse_delete_rule=2)  # Reverse delete rule: when a user is deleted, set the reference to None
    # salesHistory = ListField(EmbeddedDocumentField(History))
    # customNotes = StringField()    

 


class Table(Document):
        tableCode =StringField(required=True,unique=True)
        tableName=StringField(required=True,)
        tableStatus =StringField(required=True)
        tableQR=StringField(required=True)
        tablePlacement =StringField(required=True)
        
# Assume you have a User model defined
class User(Document):
    # Define your User model fields here
    pass


class Vendor(Document):
    vendorCode = StringField(required=True, unique=True)
    vendorName = StringField(required=True)
    vendorEmail = EmailField(required=True)
    vendorMobile = StringField(required=True)
    vendorAddr = StringField(required=True)
    creator = ReferenceField(User, reverse_delete_rule=2)
 
    
# # Define RestoMenuMaster document
# class RestoMenuMaster(Document):
#     showName = StringField(required=True, null=False)
#     path = StringField(required=True, null=False)
#     subMenu = ListField(EmbeddedDocumentField('SubMenu'))  # Add the new field
    
    

# # Define SubMenu embedded document
# class SubMenu(EmbeddedDocument):
#     showName = StringField(required=True, null=False)
#     connectedTo = StringField(required=True, null=False)
#     path = StringField(required=True, null=False)
    
    
    
# # Define RestoSellMaster document
# class RestoSellMaster(Document):
#     showName = StringField(required=True, null=False)
#     status = StringField(required=True, null=False)
#     sellUnits = ListField(StringField(required=True, null=False))
#     printers = ListField(StringField(required=True, null=False))
#     sellType = ListField(StringField(required=True, null=False))    
    
    
    
# # Define GeneralMaster document
# class GeneralMaster(Document):
#     billId = EmbeddedDocumentField('BillId')
#     language = StringField()
#     theme = StringField()
#     shopName = StringField()
#     sources = ListField(StringField())
#     shopAddress = StringField()
#     role = EmbeddedDocumentField('Role')
#     name = StringField()
#     userPic = StringField()
#     businessSummaryStatus = StringField()
#     businessSummary = ListField(EmbeddedDocumentField('BusinessSummary'))
#     orderTypes = EmbeddedDocumentField('OrderTypes')

# # Define embedded documents
# class BillId(EmbeddedDocument):
#     startString = StringField()
#     endString = IntField()

# class Role(EmbeddedDocument):
#     title = StringField()
#     accessTo = ListField(StringField())

# class BusinessSummary(EmbeddedDocument):
#     businessURL = StringField()
#     businessName = StringField()
#     businessAddress = StringField()
#     businessMobile = ListField(StringField())
#     businessEmail = EmailField()
#     businessDescription = StringField()

# class OrderTypes(EmbeddedDocument):
#     showName = StringField()
#     properties = ListField(StringField())  