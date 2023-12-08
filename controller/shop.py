from base64 import b64encode
from io import BytesIO
import json
import mimetypes
import uuid
from click import get_app_dir
from flask import request
from bson import InvalidDocument
from flask import Blueprint, request, jsonify
# from pymongo import MongoClient
from bson.objectid import ObjectId
# from firebase_admin import initialize_app, storage
from firebase_admin import credentials, initialize_app, storage
from werkzeug.utils import secure_filename
# from httplib2 import Credentials
from pydantic import ValidationError
import requests
# from model.shop_model import shop_collection,shop_invoices,shop_item_master_collection,shop_masters_collection,shop_payment_master,general_master_collection
from model.shop_model import BankDetails, GeneralMaster, Invoice, InvoiceItem, MenuMaster, PaymentMaster, PaymentModeDetails, PaymentSlab, Product, SellMaster, userinfo
from mongoengine.queryset import QuerySet
# from firebase import Firebase
# shopapp blue print
from mongoengine import EmbeddedDocument
shopapp=Blueprint('shopapp',__name__)
newfrom=Blueprint('newfrom',__name__)



 
# Firebase configuration
firebase_config = {
    "apiKey": "AIzaSyCD5nCSKUFGZgyO3tkEPt3aAuwUKIT2Rgw",
    "authDomain": "emcbackend.firebaseapp.com",
    "projectId": "emcbackend",
    "storageBucket": "emcbackend.appspot.com",
    "messagingSenderId": "381147915781",
    "appId": "1:381147915781:web:732c0ed128b30273c31e6c",
    "measurementId": "G-4WEY4FPCY0"
}

# Path to the downloaded JSON file
firebase_cred_path = './configurations/emcbackend-firebase-adminsdk-56i8d-22778d49de.json'

# Initialize Firebase app with the credentials
cred = credentials.Certificate(firebase_cred_path)
firebase_app = initialize_app(cred, firebase_config, name='emcbackend')

# Firebase Storage instance
storage_client = storage.bucket(app=firebase_app)


# Endpoint to create user and upload multiple images to Firebase
@shopapp.route('/userinfo', methods=['POST'])
def create_user():
    try:
        data = request.form
        name = data.get('name')
        shopName = data.get('shopName')
        address = data.get('address')
        mobile = data.get('mobile')

        if not name or not shopName or not address or not mobile:
            response = {'Body': None, 'error': 'All fields are required', 'status_code': 400}
            return jsonify(response)

        # Ensure 'images' is present in request.files
        if 'images' not in request.files:
            response = {'error': 'Images are required', 'status_code': 400}
            return jsonify(response)

        images = request.files.getlist('images')

        # Validate total size of all images
        total_size = sum(len(image_file.read()) for image_file in images)
        if total_size > 5 * 1024 * 1024:
            return jsonify({'error': 'Total image size exceeds 5MB'}), 400

        # Save each image to Firebase Storage and collect URLs
        photo_urls = []
        for image_file in images:
                image_file.seek(0)
                filename = secure_filename(image_file.filename)
                blob = storage_client.blob('photos/img/' + filename)

                # Set content type to image/jpeg
                blob.upload_from_file(image_file, content_type='image/jpeg')
                
                # Set ACL to public-read
                blob.acl.all().grant_read()
                
                photo_urls.append(blob.public_url)
            

        # Continue with the rest of your code
        user = userinfo(
            name=name,
            shopName=shopName,
            address=address,
            mobile=mobile,
            photos=photo_urls,
            profilePic=None  # Set profilePic to None or provide a default value if needed
        )
        user.save()

        user_id = str(user.id)
        response = {'Body': {'userid': user_id}, 'status': 'success', 'statusCode': 200,
                    'message': 'Item master successfully created'}
        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e), 'status_code': 500}), 500





@newfrom.route('/upload/<string:user_id>', methods=['POST'])
def upload_image(user_id):
    try:
        # Retrieve user from the database using user_id
        user = userinfo.objects.get(id=user_id)
    except userinfo.DoesNotExist:
        return jsonify({'error': 'User not found'}), 404

    # Check if the user_id from the URL matches the one from form data
    if str(user.id) != user_id:
        return jsonify({'error': 'User ID mismatch'}), 400

    # Check if the request contains an image file
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image = request.files['image']

    # Check if the image size is greater than 2MB
    if len(image.read()) > 2 * 1024 * 1024:
        return jsonify({'error': 'Image size exceeds 2MB'}), 400

    # Reset the file pointer after reading
    image.seek(0)

    # Define the desired filename format (e.g., "profilepic1.jpg")
    filename_format = f"profilepic{user.id}.jpg"

    # Set the content type based on the file extension
    content_type, _ = mimetypes.guess_type(filename_format)
    if not content_type:
        content_type = 'application/octet-stream'  # Set a default content type if unable to guess

    # Store the image on Firebase Storage with the predefined filename
    firebase_path = f"profilePic/{filename_format}"
    blob = storage_client.blob(firebase_path)
    blob.upload_from_file(image, content_type=content_type)

    # Generate a URL for the stored image
    cloud_url = blob.public_url

    # Update the user's profilePic field in the database
    user.profilePic = cloud_url
    user.save()

    return jsonify({'message': 'Profile photo updated successfully', 'url': cloud_url}), 200


 

# @newfrom.route('/upload/<string:user_id>', methods=['POST'])
# def upload_image(user_id):
#     try:
#         # Retrieve user from the database using user_id
#         user = userinfo.objects.get(id=user_id)
#     except userinfo.DoesNotExist:
#         return jsonify({'error': 'User not found'}), 404

#     # Check if the user_id from the URL matches the one from form data
#     if str(user.id) != user_id:
#         return jsonify({'error': 'User ID mismatch'}), 400

#     # Check if the request contains an image file
#     if 'image' not in request.files:
#         return jsonify({'error': 'No image provided'}), 400

#     image = request.files['image']

#     # Check if the image size is greater than 2MB
#     if len(image.read()) > 2 * 1024 * 1024:
#         return jsonify({'error': 'Image size exceeds 2MB'}), 400

#     # Reset the file pointer after reading
#     image.seek(0)

#     # Define the desired filename format (e.g., "profilepic1.jpg")
#     filename_format = f"profilepic{user.id}.jpg"

#     # Set the content type based on the file extension
#     content_type, _ = mimetypes.guess_type(filename_format)
#     if not content_type:
#         content_type = 'application/octet-stream'  # Set a default content type if unable to guess

#     # Store the image on Firebase Storage with the predefined filename
#     firebase_path = f"profilePic/{filename_format}"
#     blob = storage_client.blob(firebase_path)
#     blob.upload_from_file(image, content_type=content_type)

#     # Generate a URL for the stored image
#     cloud_url = blob.public_url

#     # Update the user's profilePic field in the database
#     user.profilePic = cloud_url
#     user.save()

#     return jsonify({'message': 'Profile photo updated successfully', 'url': cloud_url}), 200








@newfrom.route('/userinfo/<user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = userinfo.objects.get(id=user_id)
        user_data = {
            'name': user.name,
            'shopName': user.shopName,
            'address': user.address,
            'mobile': user.mobile,
            'photos': user.photos,
            'profilePic': user.profilePic
        }

        response = {'Body': user_data, 'status': 'success', 'statusCode': 200}
        return jsonify(response)

    except userinfo.DoesNotExist:
        response = {'Body': None, 'error': 'User not found', 'status_code': 404}
        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e), 'status_code': 500}), 500




@newfrom.route('/userinfo/<user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        data = request.json
        user = userinfo.objects.get(id=user_id)

        user.name = data.get('name', user.name)
        user.shopName = data.get('shopName', user.shopName)
        user.address = data.get('address', user.address)
        user.mobile = data.get('mobile', user.mobile)
        user.photos = data.get('photos', user.photos)
        user.profilePic = data.get('profilePic', user.profilePic)

        user.save()

        response = {'Body': None, 'status': 'success', 'statusCode': 200, 'message': 'User successfully updated'}
        return jsonify(response)

    except userinfo.DoesNotExist:
        response = {'Body': None, 'error': 'User not found', 'status_code': 404}
        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e), 'status_code': 500}), 500



@shopapp.route('/userinfo/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user = userinfo.objects.get(id=user_id)
        user.delete()

        response = {'Body': None, 'status': 'success', 'statusCode': 200, 'message': 'User successfully deleted'}
        return jsonify(response)

    except userinfo.DoesNotExist:
        response = {'Body': None, 'error': 'User not found', 'status_code': 404}
        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e), 'status_code': 500}), 500          


# ______________________________________________________________________________________________________
#  menu master
# CREATE
@shopapp.route('/api/menumasters/create', methods=['POST'])
def create_menumaster():
    try:
        data = request.json
        showName = data.get('showName')
        path = data.get('path')

        if not all([showName, path]):
            return jsonify({'error': 'All fields are required', 'status_code': 400}), 400

        existing_menumaster = MenuMaster.objects(showName=showName).first()
        if existing_menumaster:
            return jsonify({'error': 'MenuMaster with the same showName already exists', 'status_code': 400}), 400

        menumaster = MenuMaster(showName=showName, path=path)
        menumaster.save()

        response = {"Body": None, "status": "success", "statusCode": 200, "message": 'MenuMaster created'}
        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e), 'status_code': 500}), 500


# READ
@shopapp.route('/api/menumasters/<string:menumaster_id>', methods=['GET'])
def get_menumaster(menumaster_id):
    try:
        object_id = ObjectId(menumaster_id)
        menumaster = MenuMaster.objects(id=object_id).first()

        if menumaster:
            response = {
                "id": str(menumaster.id),
                "showName": menumaster.showName,
                "path": menumaster.path
            }
            return jsonify({"status_code": 200, "message": "Success", "data": response}), 200
        else:
            return jsonify({'error': 'MenuMaster not found', 'status_code': 404}), 404

    except Exception as e:
        return jsonify({'error': str(e), 'status_code': 500}), 500


# UPDATE
@shopapp.route('/api/menumasters/update/<string:menumaster_id>', methods=['PUT'])
def update_menumaster(menumaster_id):
    try:
        object_id = ObjectId(menumaster_id)
        menumaster = MenuMaster.objects(id=object_id).first()

        if not menumaster:
            return jsonify({'error': 'MenuMaster not found', 'status_code': 404}), 404

        data = request.json

        # Validate that at least one field is present in the request
        if not any(field in data for field in ['showName', 'path']):
            return jsonify({'error': 'At least one field (showName or path) is required', 'status_code': 400}), 400

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



# DELETE
@shopapp.route('/api/menumasters/delete/<string:menumaster_id>', methods=['DELETE'])
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


# ______________________________________________________________________________________________________
#iteam masters
# full validation
# CREATE
@shopapp.route('/item_masters/create', methods=['POST'])
def create_item_master():
    try:
        data = request.json
        category = data.get('category')
        subCategory = data.get('subCategory')
        taxIndividual_status = data.get('taxIndividual_status')
        taxIndividual_value = data.get('taxIndividual_value')
        barcode_status = data.get('barcode_status')
        barcode_value = data.get('barcode_value')
        rackManagement_status = data.get('rackManagement_status')
        rackManagement_value=data.get('rackManagement_value')
        deadStock_status = data.get('deadStock_status')
        deadStock_value = data.get('deadStock_value')

        if None in [category, subCategory, taxIndividual_status, taxIndividual_value,
                    barcode_status, barcode_value, rackManagement_status,rackManagement_value, deadStock_status, deadStock_value]:
            return jsonify({'error': 'All fields are required', 'status_code': 400}), 400

        itemmaster = Product(category=category, subCategory=subCategory,
                             taxIndividual_status=taxIndividual_status, taxIndividual_value=taxIndividual_value,
                             barcode_status=barcode_status, barcode_value=barcode_value,
                             rackManagement_status=rackManagement_status,
                             deadStock_status=deadStock_status, deadStock_value=deadStock_value,rackManagement_value=rackManagement_value)
        itemmaster.save()

        response = {"Body": None, "status": "success", "statusCode": 200, "message": 'Item master successfully created'}
        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e), 'status_code': 500}), 500



# READ
@shopapp.route('/item_masters/<string:item_id>', methods=['GET'])
def get_item_master(item_id):
    try:
        # Convert the string item_id to ObjectId
        object_id = ObjectId(item_id)
        itemmaster = Product.objects(id=object_id).first()

        if itemmaster:
            response = {
                "id": str(itemmaster.id),  # Convert ObjectId to string
                "category": itemmaster.category,
                "subCategory": itemmaster.subCategory,
                "taxIndividual_status": itemmaster.taxIndividual_status,
                "taxIndividual_value": itemmaster.taxIndividual_value,
                "barcode_status": itemmaster.barcode_status,
                "barcode_value": itemmaster.barcode_value,
                "rackManagement_status": itemmaster.rackManagement_status,
                "deadStock_status": itemmaster.deadStock_status,
                "deadStock_value": itemmaster.deadStock_value
            }
            return jsonify({"status_code": 200, "message": "Success", "data": response}), 200
        else:
            return jsonify({'error': 'Item master not found', 'status_code': 404}), 404
    except Exception as e:
        return jsonify({'error': str(e), 'status_code': 500}), 500



# UPDATE
@shopapp.route('/item_masters/update/<string:item_id>', methods=['PUT'])
def update_item_master(item_id):
    try:
        # Convert the string item_id to ObjectId
        object_id = ObjectId(item_id)
        itemmaster = Product.objects(id=object_id).first()

        if itemmaster:
            data = request.json

            # Validate that all fields are present in the request
            required_fields = ['category', 'subCategory', 'taxIndividual_status', 'taxIndividual_value',
                                'barcode_status', 'barcode_value', 'rackManagement_status',
                                'deadStock_status', 'deadStock_value']

            if not all(field in data for field in required_fields):
                return jsonify({'error': 'All fields are required', 'status_code': 400}), 400

            for key, value in data.items():
                setattr(itemmaster, key, value)

            itemmaster.save()

            response = {"Body": None, "status": "success", "statusCode": 200, "message": 'Item master updated'}
            return jsonify(response)

        else:
            return jsonify({'error': 'Item master not found', 'status_code': 404}), 404

    except Exception as e:
        return jsonify({'error': str(e), 'status_code': 500}), 500




# DELETE
@shopapp.route('/item_masters/delete/<string:item_id>', methods=['DELETE'])
def delete_item_master(item_id):
    try:
        # Convert the string item_id to ObjectId
        object_id = ObjectId(item_id)
        itemmaster = Product.objects(id=object_id).first()

        if itemmaster:
            itemmaster.delete()
            response = {"Body": None, "status": "success", "statusCode": 200, "message": 'Item master deleted'}
            return jsonify(response)
        else:
            return jsonify({'error': 'Item master not found', 'status_code': 404}), 404

    except Exception as e:
        return jsonify({'error': str(e), 'status_code': 500}), 500

# ______________________________________________________________________________________________________
# sellmasters
# full validation
# CREATE
@shopapp.route('/api/sellmasters/create', methods=['POST'])
def create_sellmaster():
    try:
        data = request.json
        showName = data.get('showName')
        status = data.get('status')
        sellUnits = data.get('sellUnits')
        printers = data.get('printers')
        sellType = data.get('sellType')

        if None in [showName, status, sellUnits, printers, sellType]:
            return jsonify({'error': 'All fields are required', 'status_code': 400}), 400

        sellmaster = SellMaster(showName=showName,status=status,sellUnits=sellUnits,printers=printers,sellType=sellType)
        sellmaster.save()

        response = {"Body": None, "status": "success", "statusCode": 200, "message": 'SellMaster created'}
        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e), 'status_code': 500}), 500



# READ
@shopapp.route('/api/sellmasters/<string:sellmaster_id>', methods=['GET'])
def get_sellmaster(sellmaster_id):
    try:
        object_id = ObjectId(sellmaster_id)
        sellmaster = SellMaster.objects(id=object_id).first()

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
@shopapp.route('/api/sellmasters/update/<string:sellmaster_id>', methods=['PUT'])
def update_sellmaster(sellmaster_id):
    try:
        object_id = ObjectId(sellmaster_id)
        sellmaster = SellMaster.objects(id=object_id).first()

        # Validate that all fields are present in the request
        required_fields = ['showName', 'status', 'sellUnits', 'printers', 'sellType']

        data = request.json

        if not all(field in data for field in required_fields):
            return jsonify({'error': 'All fields are required', 'status_code': 400}), 400

        if sellmaster:
            # Update each field individually, filtering out null values
            for key, value in data.items():
                if value is not None:
                    setattr(sellmaster, key, value)

            sellmaster.save()

            response = {"Body": None, "status": "success", "statusCode": 200, "message": 'SellMaster updated'}
            return jsonify(response)
        else:
            return jsonify({'error': 'SellMaster not found', 'status_code': 404}), 404

    except (ValidationError, InvalidDocument) as e:
        return jsonify({'error': str(e), 'status_code': 400}), 400
    except Exception as e:
        return jsonify({'error': str(e), 'status_code': 500}), 500



# DELETE
@shopapp.route('/api/sellmasters/delete/<string:sellmaster_id>', methods=['DELETE'])
def delete_sellmaster(sellmaster_id):
    try:
        object_id = ObjectId(sellmaster_id)
        sellmaster = SellMaster.objects(id=object_id).first()

        if sellmaster:
            sellmaster.delete()
            response = {"Body": None, "status": "success", "statusCode": 200, "message": 'SellMaster deleted'}
            return jsonify(response)
        else:
            return jsonify({'error': 'SellMaster not found', 'status_code': 404}), 404

    except Exception as e:
        return jsonify({'error': str(e), 'status_code': 500}), 500

# ___________________________________________________________________________________________________________________________________________
# GeneralMaster 
@shopapp.route('/general_masters/create', methods=['POST'])
def create_general_master():
    try:
        data = request.json
        billId_startString = data.get('billId_startString')
        billId_endString = data.get('billId_endString')
        language = data.get('language')
        theme = data.get('theme')
        shopName = data.get('shopName')
        sources = data.get('sources')
        shopAddress = data.get('shopAddress')
        role_title = data.get('role_title')
        role_accessTo = data.get('role_accessTo')
        name = data.get('name')
        userPic = data.get('userPic')
        businessSummaryStatus = data.get('businessSummaryStatus')
        businessSummary_businessURL = data.get('businessSummary_businessURL')
        businessSummary_businessName = data.get('businessSummary_businessName')
        businessSummary_businessAddress = data.get('businessSummary_businessAddress')
        businessSummary_businessMobile = data.get('businessSummary_businessMobile')
        businessSummary_businessEmail = data.get('businessSummary_businessEmail')
        businessSummary_businessDescription = data.get('businessSummary_businessDescription')
        orderTypes_showName = data.get('orderTypes_showName')
        orderTypes_properties = data.get('orderTypes_properties')

        if None in [billId_startString, billId_endString, language, theme, shopName, sources, shopAddress,
                    role_title, role_accessTo, name, userPic, businessSummaryStatus,
                    businessSummary_businessURL, businessSummary_businessName, businessSummary_businessAddress,
                    businessSummary_businessMobile, businessSummary_businessEmail, businessSummary_businessDescription,
                    orderTypes_showName, orderTypes_properties]:
            return jsonify({'error': 'All fields are required', 'status_code': 400}), 400

        general_master = GeneralMaster(
            billId_startString=billId_startString,
            billId_endString=billId_endString,
            language=language,
            theme=theme,
            shopName=shopName,
            sources=sources,
            shopAddress=shopAddress,
            role_title=role_title,
            role_accessTo=role_accessTo,
            name=name,
            userPic=userPic,
            businessSummaryStatus=businessSummaryStatus,
            businessSummary_businessURL=businessSummary_businessURL,
            businessSummary_businessName=businessSummary_businessName,
            businessSummary_businessAddress=businessSummary_businessAddress,
            businessSummary_businessMobile=businessSummary_businessMobile,
            businessSummary_businessEmail=businessSummary_businessEmail,
            businessSummary_businessDescription=businessSummary_businessDescription,
            orderTypes_showName=orderTypes_showName,
            orderTypes_properties=orderTypes_properties
        )
        general_master.save()

        response = {"Body": None, "status": "success", "statusCode": 200, "message": 'General Master successfully created'}
        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e), 'status_code': 500}), 500



# READ
@shopapp.route('/general_masters/<string:general_master_id>', methods=['GET'])
def get_general_master(general_master_id):
    try:
        # Convert the string general_master_id to ObjectId
        object_id = ObjectId(general_master_id)
        general_master = GeneralMaster.objects(id=object_id).first()

        if general_master:
            response = {
                "id": str(general_master.id),  # Convert ObjectId to string
                "billId_startString": general_master.billId_startString,
                "billId_endString": general_master.billId_endString,
                "language": general_master.language,
                "theme": general_master.theme,
                "shopName": general_master.shopName,
                "sources": general_master.sources,
                "shopAddress": general_master.shopAddress,
                "role_title": general_master.role_title,
                "role_accessTo": general_master.role_accessTo,
                "name": general_master.name,
                "userPic": general_master.userPic,
                "businessSummaryStatus": general_master.businessSummaryStatus,
                "businessSummary_businessURL": general_master.businessSummary_businessURL,
                "businessSummary_businessName": general_master.businessSummary_businessName,
                "businessSummary_businessAddress": general_master.businessSummary_businessAddress,
                "businessSummary_businessMobile": general_master.businessSummary_businessMobile,
                "businessSummary_businessEmail": general_master.businessSummary_businessEmail,
                "businessSummary_businessDescription": general_master.businessSummary_businessDescription,
                "orderTypes_showName": general_master.orderTypes_showName,
                "orderTypes_properties": general_master.orderTypes_properties
            }
            return jsonify({"status_code": 200, "message": "Success", **response}), 200
        else:
            return jsonify({'error': 'General Master not found', 'status_code': 404}), 404
    except Exception as e:
        return jsonify({'error': str(e), 'status_code': 500}), 500



# UPDATE
@shopapp.route('/general_masters/update/<string:general_master_id>', methods=['PUT'])
def update_general_master(general_master_id):
    try:
        # Convert the string general_master_id to ObjectId
        object_id = ObjectId(general_master_id)
        general_master = GeneralMaster.objects(id=object_id).first()

        if general_master:
            data = request.json

            # Validate that all fields are present in the request
            required_fields = [
                'billId_startString', 'billId_endString', 'language', 'theme', 'shopName',
                'sources', 'shopAddress', 'role_title', 'role_accessTo', 'name', 'userPic',
                'businessSummaryStatus', 'businessSummary_businessURL', 'businessSummary_businessName',
                'businessSummary_businessAddress', 'businessSummary_businessMobile', 'businessSummary_businessEmail',
                'businessSummary_businessDescription', 'orderTypes_showName', 'orderTypes_properties'
            ]

            if not all(field in data for field in required_fields):
                return jsonify({'error': 'All fields are required', 'status_code': 400}), 400

            for key, value in data.items():
                setattr(general_master, key, value)

            general_master.save()

            response = {"Body": None, "status": "success", "statusCode": 200, "message": 'General Master updated'}
            return jsonify(response)

        else:
            return jsonify({'error': 'General Master not found', 'status_code': 404}), 404

    except Exception as e:
        return jsonify({'error': str(e), 'status_code': 500}), 500



# DELETE
@shopapp.route('/general_masters/delete/<string:general_id>', methods=['DELETE'])
def delete_general_master(general_id):
    try:
        # Convert the string general_id to ObjectId
        object_id = ObjectId(general_id)
        general_master = GeneralMaster.objects(id=object_id).first()

        if general_master:
            general_master.delete()
            response = {"Body": None, "status": "success", "statusCode": 200, "message": 'GeneralMaster deleted'}
            return jsonify(response)
        else:
            return jsonify({'error': 'GeneralMaster not found', 'status_code': 404}), 404

    except Exception as e:
        return jsonify({'error': str(e), 'status_code': 500}), 500
# _______________________________________________________________________________________________________________________________________________ 
#PaymentMaster
# CREATE
@shopapp.route('/payment_masters/create', methods=['POST'])
def create_payment_master():
    try:
        data = request.json
        taxSlab_showName = data.get('taxSlab_showName')
        taxSlab_properties = data.get('taxSlab_properties')
        banks_showName = data.get('banks_showName')
        banks_properties = data.get('banks_properties')
        paymentModes_showName = data.get('paymentModes_showName')
        paymentModes_properties = data.get('paymentModes_properties')

        if None in [taxSlab_showName, taxSlab_properties, banks_showName, banks_properties,
                    paymentModes_showName, paymentModes_properties]:
            return jsonify({'error': 'All fields are required', 'status_code': 400}), 400

        payment_master = PaymentMaster(
            taxSlab_showName=taxSlab_showName,
            taxSlab_properties=taxSlab_properties,
            banks_showName=banks_showName,
            banks_properties=banks_properties,
            paymentModes_showName=paymentModes_showName,
            paymentModes_properties=paymentModes_properties
        )
        payment_master.save()

        response = {"Body": None, "status": "success", "statusCode": 200, "message": 'Payment Master successfully created'}
        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e), 'status_code': 500}), 500



 
# Convert EmbeddedDocumentField to dictionary for serialization
def convert_embedded_fields(embedded_field):
    if isinstance(embedded_field, list):
        return [convert_embedded_fields(item) for item in embedded_field]
    elif isinstance(embedded_field, QuerySet):
        return convert_embedded_fields(list(embedded_field))
    elif isinstance(embedded_field, EmbeddedDocument):
        return embedded_field.to_mongo()
    return embedded_field


@shopapp.route('/payment_masters/<string:payment_master_id>', methods=['GET'])
def get_payment_master(payment_master_id):
    try:
        object_id = ObjectId(payment_master_id)
        payment_master = PaymentMaster.objects(id=object_id).first()

        if payment_master:
            response = {
                "id": str(payment_master.id),
                "taxSlab_showName": payment_master.taxSlab_showName,
                "taxSlab_properties": convert_embedded_fields(payment_master.taxSlab_properties),
                "banks_showName": payment_master.banks_showName,
                "banks_properties": convert_embedded_fields(payment_master.banks_properties),
                "paymentModes_showName": payment_master.paymentModes_showName,
                "paymentModes_properties": convert_embedded_fields(payment_master.paymentModes_properties),
            }
            return jsonify({"status_code": 200, "message": "Success", **response}), 200
        else:
            return jsonify({'error': 'Payment Master not found', 'status_code': 404}), 404

    except Exception as e:
        return jsonify({'error': str(e), 'status_code': 500}), 500



# UPDATE
# Update route definition
# Update route definition
@shopapp.route('/payment_masters/update/<string:payment_master_id>', methods=['PUT'])
def update_payment_master(payment_master_id):
    try:
        # Retrieve PaymentMaster document by ID
        object_id = ObjectId(payment_master_id)
        payment_master = PaymentMaster.objects(id=object_id).first()

        # Check if PaymentMaster document exists
        if payment_master:
            data = request.json

            # Validate required fields
            required_fields = [
                'taxSlab_showName', 'taxSlab_properties', 'banks_showName', 'banks_properties',
                'paymentModes_showName', 'paymentModes_properties'
            ]

            if not all(field in data for field in required_fields):
                return jsonify({'error': 'All fields are required', 'status_code': 400}), 400

            # Update common fields
            common_fields = [
                'taxSlab_showName', 'taxSlab_properties', 'banks_showName', 'banks_properties',
                'paymentModes_showName', 'paymentModes_properties'
            ]

            for field in common_fields:
                if field in data and data[field] is not None and data[field] != "":
                    setattr(payment_master, field, data[field])
                elif field not in data:
                    return jsonify({'error': f'Missing value for key: {field}', 'status_code': 400}), 400

            # Update taxSlab_properties if not None or empty
            if data.get('taxSlab_showName') is not None and data.get('taxSlab_showName') != "":
                payment_master.taxSlab_showName = data.get('taxSlab_showName', '')

            payment_master.taxSlab_properties = [
                PaymentSlab(**slab_data) for slab_data in data.get('taxSlab_properties', []) if slab_data.get('slabName') is not None and slab_data.get('slabName') != ""
            ]

            # Update banks_properties if not None or empty
            if data.get('banks_showName') is not None and data.get('banks_showName') != "":
                payment_master.banks_showName = data.get('banks_showName', '')

            payment_master.banks_properties = [
                BankDetails(**bank_data) for bank_data in data.get('banks_properties', []) if bank_data.get('bankName') is not None and bank_data.get('bankName') != ""
            ]

            # Update paymentModes_properties if not None or empty
            if data.get('paymentModes_showName') is not None and data.get('paymentModes_showName') != "":
                payment_master.paymentModes_showName = data.get('paymentModes_showName', '')

            payment_master.paymentModes_properties = [
                PaymentModeDetails(**mode_data) for mode_data in data.get('paymentModes_properties', []) if mode_data.get('modeName') is not None and mode_data.get('modeName') != ""
            ]

            # Save the updated PaymentMaster document
            payment_master.save()

            response = {"Body": None, "status": "success", "statusCode": 200, "message": 'Payment Master updated'}
            return jsonify(response)

        else:
            return jsonify({'error': 'Payment Master not found', 'status_code': 404}), 404

    except Exception as e:
        return jsonify({'error': str(e), 'status_code': 500}), 500




# DELETE
@shopapp.route('/payment_masters/delete/<string:payment_id>', methods=['DELETE'])
def delete_payment_master(payment_id):
    try:
        object_id = ObjectId(payment_id)
        payment_master = PaymentMaster.objects(id=object_id).first()

        if payment_master:
            payment_master.delete()
            response = {"Body": None, "status": "success", "statusCode": 200, "message": 'Payment Master deleted'}
            return jsonify(response)
        else:
            return jsonify({'error': 'Payment Master not found', 'status_code': 404}), 404

    except Exception as e:
        return jsonify({'error': str(e), 'status_code': 500}), 500
    
    
# ____________________________________________________________________________________________________________________________________    
# Invoices Table
# CREATE
@shopapp.route('/invoices/create', methods=['POST'])
def create_invoice():
    try:
        data = request.json
        items_data = data.get('items', [])
        item_list = [InvoiceItem(**item_data) for item_data in items_data]

        invoice = Invoice(
            billId=data.get('billId'),
            customer=data.get('customer'),
            billDate=data.get('billDate'),
            items=item_list,
            savings=data.get('savings'),
            status=data.get('status'),
            count=data.get('count'),
            orderType=data.get('orderType'),
            taxedAmount=data.get('taxedAmount'),
            taxedP=data.get('taxedP'),
            discountedAmount=data.get('discountedAmount'),
            discountedP=data.get('discountedP'),
            grandTotal=data.get('grandTotal'),
            credit=data.get('credit'),
            paidAmount=data.get('paidAmount'),
            returnedAmount=data.get('returnedAmount'),
            paidIn=data.get('paidIn'),
            paymentMode=data.get('paymentMode'),
            remarks=data.get('remarks')
        )

        invoice.save()

        response = {"Body": None, "status": "success", "statusCode": 200, "message": 'Invoice successfully created'}
        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e), 'status_code': 500}), 500
    
    

# READ
@shopapp.route('/invoices/<string:invoice_id>', methods=['GET'])
def get_invoice(invoice_id):
    try:
        # Convert the string invoice_id to ObjectId
        object_id = ObjectId(invoice_id)
        invoice = Invoice.objects(id=object_id).first()

        if invoice:
            response = {
                "billId": invoice.billId,
                "customer": invoice.customer,
                "billDate": invoice.billDate,
                "items": [
                    {
                        "itemName": item.itemName,
                        "quantity": item.quantity,
                        "price": item.price,
                        "total": item.total
                    } for item in invoice.items
                ],
                "savings": invoice.savings,
                "status": invoice.status,
                "count": invoice.count,
                "orderType": invoice.orderType,
                "taxedAmount": invoice.taxedAmount,
                "taxedP": invoice.taxedP,
                "discountedAmount": invoice.discountedAmount,
                "discountedP": invoice.discountedP,
                "grandTotal": invoice.grandTotal,
                "credit": invoice.credit,
                "paidAmount": invoice.paidAmount,
                "returnedAmount": invoice.returnedAmount,
                "paidIn": invoice.paidIn,
                "paymentMode": invoice.paymentMode,
                "remarks": invoice.remarks
            }
            return jsonify({"status_code": 200, "message": "Success", "data": response}), 200
        else:
            return jsonify({'error': 'Invoice not found', 'status_code': 404}), 404
    except Exception as e:
        return jsonify({'error': str(e), 'status_code': 500}), 500



 # UPDATE
@shopapp.route('/invoices/update/<string:invoice_id>', methods=['PUT'])
def update_invoice(invoice_id):
    try:
        # Convert the string invoice_id to ObjectId
        object_id = ObjectId(invoice_id)
        invoice = Invoice.objects(id=object_id).first()

        if invoice:
            data = request.json

            # Validate that all fields are present in the request
            required_fields = ['billId', 'customer', 'billDate', 'items', 'savings', 'status', 'count',
                                'orderType', 'taxedAmount', 'taxedP', 'discountedAmount', 'discountedP',
                                'grandTotal', 'credit', 'paidAmount', 'returnedAmount', 'paidIn',
                                'paymentMode', 'remarks']

            if not all(field in data for field in required_fields):
                return jsonify({'error': 'All fields are required', 'status_code': 400}), 400

            # Update fields
            for key, value in data.items():
                if key == 'items':
                    # If updating 'items', convert each item dictionary to InvoiceItem instance
                    updated_items = [InvoiceItem(**item) for item in value]
                    setattr(invoice, key, updated_items)
                else:
                    setattr(invoice, key, value)

            # Save the updated invoice document
            invoice.save()

            response = {"Body": None, "status": "success", "statusCode": 200, "message": 'Invoice updated'}
            return jsonify(response)

        else:
            return jsonify({'error': 'Invoice not found', 'status_code': 404}), 404

    except Exception as e:
        return jsonify({'error': str(e), 'status_code': 500}), 500



# DELETE
@shopapp.route('/invoices/delete/<string:invoice_id>', methods=['DELETE'])
def delete_invoice(invoice_id):
    try:
        # Convert the string invoice_id to ObjectId
        object_id = ObjectId(invoice_id)
        invoice = Invoice.objects(id=object_id).first()

        if invoice:
            invoice.delete()
            response = {"Body": None, "status": "success", "statusCode": 200, "message": 'Invoice deleted'}
            return jsonify(response)

        else:
            return jsonify({'error': 'Invoice not found', 'status_code': 404}), 404

    except Exception as e:
        return jsonify({'error': str(e), 'status_code': 500}), 500
# __________________________________________________________________________________________________________________________