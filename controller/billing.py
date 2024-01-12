import logging
from flask import Blueprint, jsonify, request
from model.billing_model import Billing, BillingEntry
from model.resto_model import Item, ItemMaster
from model.signInsignup_model import User
from mongoengine.errors import DoesNotExist


billing=Blueprint('billing',__name__)


# Global variable for the bill counter
bill_counter = 1001  # Initialize with the starting value

# Create a new billing route
@billing.route('/v1/billing', methods=['POST'])
def create_bill():
    try:
        global bill_counter  # Access the global variable

        # Extract the user_id from the request headers
        user_id = request.headers.get('user_id')

        # Check if the user_id is provided
        if not user_id:
            return jsonify({'body': None, "status": "error", 'message': 'User ID is required in headers.', 'statusCode': 400}), 200

        # Get the current user
        user = User.objects.get(id=user_id)

        # Get items from the request payload
        items = request.json.get('items', [])

        # Calculate subtotal
        subtotal = 0
        for item_data in items:
            item_code = item_data.get('itemCode')
            quantity = item_data.get('quantity', 1)

            # Fetch item details from the database
            item = Item.objects.get(itemCode=item_code)

            # Check if there is enough stock
            if item.currentStock < quantity:
                return jsonify({'body': None, 'status': 'error', 'message': f'Not enough stock for item {item.itemName}', 'statusCode': 400}), 200
                
            if not item_code.strip():
                  return jsonify({'body': None, "status": "error", 'message': 'itemCode cannot be empty.', 'statusCode': 400}), 200
       
                # Calculate item total
            item_total = int(item.itemPrice * quantity)

            # Update subtotal
            subtotal += item_total

            # Subtract quantity from current stock
            item.currentStock -= quantity
            item.save()

            # Get tax and discount from the request payload
            tax = int(request.json.get('tax', 0))
            discount = int(request.json.get('discount', 0))

            # Calculate grand total
            grand_total = int(subtotal + tax - discount)
            # Add billing entry with auto-incrementing bill number
            billing_entry = Billing(
                itemCode=item.itemCode,
                itemName=item.itemName,
                quantity=quantity,
                itemPrice=item.itemPrice,
                itemTotal=item_total,
                subtotal=subtotal,
                tax=tax,
                discount=discount,
                grandTotal=grand_total,
                creator=user,
                billNumber=bill_counter,
                status='complete'  # Add the auto-incrementing bill number
            )
            billing_entry.save()



        # Increment the bill counter for the next bill
        bill_counter += 1

        # Create a response object
        response_items = [{
            'itemCode': item_data.get('itemCode'),
            'itemName': item.itemName,
            'quantity': item_data.get('quantity', 1),
            'itemTotal': item.itemPrice * item_data.get('quantity', 1)
        } for item_data in items]

        response = {
            'items': response_items,
            'subtotal': subtotal,
            'tax': tax,
            'discount': discount,
            'grandTotal': grand_total,
            'billNumber': bill_counter - 1,  # Use the last assigned bill number
            'status': 'complete'  # You may update this status based on your business logic
        }

        return jsonify({'body': response, 'status': 'success', 'statusCode': 200, 'message': 'Billing created successfully'}), 200

    except Exception as e:
        return jsonify({'body': None, 'error': str(e), 'statusCode': 500}), 500
    

    
# # Create a new billing route
# @billing.route('/v1/billing', methods=['POST'])
# def create_billing():
#     try:
#         # Extract the user_id from the request headers
#         user_id = request.headers.get('user_id')

#         # Check if the user_id is provided
#         if not user_id:
#             return jsonify({'body': None, "status": "error", 'message': 'User ID is required in headers.', 'statusCode': 400}), 200

#         # Get the current user
#         user = User.objects.get(id=user_id)

#         # Get items from the request payload
#         items = request.json.get('items', [])

#         # Calculate subtotal, tax, discount, and grand total
#         subtotal = 0
#         for item_data in items:
#             item_code = item_data.get('itemCode')
#             quantity = item_data.get('quantity', 1)

#             # Fetch item details from the database
#             item = Item.objects.get(itemCode=item_code)

#             # Calculate item total
#             item_total = item.itemPrice * quantity

#             # Update subtotal
#             subtotal += item_total

#             # Add billing entry
#             billing_entry = Billing(
#                 itemCode=item_code,
#                 itemName=item.itemName,
#                 quantity=quantity,
#                 itemPrice=item.itemPrice,
#                 itemTotal=item_total,
#                 creator=user
#             )
#             billing_entry.save()

#         # Calculate tax, discount, and grand total
#         tax = request.json.get('tax', 0)
#         discount = request.json.get('discount', 0)
#         grand_total = subtotal + tax - discount

#         # Create a response object
#         response_items = [{
#             'itemCode': item_data.get('itemCode'),
#             'itemName': item_data.get('itemName'),
#             'quantity': item_data.get('quantity', 1),
#             'itemTotal': item.itemPrice * item_data.get('quantity', 1)
#         } for item_data in items]

#         response = {
#             'items': response_items,
#             'subtotal': subtotal,
#             'tax': tax,
#             'discount': discount,
#             'grandTotal': grand_total,
#             'status': 'complete'  # You may update this status based on your business logic
#         }

#         return jsonify({'body': response, 'status': 'success', 'statusCode': 200, 'message': 'Billing created successfully'}), 200

#     except Exception as e:
#         return jsonify({'body': None, 'error': str(e), 'statusCode': 500}), 500






# Helper function to validate user ID in headers
def validate_user_id():
    user_id = request.headers.get('user_id')
    if not user_id:
        return False, jsonify({'body': None, 'status': 'error', 'message': 'User ID is required in headers.', 'statusCode': 400}), 200

    user_exists = User.objects(id=user_id).first()
    if not user_exists:
        return False, jsonify({'body': None, 'status': 'error', 'message': 'Invalid User ID.', 'statusCode': 401}), 401
    return True, None



# # Create a new billing route for creating a billing entry
# @billing.route('/v1/billing', methods=['POST'])
# def create_billing():
#     try:
#         # Validate user ID
#         valid_user, response = validate_user_id()
#         if not valid_user:
#             return response

#         # Get the current user
#         user = User.objects.get(id=request.headers.get('user_id'))

#         # Get items from the request payload
#         items = request.json.get('items', [])

#         # Calculate subtotal
#         subtotal = 0
#         for item_data in items:
#             item_code = item_data.get('itemCode')
#             quantity = item_data.get('quantity', 1)

#             # Fetch item details from the database
#             item = Item.objects.get(itemCode=item_code)

#             # Check if there is enough stock
#             if item.currentStock < quantity:
#                 return jsonify({'body': None, 'status': 'error', 'message': f'Not enough stock for item {item.itemName}', 'statusCode': 400}), 200

#             # Calculate item total
#             item_total = item.itemPrice * quantity

#             # Update subtotal
#             subtotal += float(item_total)

#             # Subtract quantity from current stock
#             item.currentStock -= quantity
#             item.save()

#             # Add billing entry
#             billing_entry = Billing(
#                 itemCode=item.itemCode,
#                 itemName=item.itemName,
#                 quantity=quantity,
#                 itemPrice=item.itemPrice,
#                 itemTotal=item_total,
#                 creator=user
#             )
#             billing_entry.save()

#         # Get tax and discount from the request payload
#         # Get tax and discount from the request payload
#         tax = float(request.json.get('tax', 0))  # Convert tax to float
#         discount = float(request.json.get('discount', 0))  # Convert discount to float

#         # Calculate grand total
#         grand_total = float(subtotal + tax - discount)

#         # Create a response object
#         response_items = [{
#             'itemCode': item_data.get('itemCode'),
#             'itemName': item_data.get('itemName'),
#             'quantity': item_data.get('quantity', 1),
#             'itemTotal': item.itemPrice * item_data.get('quantity', 1)
#         } for item_data in items]

#         response = {
#             'items': response_items,
#             'itemName': item.itemName,
#             'subtotal': subtotal,
#             'tax': tax,
#             'discount': discount,
#             'grandTotal': grand_total,
#             'status': 'complete'  # You may update this status based on your business logic
#         }

#         return jsonify({'body': response, 'status': 'success', 'statusCode': 200, 'message': 'Billing created successfully'}), 200

#     except Exception as e:
#         return jsonify({'body': None, 'error': str(e), 'statusCode': 500}), 500


# _____________________________________________________________________________
# Retrieve all billing entries for a user
# @billing.route('/v1/allbilling', methods=['GET'])
# def get_all_billing_entries():
#     try:
#         # Validate user ID
#         valid_user, response = validate_user_id()
#         if not valid_user:
#             return response

#         # Get the current user
#         user = User.objects.get(id=request.headers.get('user_id'))

#         # Retrieve all billing entries for the user
#         billing_entries = Billing.objects(creator=user)

#         # Create a response object
#         response_entries = [{
#             'id': str(entry.id),
#             'billNumber': entry.billNumber,
#             'itemCode': entry.itemCode,
#             'itemName': entry.itemName,
#             'quantity': entry.quantity,
#             'itemTotal': entry.itemTotal
#         } for entry in billing_entries]

#         return jsonify({'body': response_entries, 'status': 'success', 'statusCode': 200, 'message': 'Billing entries retrieved successfully'}), 200

#     except Exception as e:
#         return jsonify({'body': None, 'error': str(e), 'statusCode': 500}), 500


@billing.route('/v1/allbilling', methods=['GET'])
def get_all_billing_entries():
    try:
        # Validate user ID
        valid_user, response = validate_user_id()
        if not valid_user:
            return response

        # Get the current user
        user = User.objects.get(id=request.headers.get('user_id'))

        # Retrieve all billing entries for the user
        billing_entries = Billing.objects(creator=user)
       
        # Create a response object
        response_entries = []
        for entry in billing_entries:
            # Find the item using the item code from the current billing entry
            item_obj = Item.objects(itemCode=entry.itemCode).first()

            if item_obj:
                response_entry = {
                    "_id": str(item_obj.id),
                    'billNumber': entry.billNumber,
                    'grandTotal': float(entry.grandTotal),
                    'items': [{
                        "_id": str(entry.id),
                        'itemCode': entry.itemCode,
                        'itemName': entry.itemName,
                        'itemTotal': float(entry.itemTotal),
                        'quantity': entry.quantity
                    }],
                    'status': entry.status,
                    'subtotal': float(entry.subtotal),
                    'tax': float(entry.tax),
                    'totalDiscount': float(entry.discount)  # Assuming totalDiscount is your discount field
                }
                response_entries.append(response_entry)
            else:
                # Handle the case where the item with the given itemCode is not found
                return jsonify({'body': None, 'error': f'Item with code {entry.itemCode} not found', 'statusCode': 404}), 404

        response = {
            'body': response_entries,
            'message': 'Billing entries retrieved successfully',
            'status': 'success',
            'statusCode': 200
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({'body': None, 'error': str(e), 'statusCode': 500}), 500

# ______________________________________________________________________________________


def validate_user_id():
    user_id = request.headers.get('user_id')
    if not user_id:
        return False, jsonify({'body': None, 'status': 'error', 'message': 'User ID not provided in headers', 'statusCode': 400})
    
    try:
        user = User.objects.get(id=user_id)
        return True, None
    except DoesNotExist:
        return False, jsonify({'body': None, 'status': 'error', 'message': 'User not found', 'statusCode': 404})



# Get billing entry by code or name
@billing.route('/v1/billing', methods=['GET'])
def get_billing_entry_by_code_or_name():
    try:
        # Extract the user_id from the request headers
        user_id = request.headers.get('user_id')

        # Check if the user_id is provided
        if not user_id:
            return jsonify({'body': None, "status": "error", 'message': 'User ID is required in headers.', 'statusCode': 400}), 200

        # Get the current user
        user = User.objects.get(id=user_id)

        # Get itemCode and itemName from query parameters
        item_code = request.args.get('itemCode')
        item_name = request.args.get('itemName')

        # Log the values for debugging
        logging.info(f"Querying with itemCode: {item_code}, itemName: {item_name}")

        # Validate that at least one of itemCode or itemName is provided
        if item_code is None and item_name is None:
            return jsonify({'body': None, 'status': 'error', 'message': 'Please provide either itemCode or itemName', 'statusCode': 400}), 400

        # Query for the billing entry based on itemCode or itemName
        query_params = {
            'creator': user
        }
        if item_code is not None:
            query_params['itemCode'] = item_code
        if item_name is not None:
            query_params['itemName__iexact'] = item_name

        billing_entries = Billing.objects.filter(**query_params)

        if not billing_entries:
            return jsonify({'body': None, 'status': 'error', 'message': 'Billing entry not found', 'statusCode': 404}), 404

        # Create a list of response objects
        response_entries = []
        for entry in billing_entries:
            response_entry = {
                'id': str(entry.id), 
                'billNumber': entry.billNumber,
                'itemCode': entry.itemCode,
                'itemName': entry.itemName,
                'quantity': entry.quantity,
                'itemTotal': entry.itemTotal
            }
            response_entries.append(response_entry)

        response = {'body': response_entries, 'status': 'success', 'statusCode': 200, 'message': 'Billing entries retrieved successfully'}
        return jsonify(response), 200

    except Exception as e:
        logging.error(f"Error in API: {str(e)}")
        return jsonify({'body': None, 'error': str(e), 'statusCode': 500}), 500




 
# Delete a billing entry
@billing.route('/v1/billing/<billing_id>', methods=['DELETE'])
def delete_billing_entry(billing_id):
    try:
        # Validate user ID
        valid_user, response = validate_user_id()
        if not valid_user:
            return response

        # Get the billing entry by ID
        billing_entry = Billing.objects.get(id=billing_id, creator=request.headers.get('user_id'))

        # Delete the billing entry
        billing_entry.delete()

        return jsonify({'body': None, 'status': 'success', 'statusCode': 200, 'message': 'Billing entry deleted successfully'}), 200

    except DoesNotExist:
        return jsonify({'body': None, 'status': 'error', 'message': 'Billing entry not found', 'statusCode': 404}), 404

    except Exception as e:
        return jsonify({'body': None, 'error': str(e), 'statusCode': 500}), 500
    


