import json
from flask import Blueprint, request, jsonify
# from pymongo import MongoClient
from bson.objectid import ObjectId
from model.resto_model import resto_collection,resto_invoices,resto_item_master_collection,resto_masters_collection,resto_payment_master,general_master_collection

# restoapp blue print
restoapp=Blueprint('restoapp',__name__)


# ___________-resto-___________

@restoapp.route('/api/resto/create', methods=['POST'])
def create_resto():
    data = request.get_json()
    result = resto_collection.insert_one(data)
    return jsonify({"message": "Resto created successfully", "resto_id": str(result.inserted_id)})



@restoapp.route('/api/resto/<resto_id>', methods=['GET'])
def get_resto(resto_id):
    resto = resto_collection.find_one({"_id": ObjectId(resto_id)})
    if resto:
        # Convert the ObjectId to a string
        resto["_id"] = str(resto["_id"])
        return jsonify(resto)
    else:
        return jsonify({"message": "Resto not found"}, 404)


# @restoapp.route('/api/resto/update/<resto_id>', methods=['PUT'])
# def update_resto(resto_id):
#     data = request.get_json()
#     try:
#         if data:
#             # Exclude the '_id' field from the update
#             data.pop('_id', None)

#             result = resto_collection.update_one({"_id": ObjectId(resto_id)}, {"$set": data})
#             if result.modified_count > 0:
#                 return jsonify({"message": "Resto updated successfully"})
#             else:
#                 return jsonify({"message": "Resto not found or no changes made"}, 404)
#         else:
#             return jsonify({"error": "Invalid JSON data"}, 400)
#     except Exception as e:
#         return jsonify({"error": str(e)}, 500)





# @restoapp.route('/api/resto/delete/<resto_id>', methods=['DELETE'])
# def delete_resto(resto_id):
#     result = resto_collection.delete_one({"_id": ObjectId(resto_id)})
#     if result.deleted_count > 0:
#         return jsonify({"message": "Resto deleted successfully"})
#     else:
#         return jsonify({"message": "Resto not found"}, 404)
# # ___________-Resto End-___________



# # ___________-RestoMasters-___________

# @restoapp.route('/api/restomasters/create', methods=['POST'])
# def create_resto_master():
#     data = request.get_json()
#     result = resto_masters_collection.insert_one(data)
#     return jsonify({"message": "RestoMaster created successfully", "resto_master_id": str(result.inserted_id)})

# @restoapp.route('/api/shopmasters/<resto_master_id>', methods=['GET'])
# def get_resto_master(resto_master_id):
#     resto_master = resto_masters_collection.find_one({"_id": ObjectId(resto_master_id)})
#     if resto_master:
#         resto_master["_id"] = str(resto_master["_id"])
#         return jsonify(resto_master)
#     else:
#         return jsonify({"message": "RestoMaster not found"}, 404)

# @restoapp.route('/api/restomasters/update/<resto_master_id>', methods=['PUT'])
# def update_resto_master(resto_master_id):
#     data = request.get_json()
#     try:
#         if data:
#             # Exclude the '_id' field from the update
#             data.pop('_id', None)

#             result = resto_masters_collection.update_one({"_id": ObjectId(resto_master_id)}, {"$set": data})
#             if result.modified_count > 0:
#                 return jsonify({"message": "RestoMaster updated successfully"})
#             else:
#                 return jsonify({"message": "RestoMaster not found or no changes made"}, 404)
#         else:
#             return jsonify({"error": "Invalid JSON data"}, 400)
#     except Exception as e:
#         return jsonify({"error": str(e)}, 500)



# @restoapp.route('/api/shopmasters/delete/<resto_master_id>', methods=['DELETE'])
# def delete_resto_master(resto_master_id):
#     result = resto_masters_collection.delete_one({"_id": ObjectId(resto_master_id)})
#     if result.deleted_count > 0:
#         return jsonify({"message": "RestoMaster deleted successfully"})
#     else:
#         return jsonify({"message": "RestoMaster not found"}, 404)

# # ___________-RestoMasters End-___________




# # ___________-GeneralMaster-___________

# @restoapp.route('/api/generalmaster/create', methods=['POST'])
# def create_general_master():
#     data = request.get_json()
#     result = general_master_collection.insert_one(data)
#     return jsonify({"message": "GeneralMaster created successfully", "general_master_id": str(result.inserted_id)})

# @restoapp.route('/api/generalmaster/<general_master_id>', methods=['GET'])
# def get_general_master(general_master_id):
#     general_master = general_master_collection.find_one({"_id": ObjectId(general_master_id)})
#     if general_master:
#         general_master["_id"] = str(general_master["_id"])
#         return jsonify(general_master)
#     else:
#         return jsonify({"message": "GeneralMaster not found"}, 404)

# @restoapp.route('/api/generalmaster/update/<general_master_id>', methods=['PUT'])
# def update_general_master(general_master_id):
#     data = request.get_json()
#     try:
#         if data:
#             # Exclude the '_id' field from the update
#             data.pop('_id', None)

#             result = general_master_collection.update_one({"_id": ObjectId(general_master_id)}, {"$set": data})
#             if result.modified_count > 0:
#                 return jsonify({"message": "GeneralMaster updated successfully"})
#             else:
#                 return jsonify({"message": "GeneralMaster not found or no changes made"}, 404)
#         else:
#             return jsonify({"error": "Invalid JSON data"}, 400)
#     except Exception as e:
#         return jsonify({"error": str(e)}, 500)


# @restoapp.route('/api/generalmaster/delete/<general_master_id>', methods=['DELETE'])
# def delete_general_master(general_master_id):
#     result = general_master_collection.delete_one({"_id": ObjectId(general_master_id)})
#     if result.deleted_count > 0:
#         return jsonify({"message": "GeneralMaster deleted successfully"})
#     else:
#         return jsonify({"message": "GeneralMaster not found"}, 404)

# # ___________-GeneralMaster End-___________




# # ___________-RestoItemMaster -___________

#  # Create RestoItemMaster
# @restoapp.route('/api/restoitemmaster/create', methods=['POST'])
# def create_resto_item_master():
#     data = request.get_json()
#     try:
#         if data:
#             result = resto_item_master_collection.insert_one(data)
#             return jsonify({"message": "RestoItemMaster created successfully", "resto_item_master_id": str(result.inserted_id)})
#         else:
#             return jsonify({"error": "Invalid JSON data"}, 400)
#     except Exception as e:
#         return jsonify({"error": str(e)}, 500)

# # Get RestoItemMaster Details
# @restoapp.route('/api/restoitemmaster/<resto_item_master_id>', methods=['GET'])
# def get_resto_item_master(resto_item_master_id):
#     try:
#         resto_item_master = resto_item_master_collection.find_one({"_id": ObjectId(resto_item_master_id)})
#         if resto_item_master:
#             resto_item_master["_id"] = str(resto_item_master["_id"])
#             return jsonify(resto_item_master)
#         else:
#             return jsonify({"message": "RestoItemMaster not found"}, 404)
#     except Exception as e:
#         return jsonify({"error": str(e)}, 500)

# # Update RestoItemMaster Details
# @restoapp.route('/api/restoitemmaster/update/<resto_item_master_id>', methods=['PUT'])
# def update_resto_item_master(resto_item_master_id):
#     data = request.get_json()
#     try:
#         if data:
#             # Exclude _id from the update data
#             data.pop('_id', None)
#             result = resto_item_master_collection.update_one({"_id": ObjectId(resto_item_master_id)}, {"$set": data})
#             if result.modified_count > 0:
#                 return jsonify({"message": "RestoItemMaster updated successfully"})
#             else:
#                 return jsonify({"message": "RestoItemMaster not found or no changes made"}, 404)
#         else:
#             return jsonify({"error": "Invalid JSON data"}, 400)
#     except Exception as e:
#         return jsonify({"error": str(e)}, 500)
    

# # Delete RestoItemMaster
# @restoapp.route('/api/restoitemmaster/delete/<resto_item_master_id>', methods=['DELETE'])
# def delete_resto_item_master(resto_item_master_id):
#     try:
#         result = resto_item_master_collection.delete_one({"_id": ObjectId(resto_item_master_id)})
#         if result.deleted_count > 0:
#             return jsonify({"message": "RestoItemMaster deleted successfully"})
#         else:
#             return jsonify({"message": "RestoItemMaster not found"}, 404)
#     except Exception as e:
#         return jsonify({"error": str(e)}, 500)

# # ___________-RestoItemMaster End-___________


# # ___________-RestoPaymentMaster-___________

# # Create RestoPaymentMaster
# @restoapp.route('/api/restopaymentmaster/create', methods=['POST'])
# def create_resto_payment_master():
#     data = request.get_json()
#     try:
#         if data:
#             result = resto_payment_master.insert_one(data)
#             return jsonify({"message": "RestoPaymentMaster created successfully", "payment_master_id": str(result.inserted_id)})
#         else:
#             return jsonify({"error": "Invalid JSON data"}, 400)
#     except Exception as e:
#         return jsonify({"error": str(e)}, 500)

# # Get RestoPaymentMaster Details
# @restoapp.route('/api/restopaymentmaster/<payment_master_id>', methods=['GET'])
# def get_resto_payment_master(payment_master_id):
#     try:
#         payment_master = resto_payment_master.find_one({"_id": ObjectId(payment_master_id)})
#         if payment_master:
#             payment_master["_id"] = str(payment_master["_id"])
#             return jsonify(payment_master)
#         else:
#             return jsonify({"message": "RestoPaymentMaster not found"}, 404)
#     except Exception as e:
#         return jsonify({"error": str(e)}, 500)

# # Update RestoPaymentMaster Details
# @restoapp.route('/api/restopaymentmaster/update/<payment_master_id>', methods=['PUT'])
# def update_resto_payment_master(payment_master_id):
#     data = request.get_json()
#     try:
#         if data:
#             # Exclude the '_id' field from the update
#             data.pop('_id', None)

#             result = resto_payment_master.update_one({"_id": ObjectId(payment_master_id)}, {"$set": data})
#             if result.modified_count > 0:
#                 return jsonify({"message": "RestoPaymentMaster updated successfully"})
#             else:
#                 return jsonify({"message": "RestoPaymentMaster not found or no changes made"}, 404)
#         else:
#             return jsonify({"error": "Invalid JSON data"}, 400)
#     except Exception as e:
#         return jsonify({"error": str(e)}, 500)


# # Delete RestoPaymentMaster
# @restoapp.route('/api/restopaymentmaster/delete/<payment_master_id>', methods=['DELETE'])
# def delete_resto_payment_master(payment_master_id):
#     try:
#         result = resto_payment_master.delete_one({"_id": ObjectId(payment_master_id)})
#         if result.deleted_count > 0:
#             return jsonify({"message": "RestoPaymentMaster deleted successfully"})
#         else:
#             return jsonify({"message": "RestoPaymentMaster not found"}, 404)
#     except Exception as e:
#         return jsonify({"error": str(e)}, 500)
 

# # ___________-RestoPaymentMaster End-___________



# # ___________-RestoInvoices _____________
# # Create RestoInvoice
# @restoapp.route('/api/restoinvoices/create', methods=['POST'])
# def create_resto_invoice():
#     data = request.get_json()
#     try:
#         if data:
#             result = resto_invoices.insert_one(data)
#             return jsonify({"message": "RestoInvoice created successfully", "invoice_id": str(result.inserted_id)})
#         else:
#             return jsonify({"error": "Invalid JSON data"}, 400)
#     except Exception as e:
#         return jsonify({"error": str(e)}, 500)

# # Get RestoInvoice Details
# @restoapp.route('/api/restoinvoices/<invoice_id>', methods=['GET'])
# def get_resto_invoice(invoice_id):
#     try:
#         invoice = resto_invoices.find_one({"_id": ObjectId(invoice_id)})
#         if invoice:
#             invoice["_id"] = str(invoice["_id"])
#             return jsonify(invoice)
#         else:
#             return jsonify({"message": "RestoInvoice not found"}, 404)
#     except Exception as e:
#         return jsonify({"error": str(e)}, 500)

# # Update RestoInvoice Details
# @restoapp.route('/api/restoinvoices/update/<invoice_id>', methods=['PUT'])
# def update_resto_invoice(invoice_id):
#     data = request.get_json()
#     try:
#         if data:
#             # Exclude the '_id' field from the update
#             data.pop('_id', None)

#             result = resto_invoices.update_one({"_id": ObjectId(invoice_id)}, {"$set": data})
#             if result.modified_count > 0:
#                 return jsonify({"message": "RestoInvoice updated successfully"})
#             else:
#                 return jsonify({"message": "RestoInvoice not found or no changes made"}, 404)
#         else:
#             return jsonify({"error": "Invalid JSON data"}, 400)
#     except Exception as e:
#         return jsonify({"error": str(e)}, 500)


# # Delete RestoInvoice
# @restoapp.route('/api/restopinvoices/delete/<invoice_id>', methods=['DELETE'])
# def delete_resto_invoice(invoice_id):
#     try:
#         result = resto_invoices.delete_one({"_id": ObjectId(invoice_id)})
#         if result.deleted_count > 0:
#             return jsonify({"message": "RestoInvoice deleted successfully"})
#         else:
#             return jsonify({"message": "RestoInvoice not found"}, 404)
#     except Exception as e:
#         return jsonify({"error": str(e)}, 500)

# # ___________-RestoInvoices End-___________