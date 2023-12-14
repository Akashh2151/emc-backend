# import datetime
from json import JSONEncoder
from flask import Blueprint, app, request, jsonify 
from model.resto_model import   CustomerMaster, EmployeeMaster, History, Item, ItemMaster, Order, TaxMaster, Verification
from mongoengine.errors import DoesNotExist

from datetime import datetime

# from dateutil import parser


# restoapp blue print
restoapp = Blueprint('restoapp', __name__)




# Create an order
@restoapp.route('/order', methods=['POST'])
def create_order():
    try:
        data = request.json
        vendorCode = data.get('vendorCode')
        vendorName = data.get('vendorName')
        vendorEmail = data.get('vendorEmail')
        vendorMobile = data.get('vendorMobile')
        vendorAddr = data.get('vendorAddr')

        new_order = Order(
            vendorCode=vendorCode,
            vendorName=vendorName,
            vendorEmail=vendorEmail,
            vendorMobile=vendorMobile,
            vendorAddr=vendorAddr
        )
        new_order.save()

        response = {"Body": None, "status": "success", "statusCode": 200, "message": 'Order created'}
        return jsonify(response)

    except Exception as e:
        return jsonify({'Body': None, 'error': str(e), 'statusCode': 500})



# Get all orders
@restoapp.route('/order', methods=['GET'])
def get_orders():
    try:
        orders = Order.objects()
        orders_list = [{"vendorCode": order.vendorCode, "vendorName": order.vendorName,
                        "vendorEmail": order.vendorEmail, "vendorMobile": order.vendorMobile,
                        "vendorAddr": order.vendorAddr} for order in orders]

        response = {'Body': orders_list, 'status': 'success', 'statusCode': 200, 'message': 'Orders retrieved'}
        return jsonify(response)

    except Exception as e:
        return jsonify({'Body': None, 'error': str(e), 'statusCode': 500})



# Update an existing order by vendorCode
@restoapp.route('/order/<string:vendor_code>', methods=['PUT'])
def update_order(vendor_code):
    try:
        order = Order.objects(vendorCode=vendor_code).first()
        if not order:
            response = {'Body': None, 'message': 'Order not found', 'statusCode': 404, 'status': 'error'}
            return jsonify(response)

        data = request.json

        # Update only the fields present in the request JSON
        for key, value in data.items():
            setattr(order, key, value)

        order.save()

        response = {'Body': None, 'status': 'success', 'statusCode': 200, 'message': 'Order updated'}
        return jsonify(response)

    except Exception as e:
        return jsonify({'Body': None, 'error': str(e), 'statusCode': 500})
    

# Get a specific order by vendorCode
@restoapp.route('/order/<string:vendor_code>', methods=['GET'])
def get_order(vendor_code):
    try:
        order = Order.objects(vendorCode=vendor_code).first()
        if not order:
            response = {'Body': None, 'message': 'Order not found', 'statusCode': 404, 'status': 'error'}
            return jsonify(response)

        order_dict = {"vendorCode": order.vendorCode, "vendorName": order.vendorName,
                      "vendorEmail": order.vendorEmail, "vendorMobile": order.vendorMobile,
                      "vendorAddr": order.vendorAddr}

        response = {'Body': order_dict, 'status': 'success', 'statusCode': 200, 'message': 'Order retrieved'}
        return jsonify(response)

    except Exception as e:
        return jsonify({'Body': None, 'error': str(e), 'statusCode': 500})



# Delete an order by vendorCode
@restoapp.route('/order/<string:vendor_code>', methods=['DELETE'])
def delete_order(vendor_code):
    try:
        order = Order.objects(vendorCode=vendor_code).first()
        if not order:
            response = {'Body': None, 'message': 'Order not found', 'statusCode': 404, 'status': 'error'}
            return jsonify(response)

        order.delete()

        response = {'Body': None, 'status': 'success', 'statusCode': 200, 'message': 'Order deleted'}
        return jsonify(response)

    except Exception as e:
        return jsonify({'Body': None, 'error': str(e), 'statusCode': 500})


# __


# Create an item
@restoapp.route('/item', methods=['POST'])
def create_item():
    try:
        data = request.json
        name = data.get('name')
        description = data.get('description')
        measureUnit = data.get('measureUnit')
        price = data.get('price')
        category = data.get('category')
        subCategory = data.get('subCategory')
        nutrition = data.get('nutrition')

        new_item = ItemMaster(
            name=name,
            description=description,
            measureUnit=measureUnit,
            price=price,
            category=category,
            subCategory=subCategory,
            nutrition=nutrition
        )
        new_item.save()

        response = {"Body": None, "status": "success", "statusCode": 200, "message": 'Item created'}
        return jsonify(response)

    except Exception as e:
        return jsonify({'Body': None, 'error': str(e), 'statusCode': 500})


# Get all items
@restoapp.route('/item', methods=['GET'])
def get_items():
    try:
        items = ItemMaster.objects()
        items_list = [{"name": item.name, "description": item.description,
                       "measureUnit": item.measureUnit, "price": item.price,
                       "category": item.category, "subCategory": item.subCategory,
                       "nutrition": item.nutrition} for item in items]

        response = {'Body': items_list, 'status': 'success', 'statusCode': 200, 'message': 'Items retrieved'}
        return jsonify(response)

    except Exception as e:
        return jsonify({'Body': None, 'error': str(e), 'statusCode': 500})


# Update an existing item by name
@restoapp.route('/item/<string:item_name>', methods=['PUT'])
def update_item(item_name):
    try:
        item = ItemMaster.objects(name=item_name).first()
        if not item:
            response = {'Body': None, 'message': 'Item not found', 'statusCode': 404, 'status': 'error'}
            return jsonify(response)

        data = request.json

        # Update only the fields present in the request JSON
        for key, value in data.items():
            setattr(item, key, value)

        item.save()

        response = {'Body': None, 'status': 'success', 'statusCode': 200, 'message': 'Item updated'}
        return jsonify(response)

    except Exception as e:
        return jsonify({'Body': None, 'error': str(e), 'statusCode': 500})



# Get a specific item by name
@restoapp.route('/item/<string:item_name>', methods=['GET'])
def get_item(item_name):
    try:
        item = ItemMaster.objects(name=item_name).first()
        if not item:
            response = {'Body': None, 'message': 'Item not found', 'statusCode': 404, 'status': 'error'}
            return jsonify(response)

        item_dict = {"name": item.name, "description": item.description,
                     "measureUnit": item.measureUnit, "price": item.price,
                     "category": item.category, "subCategory": item.subCategory,
                     "nutrition": item.nutrition}

        response = {'Body': item_dict, 'status': 'success', 'statusCode': 200, 'message': 'Item retrieved'}
        return jsonify(response)

    except Exception as e:
        return jsonify({'Body': None, 'error': str(e), 'statusCode': 500})



# Delete an item by name
@restoapp.route('/item/<string:item_name>', methods=['DELETE'])
def delete_item(item_name):
    try:
        item = ItemMaster.objects(name=item_name).first()
        if not item:
            response = {'Body': None, 'message': 'Item not found', 'statusCode': 404, 'status': 'error'}
            return jsonify(response)

        item.delete()

        response = {'Body': None, 'status': 'success', 'statusCode': 200, 'message': 'Item deleted'}
        return jsonify(response)

    except Exception as e:
        return jsonify({'Body': None, 'error': str(e), 'statusCode': 500})


#__

# Create TaxMaster
@restoapp.route('/tax', methods=['POST'])
def create_tax():
    try:
        data = request.json
        taxName = data.get('taxName')

        new_tax = TaxMaster(taxName=taxName)
        new_tax.save()

        response = {"Body": None, "status": "success", "statusCode": 200, "message": 'Tax created'}
        return jsonify(response)

    except Exception as e:
        return jsonify({'Body': None, 'error': str(e), 'statusCode': 500})



# Get all taxes
@restoapp.route('/tax', methods=['GET'])
def get_taxes():
    try:
        taxes = TaxMaster.objects()
        taxes_list = [{"taxName": tax.taxName} for tax in taxes]

        response = {'Body': taxes_list, 'status': 'success', 'statusCode': 200, 'message': 'Taxes retrieved'}
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

@restoapp.route('/fooditem', methods=['POST'], endpoint='create_food_item')
def create_item():
    try:
        data = request.json
        item_code = data.get('itemCode')
        item_name = data.get('itemName')
        item_category = data.get('itemCategory')
        item_sub_category = data.get('itemSubCategory')
        item_price = data.get('itemPrice')
        ingredients = data.get('ingredients')
        recipe = data.get('recipe')
        allergen = data.get('allergen')
        portion_size = data.get('portionSize')
        status = data.get('status')
        tax = data.get('tax')
        discount = data.get('discount')
        images = data.get('images')
        current_stock = data.get('currentStock')
        barcode = data.get('barcode')
        custom_notes = data.get('customNotes')

        # Create a list of History objects from the provided salesHistory data
        sales_history_data = data.get('salesHistory', [])
        sales_history = [
            History(date=datetime.strptime(entry['date'], '%Y-%m-%dT%H:%M:%S.%fZ'), action=entry['action'])
            for entry in sales_history_data
        ]

        # Create the Item object with the extracted data
        new_item = Item(
            itemCode=item_code,
            itemName=item_name,
            itemCategory=item_category,
            itemSubCategory=item_sub_category,
            itemPrice=item_price,
            ingredients=ingredients,
            recipe=recipe,
            allergen=allergen,
            portionSize=portion_size,
            status=status,
            tax=tax,
            discount=discount,
            images=images,
            currentStock=current_stock,
            barcode=barcode,
            salesHistory=sales_history,
            customNotes=custom_notes
        )

        # Save the new item
        new_item.save()

        response = {"Body": None, "status": "success", "statusCode": 200, "message": 'Item created'}
        return jsonify(response)

    except Exception as e:
        return jsonify({'Body': None, 'error': str(e), 'statusCode': 500})



    
# Get all items
@restoapp.route('/item', methods=['GET'])
def get_all_items():
    try:
        items = Item.objects()
        items_list = [
            {
                "itemCode": item.itemCode,
                "itemName": item.itemName,
                "itemCategory": item.itemCategory,
                "itemSubCategory": item.itemSubCategory,
                "itemPrice": item.itemPrice,
                "ingredients": item.ingredients,
                "recipe": item.recipe,
                "allergen": item.allergen,
                "portionSize": item.portionSize,
                "status": item.status,
                "tax": item.tax,
                "discount": item.discount,
                "images": item.images,
                "currentStock": item.currentStock,
                "barcode": item.barcode,
                "salesHistory": [{"date": entry.date, "action": entry.action} for entry in item.salesHistory],
                "customNotes": item.customNotes
            }
            for item in items
        ]

        response = {'Body': items_list, 'status': 'success', 'statusCode': 200, 'message': 'Items retrieved'}
        return jsonify(response)

    except Exception as e:
        return jsonify({'Body': None, 'error': str(e), 'statusCode': 500})
    
    
    
 # Get a specific item by itemCode
@restoapp.route('/item/<item_code>', methods=['GET'])
def get_byitemcode(item_code):
    try:
        print(f"Attempting to find item with code: {item_code}")
        item = Item.objects.get(itemCode=item_code).first()
        print(f"Found item: {item}")
        

        item_data = {
            "itemCode": item.itemCode,
            "itemName": item.itemName,
            "itemCategory": item.itemCategory,
            "itemSubCategory": item.itemSubCategory,
            "itemPrice": item.itemPrice,
            "ingredients": item.ingredients,
            "recipe": item.recipe,
            "allergen": item.allergen,
            "portionSize": item.portionSize,
            "status": item.status,
            "tax": item.tax,
            "discount": item.discount,
            "images": item.images,
            "currentStock": item.currentStock,
            "barcode": item.barcode,
            "salesHistory": [{"date": entry.date.isoformat(), "action": entry.action} for entry in item.salesHistory],
            "customNotes": item.customNotes
        }

        response = {'Body': item_data, 'status': 'success', 'statusCode': 200, 'message': 'Item retrieved'}
        return jsonify(response)

    except Item.DoesNotExist:
        print(f"Item with code {item_code} not found.")
        return jsonify({'Body': None, 'error': 'Item not found', 'statusCode': 404})
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return jsonify({'Body': None, 'error': str(e), 'statusCode': 500})



 
 
 # Update an item by itemCode
@restoapp.route('/item/<item_code>', methods=['PUT'])
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
        item.images = data.get('images', item.images)
        item.currentStock = data.get('currentStock', item.currentStock)
        item.barcode = data.get('barcode', item.barcode)
        item.customNotes = data.get('customNotes', item.customNotes)

        # Update sales history if provided
        sales_history_data = data.get('salesHistory', [])
        item.salesHistory = [
            History(date=entry['date'], action=entry['action']) for entry in sales_history_data
        ]

        # Save the updated item
        item.save()

        response = {"Body": None, "status": "success", "statusCode": 200, "message": 'Item updated'}
        return jsonify(response)
    
    except DoesNotExist:
        return jsonify({'Body': None, 'error': 'Item not found', 'statusCode': 404})
    except Exception as e:
        return jsonify({'Body': None, 'error': str(e), 'statusCode': 500})
 
 
 
 
    

# # Delete an item by itemCode
# @restoapp.route('/item/<item_code>', methods=['DELETE'])
# def delete_item(item_code):
#     try:
#         item = Item.objects.get(itemCode=item_code)
#         item.delete()

#         response = {"Body": None, "status": "success", "statusCode": 200, "message": 'Item deleted'}
#         return jsonify(response)

#     except DoesNotExist:
#         return jsonify({'Body': None, 'error': 'Item not found', 'statusCode': 404})
#     except Exception as e:
#         return jsonify({'Body': None, 'error': str(e), 'statusCode': 500})


























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