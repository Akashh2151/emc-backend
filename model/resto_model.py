from pymongo import MongoClient





# MongoDB Configuration
client = MongoClient("mongodb+srv://akashh2151:aOSefZ94SgQEkzmg@cluster0.25xmos0.mongodb.net/?retryWrites=true&w=majority")
# client = MongoClient("mongodb://localhost:27017")


db = client["emc_project"]
resto_collection = db["resto"]
general_master_collection = db["general_master"]
# resto_masters_collection = db["resto_masters"]
# resto_item_master_collection = db["resto_item_master"]
# resto_payment_master = db["resto_payment_master"]
# resto_invoices = db["resto_invoices"]