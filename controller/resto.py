import json
from bson import InvalidDocument
from flask import Blueprint, request, jsonify
# from pymongo import MongoClient
from bson.objectid import ObjectId
from pydantic import ValidationError
from model.resto_model import BillId, BusinessSummary, GeneralMaster, OrderTypes, RestoSellMaster, Role, resto_collection,resto_invoices,resto_item_master_collection,resto_masters_collection,resto_payment_master,general_master_collection
from model.shop_model import MenuMaster

# restoapp blue print
restoapp=Blueprint('restoapp',__name__)





# _______________________________________________________________________________________________________________________________________
# CREATE
@restoapp.route('/api/menumasters/create', methods=['POST'])
def create_menumaster():
    try:
        data = request.json
        showName = data.get('showName')
        path = data.get('path')
        subMenu = data.get('subMenu')  # Include the new field

        if not all([showName, path, subMenu]):
            return jsonify({'error': 'All fields are required', 'status_code': 400}), 400

        existing_menumaster = MenuMaster.objects(showName=showName).first()
        if existing_menumaster:
            return jsonify({'error': 'MenuMaster with the same showName already exists', 'status_code': 400}), 400

        menumaster = MenuMaster(showName=showName, path=path, subMenu=subMenu)
        menumaster.save()

        response = {"Body": None, "status": "success", "statusCode": 200, "message": 'MenuMaster created'}
        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e), 'status_code': 500}), 500


# UPDATE
@restoapp.route('/api/menumasters/update/<string:menumaster_id>', methods=['PUT'])
def update_menumaster(menumaster_id):
    try:
        object_id = ObjectId(menumaster_id)
        menumaster = MenuMaster.objects(id=object_id).first()

        if not menumaster:
            return jsonify({'error': 'MenuMaster not found', 'status_code': 404}), 404

        data = request.json

        # Validate that at least one field is present in the request
        if not any(field in data for field in ['showName', 'path', 'subMenu']):
            return jsonify({'error': 'At least one field (showName, path, or subMenu) is required', 'status_code': 400}), 400

        # Update each field individually, filtering out null values
        for key, value in data.items():
            if value is not None:
                setattr(menumaster, key, value)

        menumaster.save()

        response = {"Body": None, "status": "success", "statusCode": 200, "message": 'MenuMaster updated'}
        return jsonify(response)

    except (ValidationError, InvalidDocument) as e:
        return jsonify({'error': str(e), 'status_code': 400}), 400
    except Exception as e:
        return jsonify({'error': str(e), 'status_code': 500}), 500


# READ
@restoapp.route('/api/menumasters/<string:menumaster_id>', methods=['GET'])
def get_menumaster(menumaster_id):
    try:
        object_id = ObjectId(menumaster_id)
        menumaster = MenuMaster.objects(id=object_id).first()

        if menumaster:
            response = {
                "id": str(menumaster.id),
                "showName": menumaster.showName,
                "path": menumaster.path,
                "subMenu": menumaster.subMenu  # Include the new field
            }
            return jsonify({"status_code": 200, "message": "Success", "data": response}), 200
        else:
            return jsonify({'error': 'MenuMaster not found', 'status_code': 404}), 404

    except Exception as e:
        return jsonify({'error': str(e), 'status_code': 500}), 500



# DELETE
@restoapp.route('/api/menumasters/delete/<string:menumaster_id>', methods=['DELETE'])
def delete_menumaster(menumaster_id):
    try:
        object_id = ObjectId(menumaster_id)
        menumaster = MenuMaster.objects(id=object_id).first()

        if menumaster:
            menumaster.delete()
            response = {"Body": None, "status": "success", "statusCode": 200, "message": 'MenuMaster deleted'}
            return jsonify(response)
        else:
            return jsonify({'error': 'MenuMaster not found', 'status_code': 404}), 404

    except Exception as e:
        return jsonify({'error': str(e), 'status_code': 500}), 500

# _______________________________________________________________________________________________________________________________________
# CREATE
@restoapp.route('/api/sellmasters/create', methods=['POST'])
def create_sellmaster():
    try:
        data = request.json
        showName = data.get('showName')
        status = data.get('status')
        sellUnits = data.get('sellUnits')
        printers = data.get('printers')
        sellType = data.get('sellType')

        if not all([showName, status, sellUnits, printers, sellType]):
            return jsonify({'error': 'All fields are required', 'status_code': 400}), 400

        existing_sellmaster = RestoSellMaster.objects(showName=showName).first()
        if existing_sellmaster:
            return jsonify({'error': 'SellMaster with the same showName already exists', 'status_code': 400}), 400

        sellmaster = RestoSellMaster(showName=showName, status=status, sellUnits=sellUnits, printers=printers, sellType=sellType)
        sellmaster.save()

        response = {"Body": None, "status": "success", "statusCode": 200, "message": 'SellMaster created'}
        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e), 'status_code': 500}), 500


# READ
@restoapp.route('/api/sellmasters/<string:sellmaster_id>', methods=['GET'])
def get_sellmaster(sellmaster_id):
    try:
        object_id = ObjectId(sellmaster_id)
        sellmaster = RestoSellMaster.objects(id=object_id).first()

        if sellmaster:
            response = {
                "id": str(sellmaster.id),
                "showName": sellmaster.showName,
                "status": sellmaster.status,
                "sellUnits": sellmaster.sellUnits,
                "printers": sellmaster.printers,
                "sellType": sellmaster.sellType
            }
            return jsonify({"status_code": 200, "message": "Success", "data": response}), 200
        else:
            return jsonify({'error': 'SellMaster not found', 'status_code': 404}), 404

    except Exception as e:
        return jsonify({'error': str(e), 'status_code': 500}), 500


# UPDATE
@restoapp.route('/api/sellmasters/update/<string:sellmaster_id>', methods=['PUT'])
def update_sellmaster(sellmaster_id):
    try:
        object_id = ObjectId(sellmaster_id)
        sellmaster = RestoSellMaster.objects(id=object_id).first()

        if not sellmaster:
            return jsonify({'error': 'SellMaster not found', 'status_code': 404}), 404

        data = request.json

        # Validate that at least one field is present in the request
        if not any(field in data for field in ['showName', 'status', 'sellUnits', 'printers', 'sellType']):
            return jsonify({'error': 'At least one field (showName, status, sellUnits, printers, or sellType) is required', 'status_code': 400}), 400

        # Update each field individually, filtering out null values
        for key, value in data.items():
            if value is not None:
                setattr(sellmaster, key, value)

        sellmaster.save()

        response = {"Body": None, "status": "success", "statusCode": 200, "message": 'SellMaster updated'}
        return jsonify(response)

    except (ValidationError, InvalidDocument) as e:
        return jsonify({'error': str(e), 'status_code': 400}), 400
    except Exception as e:
        return jsonify({'error': str(e), 'status_code': 500}), 500


# DELETE
@restoapp.route('/api/sellmasters/delete/<string:sellmaster_id>', methods=['DELETE'])
def delete_sellmaster(sellmaster_id):
    try:
        object_id = ObjectId(sellmaster_id)
        sellmaster = RestoSellMaster.objects(id=object_id).first()

        if sellmaster:
            sellmaster.delete()
            response = {"Body": None, "status": "success", "statusCode": 200, "message": 'SellMaster deleted'}
            return jsonify(response)
        else:
            return jsonify({'error': 'SellMaster not found', 'status_code': 404}), 404

    except Exception as e:
        return jsonify({'error': str(e), 'status_code': 500}), 500
    
# ___________________________________________________________________________________________________________________________________________________  
# CREATE
@restoapp.route('/api/generalmasters/create', methods=['POST'])
def create_generalmaster():
    try:
        data = request.json

        # Create embedded documents
        bill_id_data = data.get('billId', {})
        bill_id = BillId(startString=bill_id_data.get('startString'), endString=bill_id_data.get('endString'))

        role_data = data.get('role', {})
        role = Role(title=role_data.get('title'), accessTo=role_data.get('accessTo'))

        business_summary_data = data.get('businessSummary', [])
        business_summary = [BusinessSummary(**item) for item in business_summary_data]

        order_types_data = data.get('orderTypes', {})
        order_types = OrderTypes(showName=order_types_data.get('showName'), properties=order_types_data.get('properties'))

        # Create GeneralMaster document
        generalmaster = GeneralMaster(
            billId=bill_id,
            language=data.get('language'),
            theme=data.get('theme'),
            shopName=data.get('shopName'),
            sources=data.get('sources'),
            shopAddress=data.get('shopAddress'),
            role=role,
            name=data.get('name'),
            userPic=data.get('userPic'),
            businessSummaryStatus=data.get('businessSummaryStatus'),
            businessSummary=business_summary,
            orderTypes=order_types
        )
        generalmaster.save()

        response = {"Body": None, "status": "success", "statusCode": 200, "message": 'GeneralMaster created'}
        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e), 'status_code': 500}), 500


# READ
@restoapp.route('/api/generalmasters/<string:generalmaster_id>', methods=['GET'])
def get_generalmaster(generalmaster_id):
    try:
        object_id = ObjectId(generalmaster_id)
        generalmaster = GeneralMaster.objects(id=object_id).first()

        if generalmaster:
            response = {
                "id": str(generalmaster.id),
                "billId": {
                    "startString": generalmaster.billId.startString,
                    "endString": generalmaster.billId.endString
                },
                "language": generalmaster.language,
                "theme": generalmaster.theme,
                "shopName": generalmaster.shopName,
                "sources": generalmaster.sources,
                "shopAddress": generalmaster.shopAddress,
                "role": {
                    "title": generalmaster.role.title,
                    "accessTo": generalmaster.role.accessTo
                },
                "name": generalmaster.name,
                "userPic": generalmaster.userPic,
                "businessSummaryStatus": generalmaster.businessSummaryStatus,
                "businessSummary": [
                    {
                        "businessURL": item.businessURL,
                        "businessName": item.businessName,
                        "businessAddress": item.businessAddress,
                        "businessMobile": item.businessMobile,
                        "businessEmail": item.businessEmail,
                        "businessDescription": item.businessDescription
                    } for item in generalmaster.businessSummary
                ],
                "orderTypes": {
                    "showName": generalmaster.orderTypes.showName,
                    "properties": generalmaster.orderTypes.properties
                }
            }
            return jsonify({"status_code": 200, "message": "Success", "data": response}), 200
        else:
            return jsonify({'error': 'GeneralMaster not found', 'status_code': 404}), 404

    except Exception as e:
        return jsonify({'error': str(e), 'status_code': 500}), 500


# UPDATE
@restoapp.route('/api/generalmasters/update/<string:generalmaster_id>', methods=['PUT'])
def update_generalmaster(generalmaster_id):
    try:
        object_id = ObjectId(generalmaster_id)
        generalmaster = GeneralMaster.objects(id=object_id).first()

        if not generalmaster:
            return jsonify({'error': 'GeneralMaster not found', 'status_code': 404}), 404

        data = request.json

        # Validate that at least one field is present in the request
        if not any(field in data for field in ['billId', 'language', 'theme', 'shopName', 'sources', 'shopAddress', 'role', 'name', 'userPic', 'businessSummaryStatus', 'businessSummary', 'orderTypes']):
            return jsonify({'error': 'At least one field is required', 'status_code': 400}), 400

        # Update BillId
        if 'billId' in data:
            bill_id_data = data['billId']
            generalmaster.billId.startString = bill_id_data.get('startString', generalmaster.billId.startString)
            generalmaster.billId.endString = bill_id_data.get('endString', generalmaster.billId.endString)

        # Update Role
        if 'role' in data:
            role_data = data['role']
            generalmaster.role.title = role_data.get('title', generalmaster.role.title)
            generalmaster.role.accessTo = role_data.get('accessTo', generalmaster.role.accessTo)

        # Update BusinessSummary
        if 'businessSummary' in data:
            business_summary_data = data['businessSummary']
            generalmaster.businessSummary = [BusinessSummary(**item) for item in business_summary_data]

        # Update OrderTypes
        if 'orderTypes' in data:
            order_types_data = data['orderTypes']
            generalmaster.orderTypes.showName = order_types_data.get('showName', generalmaster.orderTypes.showName)
            generalmaster.orderTypes.properties = order_types_data.get('properties', generalmaster.orderTypes.properties)

        # Update other fields
        for key, value in data.items():
            if key not in ['billId', 'role', 'businessSummary', 'orderTypes']:
                setattr(generalmaster, key, value)

        generalmaster.save()

        response = {"Body": None, "status": "success", "statusCode": 200, "message": 'GeneralMaster updated'}
        return jsonify(response)

    except (ValidationError, InvalidDocument) as e:
        return jsonify({'error': str(e),})
    
# DELETE
@restoapp.route('/api/generalmasters/delete/<string:generalmaster_id>', methods=['DELETE'])
def delete_generalmaster(generalmaster_id):
    try:
        object_id = ObjectId(generalmaster_id)
        generalmaster = GeneralMaster.objects(id=object_id).first()

        if generalmaster:
            generalmaster.delete()
            response = {"Body": None, "status": "success", "statusCode": 200, "message": 'GeneralMaster deleted'}
            return jsonify(response)
        else:
            return jsonify({'error': 'GeneralMaster not found', 'status_code': 404}), 404

    except Exception as e:
        return jsonify({'error': str(e), 'status_code': 500}), 500
    
    
    
# @restoapp.route('/api/resto/create', methods=['POST'])
# def create_resto():
#     data = request.get_json()
#     result = resto_collection.insert_one(data)
#     return jsonify({"message": "Resto created successfully", "resto_id": str(result.inserted_id)})



# @restoapp.route('/api/resto/<resto_id>', methods=['GET'])
# def get_resto(resto_id):
#     resto = resto_collection.find_one({"_id": ObjectId(resto_id)})
#     if resto:
#         # Convert the ObjectId to a string
#         resto["_id"] = str(resto["_id"])
#         return jsonify(resto)
#     else:
#         return jsonify({"message": "Resto not found"}, 404)


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

# # # ___________-GeneralMaster End-___________




# # # ___________-RestoItemMaster -___________

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

# # # ___________-RestoItemMaster End-___________


# # # ___________-RestoPaymentMaster-___________

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

# # # Update RestoPaymentMaster Details
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
 

# # # ___________-RestoPaymentMaster End-___________



# # # ___________-RestoInvoices _____________
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

# # # Get RestoInvoice Details
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

# # # Update RestoInvoice Details
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


# # # Delete RestoInvoice
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

# # # ___________-RestoInvoices End-___________