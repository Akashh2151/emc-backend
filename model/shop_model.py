# from pymongo import MongoClient
from attr import validate
from mongoengine import Document, StringField, BooleanField,ListField,ValidationError,IntField,URLField,EmbeddedDocumentField,EmbeddedDocument,FloatField
# from pydantic import ValidationError
from pymongo import MongoClient




# # MongoDB Configuration
# # client = MongoClient("mongodb+srv://akashh2151:aOSefZ94SgQEkzmg@cluster0.25xmos0.mongodb.net/?retryWrites=true&w=majority")
# client = MongoClient("mongodb://localhost:27017")


# db = client["emc_project2151"]
# shop_collection = db["shop"]
# general_master_collection = db["general_master"]
# shop_masters_collection = db["shop_masters"]
# shop_item_master_collection = db["shop_item_master"]
# shop_payment_master = db["shop_payment_master"]
# shop_invoices = db["shop_invoices"]



# from mongoengine import connect
# Replace the values with your username, password, and cluster name
# db_uri = "mongodb+srv://akashh2151:aOSefZ94SgQEkzmg@cluster0.25xmos0.mongodb.net/?retryWrites=true&w=majority"
# Replace the value with your database name
# connect(host=db_uri, db="emc_project2151")


from mongoengine import connect
# disconnect
# Replace the values with your username, password, and cluster name
db_uri = "mongodb+srv://akashh2151:aOSefZ94SgQEkzmg@cluster0.25xmos0.mongodb.net/?retryWrites=true&w=majority"
# Replace the value with your database name
connect(host=db_uri, db="emc_project2151")
connect(host=db_uri, db="emc_project2151")

# Disconnect existing connections
# disconnect()

# local_db_uri = "mongodb://localhost:27017"
# local_db_name = "emc_project_local"
# connect(host=local_db_uri, db=local_db_name)


# def validate_non_empty(value):
#     if not value.strip():  # Check if the string is empty after stripping whitespace
#         raise ValidationError("Field cannot be empty.")

def validate_non_empty(value):
    if isinstance(value, (str,)):
        if not value.strip():
            raise ValidationError("Field cannot be empty.")
    elif isinstance(value, (int, float)):
        # You can customize this part based on your requirements for numeric fields
        pass


# Define MenuMaster document
class MenuMaster(Document):
    showName = StringField(required=True,null=False)
    path = StringField(required=True,null=False)

    
class Product(Document):
    category = StringField(required=True, null=False, validation=validate_non_empty)
    subCategory = ListField(StringField(required=True, null=False), required=True, null=False)
    taxIndividual_status = StringField(required=True, null=False, validation=validate_non_empty)
    taxIndividual_value = BooleanField(default=False, null=False)
    barcode_status = StringField(required=True, null=False, validation=validate_non_empty)
    barcode_value = BooleanField(default=False, null=False)
    rackManagement_status = StringField(required=True, null=False, validation=validate_non_empty)
    rackManagement_value = BooleanField(default=False, null=False)
    deadStock_status = StringField(required=True, null=False, validation=validate_non_empty)
    deadStock_value = BooleanField(default=False, null=False)


    
    
# SellMaster
class SellMaster(Document):
    showName = StringField(required=True, null=False,validation=validate_non_empty)
    status = StringField(required=True, null=False,validation=validate_non_empty)
    sellUnits = ListField(StringField(required=True, null=False), required=True, null=False)
    printers = ListField(StringField(required=True, null=False), required=True, null=False)
    sellType = ListField(StringField(required=True, null=False), required=True, null=False)
    



#GeneralMaster
class GeneralMaster(Document):
    billId_startString = StringField(required=True, null=False, validation=validate_non_empty)
    billId_endString = IntField(required=True, null=False)
    language = StringField(required=True, null=False, validation=validate_non_empty)
    theme = StringField(required=True, null=False, validation=validate_non_empty)
    shopName = StringField(required=True, null=False, validation=validate_non_empty)
    sources = ListField(StringField(required=True, null=False, validation=validate_non_empty), required=True, null=False)
    shopAddress = StringField(required=True, null=False, validation=validate_non_empty)
    role_title = StringField(required=True, null=False, validation=validate_non_empty)
    role_accessTo = ListField(StringField(required=True, null=False, validation=validate_non_empty), required=True, null=False)
    name = StringField(required=True, null=False, validation=validate_non_empty)
    userPic = StringField(validation=validate_non_empty)
    businessSummaryStatus = StringField(required=True, null=False, validation=validate_non_empty)
    businessSummary_businessURL = URLField(validation=validate_non_empty)
    businessSummary_businessName = StringField(validation=validate_non_empty)
    businessSummary_businessAddress = StringField(validation=validate_non_empty)
    businessSummary_businessMobile = ListField(StringField(required=True, null=False, validation=validate_non_empty), required=True, null=False)
    businessSummary_businessEmail = StringField(validation=validate_non_empty)
    businessSummary_businessDescription = StringField(validation=validate_non_empty)
    orderTypes_showName = StringField(required=True, null=False, validation=validate_non_empty)
    orderTypes_properties = ListField(StringField(required=True, null=False, validation=validate_non_empty), required=True, null=False) 
    
 
    
# Define PaymentMaster document
class PaymentSlab(EmbeddedDocument):
    slabName = StringField(required=True, validation=validate_non_empty)
    slabValue = StringField(required=True,validation=validate_non_empty)

# BankDetails
class BankDetails(EmbeddedDocument):
    bankName = StringField(required=True,null=False,validation=validate_non_empty)
    branch = StringField(validation=validate_non_empty)
    accountType = StringField(validation=validate_non_empty)
    accountNumber = StringField(validation=validate_non_empty)
    ifscCode = StringField(validation=validate_non_empty)
    otherField = StringField(validation=validate_non_empty)

# PaymentModeDetails
class PaymentModeDetails(EmbeddedDocument):
    modeName = StringField(required=True,validation=validate_non_empty)
    cardType = StringField(validation=validate_non_empty)
    issuer = StringField(validation=validate_non_empty)
    cardNumber = StringField(validation=validate_non_empty)
    expiryDate = StringField(validation=validate_non_empty)
    cvv = StringField(validation=validate_non_empty)
    otherField = StringField(validation=validate_non_empty)

# PaymentMaster
class PaymentMaster(Document):
    taxSlab_showName = StringField(required=True,validation=validate_non_empty)
    taxSlab_properties = ListField(EmbeddedDocumentField(PaymentSlab))

    banks_showName = StringField(required=True, validation=validate_non_empty)
    banks_properties = ListField(EmbeddedDocumentField(BankDetails))

    paymentModes_showName = StringField(required=True,validation=validate_non_empty)
    paymentModes_properties = ListField(EmbeddedDocumentField(PaymentModeDetails))
    
    
    
    
class InvoiceItem(EmbeddedDocument):
    itemName = StringField(required=True, validation=validate_non_empty)
    quantity = IntField(required=True)
    price = FloatField(required=True, validation=validate_non_empty)
    total = FloatField(required=True, validation=validate_non_empty)

class Invoice(Document):
    billId = StringField(required=True, validation=validate_non_empty)
    customer = StringField(required=True, validation=validate_non_empty)
    billDate = StringField(required=True, validation=validate_non_empty)
    items = ListField(EmbeddedDocumentField(InvoiceItem), required=True)  # Corrected the field definition
    savings = FloatField(required=True, validation=validate_non_empty)
    status = StringField(required=True, validation=validate_non_empty)
    count = IntField(required=True, validation=validate_non_empty)
    orderType = StringField(required=True, validation=validate_non_empty)
    taxedAmount = FloatField(required=True, validation=validate_non_empty)
    taxedP = FloatField(required=True, validation=validate_non_empty)
    discountedAmount = FloatField(required=True, validation=validate_non_empty)
    discountedP = FloatField(required=True, validation=validate_non_empty)
    grandTotal = FloatField(required=True, validation=validate_non_empty)
    credit = FloatField(required=True, validation=validate_non_empty)
    paidAmount = FloatField(required=True, validation=validate_non_empty)
    returnedAmount = FloatField(required=True, validation=validate_non_empty)
    paidIn = FloatField(required=True, validation=validate_non_empty)
    paymentMode = StringField(required=True, validation=validate_non_empty)
    remarks = StringField(required=True, validation=validate_non_empty)