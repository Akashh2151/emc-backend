from collections import defaultdict
import logging
import re
from flask import Blueprint, jsonify, request
from model.billing_model import Billing, BillingEntry
from model.resto_model import Item, ItemMaster
from model.signInsignup_model import User
from mongoengine.errors import DoesNotExist
from decimal import Decimal

from security.mastervalidation import validate_no_blank_spaces


billing=Blueprint('billing',__name__)
# Global variable for the bill counter
bill_counter = 1001  # Initialize with the starting value
@billing.route('/v1/billing', methods=['POST'])
def create_items():
    global bill_counter
    try:
        # Extract the user_id from the request headers
        user_id = request.headers.get('user_id')

        # Check if the user_id is provided
        if not user_id:
            return jsonify({'body': None, "status": "error", 'message': 'User ID is required in headers.', 'statusCode': 400}), 200

        # Get the current user
        user = User.objects.get(id=user_id) 

        items_data = request.json

        billing_response = []
               # Use the current bill counter for all items in this request
        current_bill_number = bill_counter

        for data in items_data:
            item_code = data.get('itemCode')
            item_name = data.get('itemName')
            item_price = data.get('itemPrice')

            # Calculate subtotal, grandTotal, status, discount, and tax
            subtotal = item_price * data.get('quantity', 1)
            discount = data.get('discount', 0)
            tax = data.get('tax', 0)
            grand_total = subtotal - discount + tax



            # Get the item from the collection based on itemCode
            existing_item = Item.objects(itemCode=item_code).first()

            if existing_item:
                # Check and subtract quantity from currentStock
                current_stock = existing_item.currentStock
                requested_quantity = data.get('quantity', 1)

                if current_stock is not None and current_stock >= requested_quantity:
                    existing_item.currentStock -= requested_quantity
                else:
                    return jsonify({'body': {}, "status": "error", 'message': f'Insufficient stock for itemCode: {item_code}', 'statusCode': 400}), 200

                # Save the updated item
                existing_item.save()

                # Store the calculated values in the new billing document
                new_billing = Billing(
                    itemCode=item_code,
                    itemName=item_name,
                    itemPrice=item_price,
                    itemCategory=data.get('itemCategory', None),
                    itemSubCategory=data.get('itemSubCategory', None),
                    ingredients=data.get('ingredients', None),
                    recipe=data.get('recipe', None),
                    allergen=data.get('allergen', None),
                    portionSize=data.get('portionSize', None),
                    tax=tax,
                    discount=discount,
                    currentStock=existing_item.currentStock,
                    barcode=data.get('barcode', None),
                    quantity=requested_quantity,
                    creator=user,
                    subtotal=subtotal,
                    billNumber=current_bill_number, 
                    grandTotal=grand_total
                )

                # Validate for blank spaces in keys and values
                is_no_blank_spaces, error_message = validate_no_blank_spaces(data)
                if not is_no_blank_spaces:
                    response = {"body": {}, "status": "error", "statusCode": 400, "message": error_message}
                    return jsonify(response), 200

                # Save the new billing document
                new_billing.save()

                # Increment the bill counter
                # bill_counter += 1

                # Append billing details to the response array
                billing_response.append({
                    "billingId": str(new_billing.id),
                    "billNumber": current_bill_number,
                    "subtotal": subtotal,
                    "grandTotal": grand_total,
                    "discount": discount,
                    "tax": tax,
                    "item": data,
                })

             # Increment the bill counter after processing all items
                bill_counter += 1

        # Return the response with the billing details for each item
        response = {
            "body": billing_response,
            "status": "success",
            "statusCode": 200,
            "message": 'Items created successfully'
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({'body': {}, 'error': str(e), 'statusCode': 500})



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

        # Aggregate billing entries by bill number
        bills = defaultdict(list)
        for entry in billing_entries:
            bills[entry.billNumber].append(entry)

        # Create a response object
        response_bills = []
        for bill_number, entries in bills.items():
            bill_subtotal = Decimal('0.0')
            bill_total_tax = Decimal('0.0')
            bill_total_discount = Decimal('0.0')
            bill_items = []

            for entry in entries:
                item_total = Decimal(entry.itemPrice) * Decimal(entry.quantity)
                bill_subtotal += item_total
                bill_total_tax += Decimal(entry.tax) if entry.tax is not None else Decimal('0.0')
                bill_total_discount += Decimal(entry.discount) if entry.discount is not None else Decimal('0.0')

                bill_items.append({
                    "_id": str(entry.id),
                    "itemCode": entry.itemCode,
                    "itemName": entry.itemName,
                    "itemCategory": entry.itemCategory,
                    "itemSubCategory": entry.itemSubCategory,
                    "itemPrice": float(entry.itemPrice),
                    "ingredients": entry.ingredients,
                    "recipe": entry.recipe,
                    "allergen": entry.allergen,
                    "portionSize": entry.portionSize,
                    "quantity": entry.quantity,
                    "tax": float(entry.tax) if entry.tax is not None else None,
                    "discount": float(entry.discount) if entry.discount is not None else None,
                    "currentStock": int(entry.currentStock) if entry.currentStock is not None else None,
                    "barcode": entry.barcode,
                    "itemTotal": float(item_total)
                })

            bill_grand_total = bill_subtotal + bill_total_tax - bill_total_discount
            response_bills.append({
                # "_id": str(bill_number),
                "billNumber": bill_number,
                "subtotal": round(float(bill_subtotal), 2),
                "tax": round(float(bill_total_tax), 2),
                "totalDiscount": round(float(bill_total_discount), 2),
                "grandTotal": round(float(bill_grand_total), 2),
                "items": bill_items
            })

        # Create the final response
        response = {
            "bills": response_bills,
            "status": "success",
            "statusCode": 200,
            "message": "Billing entries retrieved successfully",
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
@billing.route('/v1/billing/search', methods=['GET'])
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

        billing_entries = Item.objects.filter(**query_params)

        if not billing_entries:
            return jsonify({'body': None, 'status': 'error', 'message': 'Billing entry not found', 'statusCode': 404}), 404

        response_entries = []
        for entry in billing_entries:
            response_entry = {
                '_id': str(entry.id),
                'billNumber': entry.billNumber,
                'grandTotal': float(entry.grandTotal),
                'items': [{
                    '_id': str(entry.id),
                    'itemCode': entry.itemCode,
                    'itemName': entry.itemName,
                    'itemCategory': entry.itemCategory,
                    'itemSubCategory': entry.itemSubCategory,
                    'itemPrice': float(entry.itemPrice),
                    'ingredients': entry.ingredients,
                    'recipe': entry.recipe,
                    'allergen': entry.allergen,
                    'portionSize': entry.portionSize,
                    'tax': float(entry.tax) if entry.tax is not None else None,
                    'discount': float(entry.discount) if entry.discount is not None else None,
                    'currentStock': int(entry.currentStock) if entry.currentStock is not None else None,
                    'barcode': entry.barcode,
                    'itemTotal': float(entry.itemTotal) if entry.itemTotal is not None else None,
                    'quantity': entry.quantity
                }],
                'subtotal': float(entry.subtotal),
                'tax': float(entry.tax),
                'totalDiscount': float(entry.discount) if entry.discount is not None else None,
                'id': str(entry.id),
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
    


