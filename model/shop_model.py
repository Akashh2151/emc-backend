
from pymongo import MongoClient





# MongoDB Configuration
client = MongoClient("mongodb+srv://akashh2151:aOSefZ94SgQEkzmg@cluster0.25xmos0.mongodb.net/?retryWrites=true&w=majority")
# client = MongoClient("mongodb://localhost:27017")


db = client["emc_project"]
shop_collection = db["shop"]
general_master_collection = db["general_master"]
shop_masters_collection = db["shop_masters"]
shop_item_master_collection = db["shop_item_master"]
shop_payment_master = db["shop_payment_master"]
shop_invoices = db["shop_invoices"]
