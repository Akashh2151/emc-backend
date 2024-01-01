from flask import Blueprint, jsonify, request
from model.billing_model import Billing
from model.resto_model import Item
from model.signInsignup_model import User


billing=Blueprint('billing',__name__)



# Create a new billing route
@billing.route('/v1/billing', methods=['POST'])
def create_billing():
    try:
        # Extract the user_id from the request headers
        user_id = request.headers.get('user_id')

        # Check if the user_id is provided
        if not user_id:
            return jsonify({'body': None, "status": "error", 'message': 'User ID is required in headers.', 'statusCode': 400}), 200

        # Get the current user
        user = User.objects.get(id=user_id)

        # Get items from the request payload
        items = request.json.get('items', [])

        # Calculate subtotal, tax, discount, and grand total
        subtotal = 0
        for item_data in items:
            item_code = item_data.get('itemCode')
            quantity = item_data.get('quantity', 1)

            # Fetch item details from the database
            item = Item.objects.get(itemCode=item_code)

            # Calculate item total
            item_total = item.itemPrice * quantity

            # Update subtotal
            subtotal += item_total

            # Add billing entry
            billing_entry = Billing(
                itemCode=item_code,
                itemName=item.itemName,
                quantity=quantity,
                itemPrice=item.itemPrice,
                itemTotal=item_total,
                creator=user
            )
            billing_entry.save()

        # Calculate tax, discount, and grand total
        tax = request.json.get('tax', 0)
        discount = request.json.get('discount', 0)
        grand_total = subtotal + tax - discount

        # Create a response object
        response_items = [{
            'itemCode': item_data.get('itemCode'),
            'itemName': item_data.get('itemName'),
            'quantity': item_data.get('quantity', 1),
            'itemTotal': item.itemPrice * item_data.get('quantity', 1)
        } for item_data in items]

        response = {
            'items': response_items,
            'subtotal': subtotal,
            'tax': tax,
            'discount': discount,
            'grandTotal': grand_total,
            'status': 'complete'  # You may update this status based on your business logic
        }

        return jsonify({'body': response, 'status': 'success', 'statusCode': 200, 'message': 'Billing created successfully'}), 200

    except Exception as e:
        return jsonify({'body': None, 'error': str(e), 'statusCode': 500}), 500