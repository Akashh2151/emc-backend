# import datetime
from json import JSONEncoder
from pymongo.errors import DuplicateKeyError
# from msilib import Table
from flask import Blueprint, app, request, jsonify 
from model.resto_model import   CustomerMaster, EmployeeMaster, History, Item,Table, ItemMaster, Order, TaxMaster, Vendor, Verification 
from mongoengine.errors import DoesNotExist

from datetime import datetime
from model.signInsignup_model import User

from security.mastervalidation import validate_no_blank_spaces

# from dateutil import parser


# restoapp blue print
restoapp = Blueprint('restoapp', __name__)





# Create an order
@restoapp.route('/v1/order', methods=['POST'])
def create_order():
    try:
        data = request.json
        user_id = request.headers.get('user_id')
        user = User.objects.get(id=user_id)
       

        vendor_code = data.get('vendorCode')
        vendor_name = data.get('vendorName')
        vendor_email = data.get('vendorEmail')
        vendor_mobile = data.get('vendorMobile') 
        vendor_addr = data.get('vendorAddr')

        if not all([vendor_code, vendor_name, vendor_email, vendor_mobile, vendor_addr]):
            response = {"Body": {}, "status": "success", "statuscode": 200, "message": 'vendorCode, vendorName, vendorEmail, vendorMobile, vendorAddr All required fields must be provided'}
            return jsonify(response), 200

        existing_order = Order.objects(vendorCode=vendor_code).first()
        if existing_order:
            response = {"Body": {}, "status": "success", "statuscode": 200, "message": 'Order with the provided vendorCode already exists.'}
            return jsonify(response), 200

        new_order = Order(
            vendorCode=vendor_code,
            vendorName=vendor_name,
            vendorEmail=vendor_email,
            vendorMobile=vendor_mobile,
            vendorAddr=vendor_addr,
            creator=user
        )
        new_order.save()
        
        res={
            "updatedOrder":data
            
        }

        response = {"Body": res, "status": "success", "statusCode": 200, "message": 'Order created'}
        return jsonify(response)

    except Exception as e:
        return jsonify({'Body':  {}, 'error': str(e), 'statusCode': 500})



# Get all orders
@restoapp.route('/v1/order', methods=['GET'])
def get_orders():
    try:
        user_id = request.headers.get('user_id')
        user = User.objects.get(id=user_id)
        orders = Order.objects(creator=user)

        orders_list = [{"vendorCode": order.vendorCode, "vendorName": order.vendorName,
                        "vendorEmail": order.vendorEmail, "vendorMobile": order.vendorMobile,
                        "vendorAddr": order.vendorAddr} for order in orders]

        response = {'Body': orders_list, 'status': 'success', 'statuscode': 200, 'message': 'Orders retrieved'}
        return jsonify(response),200

    except Exception as e:
        return jsonify({'Body': None, 'error': str(e), 'statusCode': 500})



# Update an existing order by vendorCode
@restoapp.route('/v1/order/<string:vendor_code>', methods=['PUT'])
def update_order(vendor_code):
    try:
        user_id = request.headers.get('user_id')
        user = User.objects.get(id=user_id)

        order = Order.objects(vendorCode=vendor_code, creator=user).first()
        if not order:
            response = {'Body': None, 'message': 'Order not found', 'statusCode': 404, 'status': 'error'}
            return jsonify(response)

        data = request.json

        # Validate for blank spaces in keys and values
        is_no_blank_spaces, error_message = validate_no_blank_spaces(data)
        if not is_no_blank_spaces:
            response = {"Body": None, "status": "error", "statuscode": 400, "message": error_message}
            return jsonify(response), 200

        # Update only the fields present in the request JSON
        for key in data:
            if key in order._fields:
                setattr(order, key, data[key])

        order.save()

        order_id = str(order.id)
        updated_order_details = data

        res = {
            "_id": order_id,
            "updateDetails": updated_order_details
        }

        response = {"Body": res, "status": "success", "statuscode": 200, "message": 'Order updated successfully'}
        return jsonify(response)

    except DoesNotExist:
        return jsonify({'Body': {}, 'error': 'Order not found', 'statusCode': 404}), 404
    except Exception as e:
        return jsonify({'Body': None, 'error': str(e), 'statusCode': 500})



# Get a specific order by vendorCode
@restoapp.route('/v1/order/<string:vendor_code>', methods=['GET'])
def get_order(vendor_code):
    try:
        user_id = request.headers.get('user_id')
        user = User.objects.get(id=user_id)

        order = Order.objects(vendorCode=vendor_code, creator=user).first()
        if not order:
            response = {'Body': None, 'message': 'Order not found', 'statusCode': 404, 'status': 'error'}
            return jsonify(response),200

        order_dict = {"vendorCode": order.vendorCode, "vendorName": order.vendorName,
                      "vendorEmail": order.vendorEmail, "vendorMobile": order.vendorMobile,
                      "vendorAddr": order.vendorAddr}

        response = {'Body': order_dict, 'status': 'success', 'statusCode': 200, 'message': 'Order retrieved'}
        return jsonify(response),200

    except Exception as e:
        return jsonify({'Body': None, 'error': str(e), 'statusCode': 500})




# Delete an order by vendorCode
@restoapp.route('/v1/order/<string:vendor_code>', methods=['DELETE'])
def delete_order(vendor_code):
    try:
        user_id = request.headers.get('user_id')
        user = User.objects.get(id=user_id)

        order = Order.objects(vendorCode=vendor_code, creator=user).first()
        if not order:
            response = {'Body': None, 'message': 'Order not found', 'statusCode': 404, 'status': 'error'}
            return jsonify(response)

        order.delete()

        response = {'Body': None, 'status': 'success', 'statusCode': 200, 'message': 'Order deleted'}
        return jsonify(response)

    except Exception as e:
        return jsonify({'Body': None, 'error': str(e), 'statusCode': 500})





# __

# Create an item master
@restoapp.route('/v1/itemmaster', methods=['POST'])
def create_item_master():
    try:
        data = request.json
        name = data.get('name')
        description = data.get('description')
        measure_unit = data.get('measureUnit')
        price = data.get('price')
        category = data.get('category')
        sub_category = data.get('subCategory')
        nutrition = data.get('nutrition')
        
        # Validate for blank spaces in keys and values
        is_no_blank_spaces, error_message = validate_no_blank_spaces(data)
        if not is_no_blank_spaces:
            response = {"Body": None, "status": "error", "statuscode": 400, "message": error_message}
            return jsonify(response), 200

        # Add creator to the data
        user_id = request.headers.get('user_id')
        user = User.objects.get(id=user_id)

        new_item = ItemMaster(
            name=name,
            description=description,
            measureUnit=measure_unit,
            price=price,
            category=category,
            subCategory=sub_category,
            nutrition=nutrition,
            creator=user
        )
        new_item.save()
        
        res={
            "updateditemmaster":data
        }

        response = {"Body": res, "status": "success", "statuscode": 200, "message": 'Item created successfully'}
        return jsonify(response), 200

    except Exception as e:
        return jsonify({'Body': None, 'error': str(e), 'statuscode': 500})



# Get all item masters
@restoapp.route('/v1/itemmaster', methods=['GET'])
def get_all_item_masters():
    try:
        # Extract the user_id from the request headers
        user_id = request.headers.get('user_id')

        # Check if the user_id is provided
        if not user_id:
            return jsonify({'Body': None, 'status': 'error', 'message': 'User ID is required in headers.', 'statuscode': 400}), 200

        # Get the current user
        user = User.objects.get(id=user_id)

        # Get all item masters associated with the user
        item_masters = ItemMaster.objects(creator=user)

        response_items = []

        for item_master in item_masters:
            response_item = {
                "name": item_master.name,
                "description": item_master.description,
                "measureUnit": item_master.measureUnit,
                "price": item_master.price,
                "category": item_master.category,
                "subCategory": item_master.subCategory,
                "nutrition": item_master.nutrition
            }
            response_items.append(response_item)

        response = {'Body': response_items, 'status': 'success', 'statuscode': 200, 'message': 'Item masters retrieved successfully'}
        return jsonify(response), 200

    except Exception as e:
        return jsonify({'Body': None, 'error': str(e), 'statuscode': 500})




# Get a specific item master by name
@restoapp.route('/v1/itemmaster/<string:item_name>', methods=['GET'])
def get_item_master(item_name):
    try:
        user_id = request.headers.get('user_id')
        user = User.objects.get(id=user_id)

        item = ItemMaster.objects(name=item_name, creator=user).first()
        if not item:
            response = {'Body': None, 'error': 'Item not found', 'statuscode': 404}
            return jsonify(response), 404

        item_dict = {
            "name": item.name,
            "description": item.description,
            "measureUnit": item.measureUnit,
            "price": item.price,
            "category": item.category,
            "subCategory": item.subCategory,
            "nutrition": item.nutrition
        }

        response = {'Body': item_dict, 'status': 'success', 'statuscode': 200, 'message': 'Item retrieved successfully'}
        return jsonify(response), 200

    except Exception as e:
        return jsonify({'Body': None, 'error': str(e), 'statuscode': 500})




# Update an item master by name
@restoapp.route('/v1/itemmaster/<string:item_name>', methods=['PUT'])
def update_item_master(item_name):
    try:
        data = request.json
        user_id = request.headers.get('user_id')
        user = User.objects.get(id=user_id)

        item = ItemMaster.objects(name=item_name, creator=user).first()
        if not item:
            response = {'Body': None, 'error': 'Item not found', 'statuscode': 404}
            return jsonify(response), 404

        # Validate for blank spaces in keys and values
        is_no_blank_spaces, error_message = validate_no_blank_spaces(data)
        if not is_no_blank_spaces:
            response = {"Body": None, "status": "error", "statuscode": 400, "message": error_message}
            return jsonify(response), 200

        # Update item master attributes
        for key, value in data.items():
            setattr(item, key, value)

        item.save()
        
        res={
            "masteriteam":data
        }

        response = {'Body': res, 'status': 'success', 'statuscode': 200, 'message': 'Item updated successfully'}
        return jsonify(response), 200

    except Exception as e:
        return jsonify({'Body': None, 'error': str(e), 'statuscode': 500})


# Delete an item master by name
@restoapp.route('/v1/itemmaster/<string:item_name>', methods=['DELETE'])
def delete_item_master(item_name):
    try:
        user_id = request.headers.get('user_id')
        user = User.objects.get(id=user_id)

        item = ItemMaster.objects(name=item_name, creator=user).first()
        if not item:
            response = {'Body': None, 'error': 'Item not found', 'statuscode': 404}
            return jsonify(response), 404

        item.delete()

        response = {'Body': None, 'status': 'success', 'statuscode': 200, 'message': 'Item deleted successfully'}
        return jsonify(response), 200

    except Exception as e:
        return jsonify({'Body': None, 'error': str(e), 'statuscode': 500})




#__


# Create TaxMaster
@restoapp.route('/v1/tax', methods=['POST'])
def create_tax():
    try:
        data = request.json
        tax_name = data.get('taxName')

        # Validation: Check if taxName is provided
        if not tax_name:
            response = {"Body": None, "status": "error", "statusCode": 400, "message": 'TaxName is required'}
            return jsonify(response), 200

        user_id = request.headers.get('user_id')
        user = User.objects.get(id=user_id)

        new_tax = TaxMaster(taxName=tax_name, creator=user)
        new_tax.save()

        response = {"Body": None, "status": "success", "statusCode": 200, "message": 'Tax created'}
        return jsonify(response)

    except Exception as e:
        return jsonify({'Body': None, 'error': str(e), 'statusCode': 500})


# Get all taxes
@restoapp.route('/v1/tax', methods=['GET'])
def get_taxes():
    try:
        user_id = request.headers.get('user_id')
        user = User.objects.get(id=user_id)

        taxes = TaxMaster.objects(creator=user)
        taxes_list = [{"taxName": tax.taxName} for tax in taxes]

        response = {'Body': taxes_list, 'status': 'success', 'statusCode': 200, 'message': 'Taxes retrieved'}
        return jsonify(response)

    except Exception as e:
        return jsonify({'Body': None, 'error': str(e), 'statusCode': 500})


# Update TaxMaster by taxName
@restoapp.route('/v1/tax/<string:tax_name>', methods=['PUT'])
def update_tax(tax_name):
    try:
        user_id = request.headers.get('user_id')
        user = User.objects.get(id=user_id)

        tax = TaxMaster.objects(creator=user, taxName=tax_name).first()
        if not tax:
            response = {'Body': None, 'message': 'Tax not found', 'statusCode': 404, 'status': 'error'}
            return jsonify(response)

        data = request.json

        # Validate key-value pairs
        is_no_blank_spaces, error_message = validate_no_blank_spaces(data)
        if not is_no_blank_spaces:
            response = {"Body": None, "status": "error", "statuscode": 400, "message": error_message}
            return jsonify(response), 200


        # Validate if the taxName is present in the request JSON
        if 'taxName' in data:
            response = {'Body': None, 'status': 'error', 'statusCode': 400, 'message': 'Cannot update taxName'}
            return jsonify(response)

        # Update only the fields present in the request JSON
        for key, value in data.items():
            setattr(tax, key, value)

        tax.save()
        
        res={
            "updatetax":data
        }

        response = {'Body': res, 'status': 'success', 'statusCode': 200, 'message': 'Tax updated'}
        return jsonify(response)

    except Exception as e:
        return jsonify({'Body': None, 'error': str(e), 'statusCode': 500})
    


# Get a specific tax by taxName
@restoapp.route('/v1/tax/<string:tax_name>', methods=['GET'])
def get_tax(tax_name):
    try:
        user_id = request.headers.get('user_id')
        user = User.objects.get(id=user_id)

        tax = TaxMaster.objects(creator=user, taxName=tax_name).first()
        if not tax:
            response = {'Body': None, 'message': 'Tax not found', 'statusCode': 404, 'status': 'error'}
            return jsonify(response)

        tax_dict = {"taxName": tax.taxName}

        response = {'Body': tax_dict, 'status': 'success', 'statusCode': 200, 'message': 'Tax retrieved'}
        return jsonify(response)

    except Exception as e:
        return jsonify({'Body': None, 'error': str(e), 'statusCode': 500})


# Delete TaxMaster by taxName
@restoapp.route('/v1/tax/<string:tax_name>', methods=['DELETE'])
def delete_tax(tax_name):
    try:
        user_id = request.headers.get('user_id')
        user = User.objects.get(id=user_id)

        tax = TaxMaster.objects(creator=user, taxName=tax_name).first()
        if not tax:
            response = {'Body': None, 'message': 'Tax not found', 'statusCode': 404, 'status': 'error'}
            return jsonify(response)

        tax.delete()

        response = {'Body': None, 'status': 'success', 'statusCode': 200, 'message': 'Tax deleted'}
        return jsonify(response)

    except Exception as e:
        return jsonify({'Body': None, 'error': str(e), 'statusCode': 500})


# --
# Custom JSON Encoder for History and datetime objects
class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, History):
            return {'date': obj.date, 'action': obj.action}
        elif isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        return super().default(obj)

# Set the custom JSON encoder for the app
restoapp.json_encoder = CustomJSONEncoder


@restoapp.route('/customer', methods=['POST'])
def create_customer():
    try:
        data = request.json
        customerName = data.get('customerName')
        customerMobile = data.get('customerMobile')
        customerEmail = data.get('customerEmail')
        customerLastVisit = datetime.strptime(data.get('customerLastVisit'), '%Y-%m-%dT%H:%M:%S.%fZ')
        customerAddr = data.get('customerAddr')
        customerHistory = [History(date=datetime.strptime(hist['date'], '%Y-%m-%dT%H:%M:%S.%fZ'), action=hist['action']) for hist in data.get('customerHistory', [])]

        new_customer = CustomerMaster(
            customerName=customerName,
            customerMobile=customerMobile,
            customerEmail=customerEmail,
            customerLastVisit=customerLastVisit,
            customerAddr=customerAddr,
            customerHistory=customerHistory
        )
        new_customer.save()

        response = {"Body": None, "status": "success", "statusCode": 200, "message": 'Customer created'}
        return jsonify(response)

    except Exception as e:
        return jsonify({'Body': None, 'error': str(e), 'statusCode': 500})
    
    

# Get all customers
@restoapp.route('/customer', methods=['GET'])
def get_customers():
    try:
        customers = CustomerMaster.objects()
        customers_list = [{"customerName": customer.customerName,
                           "customerMobile": customer.customerMobile,
                           "customerEmail": customer.customerEmail,
                           "customerLastVisit": customer.customerLastVisit,
                           "customerAddr": customer.customerAddr,
                           "customerHistory": customer.customerHistory} for customer in customers]

        response = {'Body': customers_list, 'status': 'success', 'statusCode': 200, 'message': 'Customers retrieved'}
        return jsonify(response)

    except Exception as e:
        return jsonify({'Body': None, 'error': str(e), 'statusCode': 500})

# Update customer route
@restoapp.route('/customer/<customer_id>', methods=['PUT'])
def update_customer(customer_id):
    try:
        data = request.json
        # Find the customer by ID
        customer = CustomerMaster.objects.get(id=customer_id)

        # Update customer fields
        customer.customerName = data.get('customerName', customer.customerName)
        customer.customerMobile = data.get('customerMobile', customer.customerMobile)
        customer.customerEmail = data.get('customerEmail', customer.customerEmail)
        customer.customerLastVisit = datetime.strptime(data.get('customerLastVisit'), '%Y-%m-%dT%H:%M:%S.%fZ')
        customer.customerAddr = data.get('customerAddr', customer.customerAddr)
        customer.customerHistory = [History(date=datetime.strptime(hist['date'], '%Y-%m-%dT%H:%M:%S.%fZ'), action=hist['action']) for hist in data.get('customerHistory', [])]

        customer.save()

        response = {"Body": None, "status": "success", "statusCode": 200, "message": 'Customer updated'}
        return jsonify(response)

    except Exception as e:
        return jsonify({'Body': None, 'error': str(e), 'statusCode': 500})



# Delete customer route
@restoapp.route('/customer/<customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    try:
        # Find the customer by ID and delete
        CustomerMaster.objects.get(id=customer_id).delete()

        response = {"Body": None, "status": "success", "statusCode": 200, "message": 'Customer deleted'}
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'Body': None, 'error': str(e), 'statusCode': 500})
    
    
# --
 

# Create EmployeeMaster
@restoapp.route('/employee', methods=['POST'])
def create_employee():
    try:
        data = request.json
        employeeName = data.get('employeeName')
        employeeMobile = data.get('employeeMobile')
        employeeEmail = data.get('employeeEmail')
        employeeAddr = data.get('employeeAddr')
        employeeHistory = data.get('employeeHistory', [])
        employeeVerification = data.get('employeeVerification', [])

        new_employee = EmployeeMaster(
            employeeName=employeeName,
            employeeMobile=employeeMobile,
            employeeEmail=employeeEmail,
            employeeAddr=employeeAddr,
            employeeHistory=employeeHistory,
            employeeVerification=employeeVerification
        )
        new_employee.save()

        response = {"Body": None, "status": "success", "statusCode": 200, "message": 'Employee created'}
        return jsonify(response)

    except Exception as e:
        return jsonify({'Body': None, 'error': str(e), 'statusCode': 500})


# Custom JSON Encoder for History, Verification, and datetime objects
class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, History):
            return {'date': obj.date, 'action': obj.action}
        elif isinstance(obj, Verification):
            return {'date': obj.date, 'status': obj.status, 'comments': obj.comments}
        elif isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        return super().default(obj)

# Set the custom JSON encoder for the app
restoapp.json_encoder = CustomJSONEncoder

# Get all employees
@restoapp.route('/employee', methods=['GET'])
def get_employees():
    try:
        employees = EmployeeMaster.objects()
        employees_list = [{"employeeName": employee.employeeName,
                            "employeeMobile": employee.employeeMobile,
                            "employeeEmail": employee.employeeEmail,
                            "employeeAddr": employee.employeeAddr,
                            "employeeHistory": employee.employeeHistory,
                            "employeeVerification": employee.employeeVerification} for employee in employees]

        response = {'Body': employees_list, 'status': 'success', 'statusCode': 200, 'message': 'Employees retrieved'}
        return jsonify(response)

    except Exception as e:
        return jsonify({'Body': None, 'error': str(e), 'statusCode': 500})



@restoapp.route('/employee/<employee_id>', methods=['PUT'])
def update_employee(employee_id):
    try:
        data = request.json
        employee = EmployeeMaster.objects.get(id=employee_id)

        # Update employee attributes
        employee.employeeName = data.get('employeeName', employee.employeeName)
        employee.employeeMobile = data.get('employeeMobile', employee.employeeMobile)
        employee.employeeEmail = data.get('employeeEmail', employee.employeeEmail)
        employee.employeeAddr = data.get('employeeAddr', employee.employeeAddr)
        
        # Update employee history if provided
        employee_history = data.get('employeeHistory', [])
        if employee_history:
            employee.employeeHistory = [
                History(date=datetime.strptime(hist['date'], '%Y-%m-%dT%H:%M:%S.%fZ'), action=hist['action']) 
                for hist in employee_history
            ]

        # Update employee verification if provided
        employee_verification = data.get('employeeVerification', [])
        if employee_verification:
            employee.employeeVerification = [
                Verification(date=datetime.strptime(verif['date'], '%Y-%m-%dT%H:%M:%S.%fZ'), 
                             status=verif['status'], 
                             comments=verif['comments'])
                for verif in employee_verification
            ]

        # Save the updated employee
        employee.save()

        response = {"Body": None, "status": "success", "statusCode": 200, "message": 'Employee updated'}
        return jsonify(response)

    except DoesNotExist:
        return jsonify({'Body': None, 'error': 'Employee not found', 'statusCode': 404})
    except Exception as e:
        return jsonify({'Body': None, 'error': str(e), 'statusCode': 500})


# Delete an employee
@restoapp.route('/employee/<employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    try:
        employee = EmployeeMaster.objects.get(id=employee_id)
        employee.delete()

        response = {"Body": None, "status": "success", "statusCode": 200, "message": 'Employee deleted'}
        return jsonify(response)

    except DoesNotExist:
        return jsonify({'Body': None, 'error': 'Employee not found', 'statusCode': 404})
    except Exception as e:
        return jsonify({'Body': None, 'error': str(e), 'statusCode': 500})
    
    

# __
@restoapp.route('/v1/item', methods=['POST'])
def create_item():
    try:
        # Extract the user_id from the request headers
        user_id = request.headers.get('user_id')

        # Check if the user_id is provided
        if not user_id:
            return jsonify({'Body': None, "status": "error", 'message': 'User ID is required in headers.', 'statuscode': 400}), 200

        # Get the current user
        user = User.objects.get(id=user_id)

        data = request.json
        item_code = data.get('itemCode')
        item_name = data.get('itemName')
        item_price = data.get('itemPrice')

        # Check if the required fields are provided
        if item_code is None or item_name is None or item_price is None:
            return jsonify({'Body': None, "status": "error", 'message': 'itemCode, itemName, and itemPrice are required fields.', 'statuscode': 400}), 200

        existing_item = Item.objects(itemCode=item_code).first()
        if existing_item:
            return jsonify({'Body': None, "status": "error", 'message': 'Item with the provided itemCode already exists.', 'statuscode': 400}), 200

        new_item = Item(
            itemCode=item_code,
            itemName=item_name,
            itemPrice=item_price,
            # Set other fields to default values if not provided
            itemCategory=data.get('itemCategory', None),
            itemSubCategory=data.get('itemSubCategory', None),
            ingredients=data.get('ingredients', None),
            recipe=data.get('recipe', None),
            allergen=data.get('allergen', None),
            portionSize=data.get('portionSize', None),
            status=data.get('status', None),
            tax=data.get('tax', None),
            discount=data.get('discount', None),
            currentStock=data.get('currentStock', None),
            barcode=data.get('barcode', None),
            creator=user
        )

        # Validate for blank spaces in keys and values
        is_no_blank_spaces, error_message = validate_no_blank_spaces(request.json)
        if not is_no_blank_spaces:
            response = {"Body": None, "status": "error", "statusCode": 400, "message": error_message}
            return jsonify(response), 200

        # Save the new item
        new_item.save()

        # updatedetails = {
           
            # Include other fields as needed
        # }

        response = {"Body": data, "status": "success", "statuscode": 200, "message": 'Item created successfully'}
        return jsonify(response), 200

    except Exception as e:
        return jsonify({'Body': None, 'error': str(e), 'statusCode': 500})



# Get all items
@restoapp.route('/v1/item', methods=['GET'])
def get_all_items():
    try:
        # Extract the user_id from the request headers
        user_id = request.headers.get('user_id')

        # Check if the user_id is provided
        if not user_id:
            return jsonify({'Body': None, "status": "error", 'message': 'User ID is required in headers.', 'statuscode': 400}), 200

        # Get the current user
        user = User.objects.get(id=user_id)

        # Get all items associated with the user
        items = Item.objects(creator=user)

        response_items = []
        
        for item in items:
            response_item = {
               "itemCode": str(item.itemCode) if item.itemCode else None,
                "itemName": item.itemName,
                "itemCategory": item.itemCategory,
                "itemSubCategory": item.itemSubCategory,
                "itemPrice": float(item.itemPrice) if item.itemPrice is not None else None,
                "ingredients": item.ingredients,
                "recipe": item.recipe,
                "allergen": item.allergen,
                "portionSize": item.portionSize,
                "status": item.status,
                "tax": float(item.tax) if item.tax is not None else None,
                "discount": float(item.discount) if item.discount is not None else None,
                "currentStock": item.currentStock,
                "barcode": item.barcode,
            }
            response_items.append(response_item)

        response = {'Body': response_items, 'status': 'success', 'statuscode': 200, 'message': 'Items retrieved successfully'}
        return jsonify(response), 200

    except Exception as e:
        return jsonify({'Body': None, 'error': str(e), 'statusCode': 500})
    
    


    
 # Get a specific item by itemCode
@restoapp.route('/v1/item/<item_code>', methods=['GET'])
def get_byitemcode(item_code):
    try:
        print(f"Attempting to find item with code: {item_code}")
        item = Item.objects.get(itemCode=item_code)
        print(f"Found item: {item}")
        

        item_data = {
                "itemCode": str(item.itemCode) if item.itemCode else None,
                "itemName": item.itemName,
                "itemCategory": item.itemCategory,
                "itemSubCategory": item.itemSubCategory,
                "itemPrice": float(item.itemPrice) if item.itemPrice is not None else None,
                "ingredients": item.ingredients,
                "recipe": item.recipe,
                "allergen": item.allergen,
                "portionSize": item.portionSize,
                "status": item.status,
                "tax": float(item.tax) if item.tax is not None else None,
                "discount": float(item.discount) if item.discount is not None else None,
                # "images": item.images,
                "currentStock": item.currentStock,
                "barcode": item.barcode,
                # "salesHistory": [{"date": entry.date, "action": entry.action} for entry in item.salesHistory],
                # "customNotes": item.customNotes
        }

        response = {'Body': item_data, 'status': 'success', 'statuscode': 200, 'message': 'Item retrieved successfully'}
        return jsonify(response),200

    except Item.DoesNotExist:
        print(f"Item with code {item_code} not found.")
        return jsonify({'Body': None, 'error': 'Item not found', 'statusCode': 404})
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return jsonify({'Body': None, 'error': str(e), 'statusCode': 500})



 
 
 # Update an item by itemCode
from datetime import datetime
from flask import jsonify

# Assuming you have the rest of the necessary imports and setup

@restoapp.route('/v1/item/<item_code>', methods=['PUT'])
def update_items(item_code):
    try:
        data = request.json
        item = Item.objects.get(itemCode=item_code)

        # Update item attributes
        item.itemName = data.get('itemName', item.itemName)
        item.itemCategory = data.get('itemCategory', item.itemCategory)
        item.itemSubCategory = data.get('itemSubCategory', item.itemSubCategory)
        item.itemPrice = data.get('itemPrice', item.itemPrice)
        item.ingredients = data.get('ingredients', item.ingredients)
        item.recipe = data.get('recipe', item.recipe)
        item.allergen = data.get('allergen', item.allergen)
        item.portionSize = data.get('portionSize', item.portionSize)
        item.status = data.get('status', item.status)
        item.tax = data.get('tax', item.tax)
        item.discount = data.get('discount', item.discount)
        # item.images = data.get('images', item.images)
        item.currentStock = data.get('currentStock', item.currentStock)
        item.barcode = data.get('barcode', item.barcode)
       
        # Validate for blank spaces in keys and values
        is_no_blank_spaces, error_message = validate_no_blank_spaces(request.json)
        if not is_no_blank_spaces:
            response = {"Body": None, "status": "error", "statuscode": 400, "message": error_message}
            return jsonify(response), 200
        
        item.save()
        
        userid=str(item.id)
        updatediteamdetail=request.json
        
        res={
            "_id":userid,
            "updateDetails":updatediteamdetail
        }

        response = {"Body": res, "status": "success", "statuscode": 200, "message": 'Item updated successfully'}
        return jsonify(response),200
    
    except DoesNotExist:
        return jsonify({'Body': {}, 'error': 'Item not found', 'statusCode': 404}),404
    except Exception as e:
        return jsonify({'Body': {}, 'error': str(e), 'statusCode': 500})

 
 

# Delete an item by itemCode
@restoapp.route('/v1/item/<item_code>', methods=['DELETE'])
def delete_item(item_code):
    try:
        item = Item.objects.get(itemCode=item_code)
        item.delete()

        response = {"Body": {}, "status": "success", "statuscode": 200, "message": 'Item deleted successfully'}
        return jsonify(response)

    except DoesNotExist:
        return jsonify({'Body': {}, 'error': 'Item not found', 'statuscode': 404})
    except Exception as e:
        return jsonify({'Body': {}, 'error': str(e), 'statusCode': 500})




# __
 
 
@restoapp.route('/v1/table', methods=['POST'])
def create_table():
    try:
        data = request.json
        table_code = data.get('tableCode')
        table_name = data.get('tableName')
        table_status = data.get('tableStatus')
        table_placement = data.get('tablePlacement')
        table_qr = data.get('tableQR')

        if not table_code or not table_name or not table_status or not table_placement or not table_qr:
            response = {'Body': None, "status": "error", 'statusCode': 400, 'message': 'All fields are required'}
            return jsonify(response),200

        existing_table = Table.objects(tableCode=table_code).first()

        if existing_table:
            return jsonify({'Body': None, "status": "error", 'message': 'Table with the provided tableCode already exists.', 'statuscode': 400}), 200

        new_table = Table(
            tableCode=table_code,
            tableName=table_name,
            tableStatus=table_status,
            tablePlacement=table_placement,
            tableQR=table_qr
        )

        # Validate for blank spaces in keys and values
        is_no_blank_spaces, error_message = validate_no_blank_spaces(request.json)
        if not is_no_blank_spaces:
            response = {"Body": None, "status": "error", "statusCode": 400, "message": error_message}
            return jsonify(response), 200

        new_table.save()

        response = {"Body": {}, "status": "success", "statusCode": 200, "message": 'Table created successfully'}
        return jsonify(response), 200

    except Exception as e:
        return jsonify({'Body': None, 'error': str(e), 'statusCode': 500})


@restoapp.route('/v1/table', methods=['GET'])
def get_all_tables():
    try:
        tables = Table.objects()

        response_tables = [{"tableCode": table.tableCode, "tableName": table.tableName,
                             "tableStatus": table.tableStatus, "tablePlacement": table.tablePlacement,
                             "tableQR": table.tableQR} for table in tables]

        response = {'Body': response_tables, 'status': 'success', 'statuscode': 200, 'message': 'Tables retrieved successfully'}
        return jsonify(response), 200

    except Exception as e:
        return jsonify({'Body': None, 'error': str(e), 'statusCode': 500})



@restoapp.route('/v1/table/<table_code>', methods=['GET'])
def get_table_by_code(table_code):
    try:
        table = Table.objects.get(tableCode=table_code)

        table_data = {
            "tableCode": table.tableCode,
            "tableName": table.tableName,
            "tableStatus": table.tableStatus,
            "tablePlacement": table.tablePlacement,
            "tableQR": table.tableQR
        }

        response = {'Body': table_data, 'status': 'success', 'statuscode': 200, 'message': 'Table retrieved successfully'}
        return jsonify(response), 200

    except DoesNotExist:
        return jsonify({'Body': None, 'error': 'Table not found', 'statusCode': 404}), 404
    except Exception as e:
        return jsonify({'Body': None, 'error': str(e), 'statusCode': 500})


@restoapp.route('/v1/table/<table_code>', methods=['PUT'])
def update_table(table_code):
    try:
        data = request.json
        table = Table.objects.get(tableCode=table_code)

        table.tableName = data.get('tableName', table.tableName)
        table.tableStatus = data.get('tableStatus', table.tableStatus)
        table.tablePlacement = data.get('tablePlacement', table.tablePlacement)
        table.tableQR = data.get('tableQR', table.tableQR)

        # Validate for blank spaces in keys and values
        is_no_blank_spaces, error_message = validate_no_blank_spaces(request.json)
        if not is_no_blank_spaces:
            response = {"Body": None, "status": "error", "statuscode": 400, "message": error_message}
            return jsonify(response), 200

        table.save()
        
       

        response = {"Body": data, "status": "success", "statuscode": 200, "message": 'Table updated successfully'}
        return jsonify(response), 200

    except DoesNotExist:
        return jsonify({'Body': None, 'error': 'Table not found', 'statusCode': 404}), 404
    except Exception as e:
        return jsonify({'Body': None, 'error': str(e), 'statusCode': 500})




@restoapp.route('/v1/table/<table_code>', methods=['DELETE'])
def delete_table(table_code):
    try:
        table = Table.objects.get(tableCode=table_code)
        table.delete()

        response = {"Body": None, "status": "success", "statuscode": 200, "message": 'Table deleted successfully'}
        return jsonify(response), 200

    except DoesNotExist:
        return jsonify({'Body': None, 'error': 'Table not found', 'statuscode': 404}), 404
    except Exception as e:
        return jsonify({'Body': None, 'error': str(e), 'statusCode': 500})
    





@restoapp.route('/v1/vendors', methods=['POST'])
def create_vendor():
    try:
        data = request.json
        vendor_code = data.get('vendorCode')
        vendor_name = data.get('vendorName')
        vendor_email = data.get('vendorEmail')
        vendor_mobile = data.get('vendorMobile')
        vendor_addr = data.get('vendorAddr')

        if not vendor_code or not vendor_name or not vendor_email or not vendor_mobile or not vendor_addr:
            response = {'Body': None, "status": "error", 'statusCode': 400, 'message': 'All fields are required'}
            return jsonify(response), 400

        existing_vendor = Vendor.objects(vendorCode=vendor_code).first()

        if existing_vendor:
            return jsonify({'Body': None, "status": "error", 'message': 'Vendor with the provided vendorCode already exists.', 'statuscode': 400}), 200

        new_vendor = Vendor(
            vendorCode=vendor_code,
            vendorName=vendor_name,
            vendorEmail=vendor_email,
            vendorMobile=vendor_mobile,
            vendorAddr=vendor_addr
        )

        # Validate for blank spaces in keys and values
        is_no_blank_spaces, error_message = validate_no_blank_spaces(request.json)
        if not is_no_blank_spaces:
            response = {"Body": None, "status": "error", "statusCode": 400, "message": error_message}
            return jsonify(response), 200

        new_vendor.save()

        response = {"Body":  {}, "status": "success", "statusCode": 200, "message": 'Vendor created successfully'}
        return jsonify(response), 200

    except Exception as e:
        return jsonify({'Body': None, 'error': str(e), 'statusCode': 500})


@restoapp.route('/v1/vendors', methods=['GET'])
def get_all_vendors():
    try:
        vendors = Vendor.objects()

        response_vendors = [{"vendorCode": vendor.vendorCode, "vendorName": vendor.vendorName,
                             "vendorEmail": vendor.vendorEmail, "vendorMobile": vendor.vendorMobile,
                             "vendorAddr": vendor.vendorAddr} for vendor in vendors]

        response = {'Body': response_vendors, 'status': 'success', 'statuscode': 200, 'message': 'Vendors retrieved successfully'}
        return jsonify(response), 200

    except Exception as e:
        return jsonify({'Body': None, 'error': str(e), 'statusCode': 500})


@restoapp.route('/v1/vendors/<vendor_code>', methods=['GET'])
def get_vendor_by_code(vendor_code):
    try:
        vendor = Vendor.objects.get(vendorCode=vendor_code)

        vendor_data = {
            "vendorCode": vendor.vendorCode,
            "vendorName": vendor.vendorName,
            "vendorEmail": vendor.vendorEmail,
            "vendorMobile": vendor.vendorMobile,
            "vendorAddr": vendor.vendorAddr
        }

        response = {'Body': vendor_data, 'status': 'success', 'statuscode': 200, 'message': 'Vendor retrieved successfully'}
        return jsonify(response), 200

    except DoesNotExist:
        return jsonify({'Body': None, 'error': 'Vendor not found', 'statusCode': 404}), 404
    except Exception as e:
        return jsonify({'Body': None, 'error': str(e), 'statusCode': 500})


@restoapp.route('/v1/vendors/<vendor_code>', methods=['PUT'])
def update_vendor(vendor_code):
    try:
        data = request.json
        vendor = Vendor.objects.get(vendorCode=vendor_code)

        vendor.vendorName = data.get('vendorName', vendor.vendorName)
        vendor.vendorEmail = data.get('vendorEmail', vendor.vendorEmail)
        vendor.vendorMobile = data.get('vendorMobile', vendor.vendorMobile)
        vendor.vendorAddr = data.get('vendorAddr', vendor.vendorAddr)

        # Validate for blank spaces in keys and values
        is_no_blank_spaces, error_message = validate_no_blank_spaces(request.json)
        if not is_no_blank_spaces:
            response = {"Body": None, "status": "error", "statuscode": 400, "message": error_message}
            return jsonify(response), 200

        vendor.save()

        response = {"Body": None, "status": "success", "statuscode": 200, "message": 'Vendor updated successfully'}
        return jsonify(response), 200

    except DoesNotExist:
        return jsonify({'Body': None, 'error': 'Vendor not found', 'statusCode': 404}), 404
    except Exception as e:
        return jsonify({'Body': None, 'error': str(e), 'statusCode': 500})


@restoapp.route('/v1/vendors/<vendor_code>', methods=['DELETE'])
def delete_vendor(vendor_code):
    try:
        vendor = Vendor.objects.get(vendorCode=vendor_code)
        vendor.delete()

        response = {"Body": None, "status": "success", "statuscode": 200, "message": 'Vendor deleted successfully'}
        return jsonify(response), 200

    except DoesNotExist:
        return jsonify({'Body': None, 'error': 'Vendor not found', 'statuscode': 404}), 404
    except Exception as e:
        return jsonify({'Body': None, 'error': str(e), 'statusCode': 500})
















# # _______________________________________________________________________________________________________________________________________
# # CREATE
# @restoapp.route('/api/v1', methods=['POST'])
# def create_menumaster():
#     try:
#         data = request.json
#         vendorCode = data.get('vendorCode')
#         vendorName = data.get('vendorName')
#         vendorEmail = data.get('vendorEmail')
#         vendorMobile = data.get('vendorMobile')
#         vendorAddr = data.get('vendorAddr')
#         print(vendorCode)

#         # if not vendorCode or not vendorName or not vendorEmail or not vendorMobile or not vendorAddr:
#         #     response = {'Body': None, 'message': 'All fields are required', 'statusCode': 400, 'status': 'error'}
#         #     return jsonify(response)

#         user = Order(vendorCode=vendorCode, vendorName=vendorName, vendorEmail=vendorEmail,
#                      vendorMobile=vendorMobile, vendorAddr=vendorAddr)
#         user.save()

#         response = {"Body": None, "status": "success", "statusCode": 200, "message": 'MenuMaster created'}
#         return jsonify(response)

#     except Exception as e:
#         return jsonify({'error': str(e), 'status_code': 500}), 500



# # UPDATE
# @restoapp.route('/api/menumasters/update/<string:menumaster_id>', methods=['PUT'])
# def update_menumaster(menumaster_id):
#     try:
#         object_id = ObjectId(menumaster_id)
#         menumaster = MenuMaster.objects(id=object_id).first()

#         if not menumaster:
#             return jsonify({'error': 'MenuMaster not found', 'status_code': 404}), 404

#         data = request.json

#         # Validate that at least one field is present in the request
#         if not any(field in data for field in ['showName', 'path', 'subMenu']):
#             return jsonify({'error': 'At least one field (showName, path, or subMenu) is required', 'status_code': 400}), 400

#         # Update each field individually, filtering out null values
#         for key, value in data.items():
#             if value is not None:
#                 setattr(menumaster, key, value)

#         menumaster.save()

#         response = {"Body": None, "status": "success", "statusCode": 200, "message": 'MenuMaster updated'}
#         return jsonify(response)

#     except (ValidationError, InvalidDocument) as e:
#         return jsonify({'error': str(e), 'status_code': 400}), 400
#     except Exception as e:
#         return jsonify({'error': str(e), 'status_code': 500}), 500


# # READ
# @restoapp.route('/api/menumasters/<string:menumaster_id>', methods=['GET'])
# def get_menumaster(menumaster_id):
#     try:
#         object_id = ObjectId(menumaster_id)
#         menumaster = MenuMaster.objects(id=object_id).first()

#         if menumaster:
#             response = {
#                 "id": str(menumaster.id),
#                 "showName": menumaster.showName,
#                 "path": menumaster.path,
#                 "subMenu": menumaster.subMenu  # Include the new field
#             }
#             return jsonify({"status_code": 200, "message": "Success", "data": response}), 200
#         else:
#             return jsonify({'error': 'MenuMaster not found', 'status_code': 404}), 404

#     except Exception as e:
#         return jsonify({'error': str(e), 'status_code': 500}), 500



# # DELETE
# @restoapp.route('/api/menumasters/delete/<string:menumaster_id>', methods=['DELETE'])
# def delete_menumaster(menumaster_id):
#     try:
#         object_id = ObjectId(menumaster_id)
#         menumaster = MenuMaster.objects(id=object_id).first()

#         if menumaster:
#             menumaster.delete()
#             response = {"Body": None, "status": "success", "statusCode": 200, "message": 'MenuMaster deleted'}
#             return jsonify(response)
#         else:
#             return jsonify({'error': 'MenuMaster not found', 'status_code': 404}), 404

#     except Exception as e:
#         return jsonify({'error': str(e), 'status_code': 500}), 500

# # _______________________________________________________________________________________________________________________________________
# # CREATE
# @restoapp.route('/api/sellmasters/create', methods=['POST'])
# def create_sellmaster():
#     try:
#         data = request.json
#         showName = data.get('showName')
#         status = data.get('status')
#         sellUnits = data.get('sellUnits')
#         printers = data.get('printers')
#         sellType = data.get('sellType')

#         if not all([showName, status, sellUnits, printers, sellType]):
#             return jsonify({'error': 'All fields are required', 'status_code': 400}), 400

#         existing_sellmaster = RestoSellMaster.objects(showName=showName).first()
#         if existing_sellmaster:
#             return jsonify({'error': 'SellMaster with the same showName already exists', 'status_code': 400}), 400

#         sellmaster = RestoSellMaster(showName=showName, status=status, sellUnits=sellUnits, printers=printers, sellType=sellType)
#         sellmaster.save()

#         response = {"Body": None, "status": "success", "statusCode": 200, "message": 'SellMaster created'}
#         return jsonify(response)

#     except Exception as e:
#         return jsonify({'error': str(e), 'status_code': 500}), 500


# # READ
# @restoapp.route('/api/sellmasters/<string:sellmaster_id>', methods=['GET'])
# def get_sellmaster(sellmaster_id):
#     try:
#         object_id = ObjectId(sellmaster_id)
#         sellmaster = RestoSellMaster.objects(id=object_id).first()

#         if sellmaster:
#             response = {
#                 "id": str(sellmaster.id),
#                 "showName": sellmaster.showName,
#                 "status": sellmaster.status,
#                 "sellUnits": sellmaster.sellUnits,
#                 "printers": sellmaster.printers,
#                 "sellType": sellmaster.sellType
#             }
#             return jsonify({"status_code": 200, "message": "Success", "data": response}), 200
#         else:
#             return jsonify({'error': 'SellMaster not found', 'status_code': 404}), 404

#     except Exception as e:
#         return jsonify({'error': str(e), 'status_code': 500}), 500


# # UPDATE
# @restoapp.route('/api/sellmasters/update/<string:sellmaster_id>', methods=['PUT'])
# def update_sellmaster(sellmaster_id):
#     try:
#         object_id = ObjectId(sellmaster_id)
#         sellmaster = RestoSellMaster.objects(id=object_id).first()

#         if not sellmaster:
#             return jsonify({'error': 'SellMaster not found', 'status_code': 404}), 404

#         data = request.json

#         # Validate that at least one field is present in the request
#         if not any(field in data for field in ['showName', 'status', 'sellUnits', 'printers', 'sellType']):
#             return jsonify({'error': 'At least one field (showName, status, sellUnits, printers, or sellType) is required', 'status_code': 400}), 400

#         # Update each field individually, filtering out null values
#         for key, value in data.items():
#             if value is not None:
#                 setattr(sellmaster, key, value)

#         sellmaster.save()

#         response = {"Body": None, "status": "success", "statusCode": 200, "message": 'SellMaster updated'}
#         return jsonify(response)

#     except (ValidationError, InvalidDocument) as e:
#         return jsonify({'error': str(e), 'status_code': 400}), 400
#     except Exception as e:
#         return jsonify({'error': str(e), 'status_code': 500}), 500


# # DELETE
# @restoapp.route('/api/sellmasters/delete/<string:sellmaster_id>', methods=['DELETE'])
# def delete_sellmaster(sellmaster_id):
#     try:
#         object_id = ObjectId(sellmaster_id)
#         sellmaster = RestoSellMaster.objects(id=object_id).first()

#         if sellmaster:
#             sellmaster.delete()
#             response = {"Body": None, "status": "success", "statusCode": 200, "message": 'SellMaster deleted'}
#             return jsonify(response)
#         else:
#             return jsonify({'error': 'SellMaster not found', 'status_code': 404}), 404

#     except Exception as e:
#         return jsonify({'error': str(e), 'status_code': 500}), 500
    
# # ___________________________________________________________________________________________________________________________________________________  
# # CREATE
# @restoapp.route('/api/generalmasters/create', methods=['POST'])
# def create_generalmaster():
#     try:
#         data = request.json

#         # Create embedded documents
#         bill_id_data = data.get('billId', {})
#         bill_id = BillId(startString=bill_id_data.get('startString'), endString=bill_id_data.get('endString'))

#         role_data = data.get('role', {})
#         role = Role(title=role_data.get('title'), accessTo=role_data.get('accessTo'))

#         business_summary_data = data.get('businessSummary', [])
#         business_summary = [BusinessSummary(**item) for item in business_summary_data]

#         order_types_data = data.get('orderTypes', {})
#         order_types = OrderTypes(showName=order_types_data.get('showName'), properties=order_types_data.get('properties'))

#         # Create GeneralMaster document
#         generalmaster = GeneralMaster(
#             billId=bill_id,
#             language=data.get('language'),
#             theme=data.get('theme'),
#             shopName=data.get('shopName'),
#             sources=data.get('sources'),
#             shopAddress=data.get('shopAddress'),
#             role=role,
#             name=data.get('name'),
#             userPic=data.get('userPic'),
#             businessSummaryStatus=data.get('businessSummaryStatus'),
#             businessSummary=business_summary,
#             orderTypes=order_types
#         )
#         generalmaster.save()

#         response = {"Body": None, "status": "success", "statusCode": 200, "message": 'GeneralMaster created'}
#         return jsonify(response)

#     except Exception as e:
#         return jsonify({'error': str(e), 'status_code': 500}), 500


# # READ
# @restoapp.route('/api/generalmasters/<string:generalmaster_id>', methods=['GET'])
# def get_generalmaster(generalmaster_id):
#     try:
#         object_id = ObjectId(generalmaster_id)
#         generalmaster = GeneralMaster.objects(id=object_id).first()

#         if generalmaster:
#             response = {
#                 "id": str(generalmaster.id),
#                 "billId": {
#                     "startString": generalmaster.billId.startString,
#                     "endString": generalmaster.billId.endString
#                 },
#                 "language": generalmaster.language,
#                 "theme": generalmaster.theme,
#                 "shopName": generalmaster.shopName,
#                 "sources": generalmaster.sources,
#                 "shopAddress": generalmaster.shopAddress,
#                 "role": {
#                     "title": generalmaster.role.title,
#                     "accessTo": generalmaster.role.accessTo
#                 },
#                 "name": generalmaster.name,
#                 "userPic": generalmaster.userPic,
#                 "businessSummaryStatus": generalmaster.businessSummaryStatus,
#                 "businessSummary": [
#                     {
#                         "businessURL": item.businessURL,
#                         "businessName": item.businessName,
#                         "businessAddress": item.businessAddress,
#                         "businessMobile": item.businessMobile,
#                         "businessEmail": item.businessEmail,
#                         "businessDescription": item.businessDescription
#                     } for item in generalmaster.businessSummary
#                 ],
#                 "orderTypes": {
#                     "showName": generalmaster.orderTypes.showName,
#                     "properties": generalmaster.orderTypes.properties
#                 }
#             }
#             return jsonify({"status_code": 200, "message": "Success", "data": response}), 200
#         else:
#             return jsonify({'error': 'GeneralMaster not found', 'status_code': 404}), 404

#     except Exception as e:
#         return jsonify({'error': str(e), 'status_code': 500}), 500


# # UPDATE
# @restoapp.route('/api/generalmasters/update/<string:generalmaster_id>', methods=['PUT'])
# def update_generalmaster(generalmaster_id):
#     try:
#         object_id = ObjectId(generalmaster_id)
#         generalmaster = GeneralMaster.objects(id=object_id).first()

#         if not generalmaster:
#             return jsonify({'error': 'GeneralMaster not found', 'status_code': 404}), 404

#         data = request.json

#         # Validate that at least one field is present in the request
#         if not any(field in data for field in ['billId', 'language', 'theme', 'shopName', 'sources', 'shopAddress', 'role', 'name', 'userPic', 'businessSummaryStatus', 'businessSummary', 'orderTypes']):
#             return jsonify({'error': 'At least one field is required', 'status_code': 400}), 400

#         # Update BillId
#         if 'billId' in data:
#             bill_id_data = data['billId']
#             generalmaster.billId.startString = bill_id_data.get('startString', generalmaster.billId.startString)
#             generalmaster.billId.endString = bill_id_data.get('endString', generalmaster.billId.endString)

#         # Update Role
#         if 'role' in data:
#             role_data = data['role']
#             generalmaster.role.title = role_data.get('title', generalmaster.role.title)
#             generalmaster.role.accessTo = role_data.get('accessTo', generalmaster.role.accessTo)

#         # Update BusinessSummary
#         if 'businessSummary' in data:
#             business_summary_data = data['businessSummary']
#             generalmaster.businessSummary = [BusinessSummary(**item) for item in business_summary_data]

#         # Update OrderTypes
#         if 'orderTypes' in data:
#             order_types_data = data['orderTypes']
#             generalmaster.orderTypes.showName = order_types_data.get('showName', generalmaster.orderTypes.showName)
#             generalmaster.orderTypes.properties = order_types_data.get('properties', generalmaster.orderTypes.properties)

#         # Update other fields
#         for key, value in data.items():
#             if key not in ['billId', 'role', 'businessSummary', 'orderTypes']:
#                 setattr(generalmaster, key, value)

#         generalmaster.save()

#         response = {"Body": None, "status": "success", "statusCode": 200, "message": 'GeneralMaster updated'}
#         return jsonify(response)

#     except (ValidationError, InvalidDocument) as e:
#         return jsonify({'error': str(e),})
    
# # DELETE
# @restoapp.route('/api/generalmasters/delete/<string:generalmaster_id>', methods=['DELETE'])
# def delete_generalmaster(generalmaster_id):
#     try:
#         object_id = ObjectId(generalmaster_id)
#         generalmaster = GeneralMaster.objects(id=object_id).first()

#         if generalmaster:
#             generalmaster.delete()
#             response = {"Body": None, "status": "success", "statusCode": 200, "message": 'GeneralMaster deleted'}
#             return jsonify(response)
#         else:
#             return jsonify({'error': 'GeneralMaster not found', 'status_code': 404}), 404

#     except Exception as e:
#         return jsonify({'error': str(e), 'status_code': 500}), 500
    
    _____
    
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