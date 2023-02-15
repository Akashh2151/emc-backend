import json
from flask import Blueprint, request, jsonify
# from pymongo import MongoClient
from bson.objectid import ObjectId
from model.shop_model import shop_collection,shop_invoices,shop_item_master_collection,shop_masters_collection,shop_payment_master,general_master_collection

# shopapp blue print
shopapp=Blueprint('shopapp',__name__)


# __________________________________-shop-__________________________________

@shopapp.route('/api/shop/create', methods=['POST'])
def create_shop():
    data = request.get_json()
    result = shop_collection.insert_one(data)
    return jsonify({"message": "Shop created successfully", "shop_id": str(result.inserted_id)})



@shopapp.route('/api/shop/<shop_id>', methods=['GET'])
def get_shop(shop_id):
    shop = shop_collection.find_one({"_id": ObjectId(shop_id)})
    if shop:
        # Convert the ObjectId to a string
        shop["_id"] = str(shop["_id"])
        return jsonify(shop)
    else:
        return jsonify({"message": "Shop not found"}, 404)


@shopapp.route('/api/shop/update/<shop_id>', methods=['PUT'])
def update_shop(shop_id):
    data = request.get_json()
    try:
        if data:
            # Exclude the '_id' field from the update
            data.pop('_id', None)

            result = shop_collection.update_one({"_id": ObjectId(shop_id)}, {"$set": data})
            if result.modified_count > 0:
                return jsonify({"message": "Shop updated successfully"})
            else:
                return jsonify({"message": "Shop not found or no changes made"}, 404)
        else:
            return jsonify({"error": "Invalid JSON data"}, 400)
    except Exception as e:
        return jsonify({"error": str(e)}, 500)





@shopapp.route('/api/shop/delete/<shop_id>', methods=['DELETE'])
def delete_shop(shop_id):
    result = shop_collection.delete_one({"_id": ObjectId(shop_id)})
    if result.deleted_count > 0:
        return jsonify({"message": "Shop deleted successfully"})
    else:
        return jsonify({"message": "Shop not found"}, 404)
# # __________________________________-shop End-__________________________________



# # __________________________________-ShopMasters-__________________________________

@shopapp.route('/api/shopmasters/create', methods=['POST'])
def create_shop_master():
    data = request.get_json()
    result = shop_masters_collection.insert_one(data)
    return jsonify({"message": "ShopMaster created successfully", "shop_master_id": str(result.inserted_id)})

@shopapp.route('/api/shopmasters/<shop_master_id>', methods=['GET'])
def get_shop_master(shop_master_id):
    shop_master = shop_masters_collection.find_one({"_id": ObjectId(shop_master_id)})
    if shop_master:
        shop_master["_id"] = str(shop_master["_id"])
        return jsonify(shop_master)
    else:
        return jsonify({"message": "ShopMaster not found"}, 404)

@shopapp.route('/api/shopmasters/update/<shop_master_id>', methods=['PUT'])
def update_shop_master(shop_master_id):
    data = request.get_json()
    try:
        if data:
            # Exclude the '_id' field from the update
            data.pop('_id', None)

            result = shop_masters_collection.update_one({"_id": ObjectId(shop_master_id)}, {"$set": data})
            if result.modified_count > 0:
                return jsonify({"message": "ShopMaster updated successfully"})
            else:
                return jsonify({"message": "ShopMaster not found or no changes made"}, 404)
        else:
            return jsonify({"error": "Invalid JSON data"}, 400)
    except Exception as e:
        return jsonify({"error": str(e)}, 500)



@shopapp.route('/api/shopmasters/delete/<shop_master_id>', methods=['DELETE'])
def delete_shop_master(shop_master_id):
    result = shop_masters_collection.delete_one({"_id": ObjectId(shop_master_id)})
    if result.deleted_count > 0:
        return jsonify({"message": "ShopMaster deleted successfully"})
    else:
        return jsonify({"message": "ShopMaster not found"}, 404)

# # __________________________________-ShopMasters End-__________________________________




# # __________________________________-GeneralMaster-__________________________________

@shopapp.route('/api/generalmaster/create', methods=['POST'])
def create_general_master():
    data = request.get_json()
    result = general_master_collection.insert_one(data)
    return jsonify({"message": "GeneralMaster created successfully", "general_master_id": str(result.inserted_id)})

@shopapp.route('/api/generalmaster/<general_master_id>', methods=['GET'])
def get_general_master(general_master_id):
    general_master = general_master_collection.find_one({"_id": ObjectId(general_master_id)})
    if general_master:
        general_master["_id"] = str(general_master["_id"])
        return jsonify(general_master)
    else:
        return jsonify({"message": "GeneralMaster not found"}, 404)

@shopapp.route('/api/generalmaster/update/<general_master_id>', methods=['PUT'])
def update_general_master(general_master_id):
    data = request.get_json()
    try:
        if data:
            # Exclude the '_id' field from the update
            data.pop('_id', None)

            result = general_master_collection.update_one({"_id": ObjectId(general_master_id)}, {"$set": data})
            if result.modified_count > 0:
                return jsonify({"message": "GeneralMaster updated successfully"})
            else:
                return jsonify({"message": "GeneralMaster not found or no changes made"}, 404)
        else:
            return jsonify({"error": "Invalid JSON data"}, 400)
    except Exception as e:
        return jsonify({"error": str(e)}, 500)


@shopapp.route('/api/generalmaster/delete/<general_master_id>', methods=['DELETE'])
def delete_general_master(general_master_id):
    result = general_master_collection.delete_one({"_id": ObjectId(general_master_id)})
    if result.deleted_count > 0:
        return jsonify({"message": "GeneralMaster deleted successfully"})
    else:
        return jsonify({"message": "GeneralMaster not found"}, 404)

# # __________________________________-GeneralMaster End-__________________________________




# # __________________________________-ShopItemMaster -__________________________________

 # Create ShopItemMaster
@shopapp.route('/api/shopitemmaster/create', methods=['POST'])
def create_shop_item_master():
    data = request.get_json()
    try:
        if data:
            result = shop_item_master_collection.insert_one(data)
            return jsonify({"message": "ShopItemMaster created successfully", "shop_item_master_id": str(result.inserted_id)})
        else:
            return jsonify({"error": "Invalid JSON data"}, 400)
    except Exception as e:
        return jsonify({"error": str(e)}, 500)

# Get ShopItemMaster Details
@shopapp.route('/api/shopitemmaster/<shop_item_master_id>', methods=['GET'])
def get_shop_item_master(shop_item_master_id):
    try:
        shop_item_master = shop_item_master_collection.find_one({"_id": ObjectId(shop_item_master_id)})
        if shop_item_master:
            shop_item_master["_id"] = str(shop_item_master["_id"])
            return jsonify(shop_item_master)
        else:
            return jsonify({"message": "ShopItemMaster not found"}, 404)
    except Exception as e:
        return jsonify({"error": str(e)}, 500)

# Update ShopItemMaster Details
@shopapp.route('/api/shopitemmaster/update/<shop_item_master_id>', methods=['PUT'])
def update_shop_item_master(shop_item_master_id):
    data = request.get_json()
    try:
        if data:
            # Exclude _id from the update data
            data.pop('_id', None)
            result = shop_item_master_collection.update_one({"_id": ObjectId(shop_item_master_id)}, {"$set": data})
            if result.modified_count > 0:
                return jsonify({"message": "ShopItemMaster updated successfully"})
            else:
                return jsonify({"message": "ShopItemMaster not found or no changes made"}, 404)
        else:
            return jsonify({"error": "Invalid JSON data"}, 400)
    except Exception as e:
        return jsonify({"error": str(e)}, 500)
    

# Delete ShopItemMaster
@shopapp.route('/api/shopitemmaster/delete/<shop_item_master_id>', methods=['DELETE'])
def delete_shop_item_master(shop_item_master_id):
    try:
        result = shop_item_master_collection.delete_one({"_id": ObjectId(shop_item_master_id)})
        if result.deleted_count > 0:
            return jsonify({"message": "ShopItemMaster deleted successfully"})
        else:
            return jsonify({"message": "ShopItemMaster not found"}, 404)
    except Exception as e:
        return jsonify({"error": str(e)}, 500)

# # __________________________________-ShopItemMaster End-__________________________________


# # __________________________________-ShopPaymentMaster-__________________________________

# Create ShopPaymentMaster
# @shopapp.route('/api/shoppaymentmaster/create', methods=['POST'])
# def create_shop_payment_master():
#     data = request.get_json()
#     try:
#         if data:
#             result = shop_payment_master.insert_one(data)
#             return jsonify({"message": "ShopPaymentMaster created successfully", "payment_master_id": str(result.inserted_id)})
#         else:
#             return jsonify({"error": "Invalid JSON data"}, 400)
#     except Exception as e:
#         return jsonify({"error": str(e)}, 500)

# Get ShopPaymentMaster Details
# @shopapp.route('/api/shoppaymentmaster/<payment_master_id>', methods=['GET'])
# def get_shop_payment_master(payment_master_id):
#     try:
#         payment_master = shop_payment_master.find_one({"_id": ObjectId(payment_master_id)})
#         if payment_master:
#             payment_master["_id"] = str(payment_master["_id"])
#             return jsonify(payment_master)
#         else:
#             return jsonify({"message": "ShopPaymentMaster not found"}, 404)
#     except Exception as e:
#         return jsonify({"error": str(e)}, 500)

# Update ShopPaymentMaster Details
# @shopapp.route('/api/shoppaymentmaster/update/<payment_master_id>', methods=['PUT'])
# def update_shop_payment_master(payment_master_id):
#     data = request.get_json()
#     try:
#         if data:
#             # Exclude the '_id' field from the update
#             data.pop('_id', None)

#             result = shop_payment_master.update_one({"_id": ObjectId(payment_master_id)}, {"$set": data})
#             if result.modified_count > 0:
#                 return jsonify({"message": "ShopPaymentMaster updated successfully"})
#             else:
#                 return jsonify({"message": "ShopPaymentMaster not found or no changes made"}, 404)
#         else:
#             return jsonify({"error": "Invalid JSON data"}, 400)
#     except Exception as e:
#         return jsonify({"error": str(e)}, 500)


# Delete ShopPaymentMaster
# @shopapp.route('/api/shoppaymentmaster/delete/<payment_master_id>', methods=['DELETE'])
# def delete_shop_payment_master(payment_master_id):
#     try:
#         result = shop_payment_master.delete_one({"_id": ObjectId(payment_master_id)})
#         if result.deleted_count > 0:
#             return jsonify({"message": "ShopPaymentMaster deleted successfully"})
#         else:
#             return jsonify({"message": "ShopPaymentMaster not found"}, 404)
#     except Exception as e:
#         return jsonify({"error": str(e)}, 500)
 

# # __________________________________-ShopPaymentMaster End-__________________________________



# # __________________________________-ShopInvoices __________________________________
# Create ShopInvoice
# @shopapp.route('/api/shopinvoices/create', methods=['POST'])
# def create_shop_invoice():
#     data = request.get_json()
#     try:
#         if data:
#             result = shop_invoices.insert_one(data)
#             return jsonify({"message": "ShopInvoice created successfully", "invoice_id": str(result.inserted_id)})
#         else:
#             return jsonify({"error": "Invalid JSON data"}, 400)
#     except Exception as e:
#         return jsonify({"error": str(e)}, 500)

# Get ShopInvoice Details
# @shopapp.route('/api/shopinvoices/<invoice_id>', methods=['GET'])
# def get_shop_invoice(invoice_id):
#     try:
#         invoice = shop_invoices.find_one({"_id": ObjectId(invoice_id)})
#         if invoice:
#             invoice["_id"] = str(invoice["_id"])
#             return jsonify(invoice)
#         else:
#             return jsonify({"message": "ShopInvoice not found"}, 404)
#     except Exception as e:
#         return jsonify({"error": str(e)}, 500)

# Update ShopInvoice Details
# @shopapp.route('/api/shopinvoices/update/<invoice_id>', methods=['PUT'])
# def update_shop_invoice(invoice_id):
#     data = request.get_json()
#     try:
#         if data:
#             # Exclude the '_id' field from the update
#             data.pop('_id', None)

#             result = shop_invoices.update_one({"_id": ObjectId(invoice_id)}, {"$set": data})
#             if result.modified_count > 0:
#                 return jsonify({"message": "ShopInvoice updated successfully"})
#             else:
#                 return jsonify({"message": "ShopInvoice not found or no changes made"}, 404)
#         else:
#             return jsonify({"error": "Invalid JSON data"}, 400)
#     except Exception as e:
#         return jsonify({"error": str(e)}, 500)


# Delete ShopInvoice
# @shopapp.route('/api/shopinvoices/delete/<invoice_id>', methods=['DELETE'])
# def delete_shop_invoice(invoice_id):
#     try:
#         result = shop_invoices.delete_one({"_id": ObjectId(invoice_id)})
#         if result.deleted_count > 0:
#             return jsonify({"message": "ShopInvoice deleted successfully"})
#         else:
#             return jsonify({"message": "ShopInvoice not found"}, 404)
#     except Exception as e:
#         return jsonify({"error": str(e)}, 500)

# # __________________________________-ShopInvoices End-__________________________________



 