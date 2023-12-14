from bson import ObjectId
from flask import Blueprint, jsonify, request
from model.signInsignup_model import User


master=Blueprint('master',__name__)
from flask import request, jsonify


@master.route('/v1/updateuserinfo', methods=['POST'])
def update_master_details():
    try:
        # Get the user ID from the headers
        user_id_from_header = request.headers.get('id')

        if not user_id_from_header:
            response = {"Body": None, "status": "error", "statusCode": 400, "message": 'User ID is required in the header'}
            return jsonify(response), 400

        # Convert user ID to ObjectId
        user_id_object = ObjectId(user_id_from_header)

        # Get the user from the database
        user = User.objects(id=user_id_object).first()

        if not user:
            response = {"Body": None, "status": "error", "statusCode": 404, "message": 'User not found'}
            return jsonify(response), 404

        # Get the new isActive values from the request JSON
        updated_master = request.json

        # Extract master details
        master_type = updated_master.get('type')  # Add a 'type' field to distinguish between menu and item master

        # Function to recursively update isActive values based on name
        def update_is_active(item, name, new_is_active):
            if item.get('name') == name:
                item['isActive'] = new_is_active
            for sub_item in item.get('subMenu', []):
                update_is_active(sub_item, name, new_is_active)
            for subcategory_item in item.get('subcategories', []):
                for sub_item in subcategory_item.get('subMenu', []):
                    update_is_active(sub_item, name, new_is_active)

        # Iterate through each category and update isActive based on name
        for category in user.restoBundle[0]['categories']:
            for subcategory in category.get("subcategories", []):
                update_is_active(subcategory, updated_master['name'], updated_master['isActive'])
                
            

        # Save the updated user to the database
        user.save()

        response = {"Body": None, "status": "success", "statusCode": 200, "message": 'master details updated successfully'}
        return jsonify(response), 200

    except Exception as e:
        response = {"Body": None, "status": "error", "statusCode": 500, "message": str(e)}
        return jsonify(response), 500







# ________________________________
# changed all top master value
# @master.route('/update-master-details', methods=['POST'])
# def update_master_details():
#     try:
#         # Get the user ID from the headers
#         user_id_from_header = request.headers.get('id')

#         if not user_id_from_header:
#             response = {"Body": None, "status": "error", "statusCode": 400, "message": 'User ID is required in the header'}
#             return jsonify(response), 400

#         # Convert user ID to ObjectId
#         user_id_object = ObjectId(user_id_from_header)

#         # Get the user from the database
#         user = User.objects(id=user_id_object).first()

#         if not user:
#             response = {"Body": None, "status": "error", "statusCode": 404, "message": 'User not found'}
#             return jsonify(response), 404

#         # Get the new isActive values from the request JSON
#         updated_master = request.json

#         # Extract master details
#         master_type = updated_master.get('type')  # Add a 'type' field to distinguish between menu and item master
#         master_name = updated_master.get('name')
#         new_is_active_master = updated_master.get('isActive')

#         # Locate the master based on its name
#         master_to_update = None
#         for category in user.restoBundle[0]['categories']:
#             for subcategory in category.get("subcategories", []):
#                 if subcategory.get("name") == master_name:
#                     master_to_update = subcategory
#                     break
#             if master_to_update:
#                 break

#         if not master_to_update:
#             response = {"Body": None, "status": "error", "statusCode": 404, "message": f'{master_name} not found in any category'}
#             return jsonify(response), 404

#         # Update isActive for the master
#         master_to_update['isActive'] = new_is_active_master

#         # Handle subcategories if any
#         subcategories = updated_master.get("subMenu", [])
#         for subcategory in subcategories:
#             subcategory_name = subcategory.get("name")
#             new_is_active_subcategory = subcategory.get("isActive")

#             # Find the specific subcategory based on subcategory name
#             target_subcategory = next((sub for sub in master_to_update.get("subcategories", []) if sub.get("name") == subcategory_name), None)

#             if not target_subcategory:
#                 response = {"Body": None, "status": "error", "statusCode": 404, "message": f'{subcategory_name} not found in {master_name}'}
#                 return jsonify(response), 404

#             # Update isActive for the subcategory
#             target_subcategory['isActive'] = new_is_active_subcategory

#         # Save the updated user to the database
#         user.save()

#         response = {"Body": None, "status": "success", "statusCode": 200, "message": f'{master_type} master details updated successfully'}
#         return jsonify(response), 200

#     except Exception as e:
#         response = {"Body": None, "status": "error", "statusCode": 500, "message": str(e)}
#         return jsonify(response), 500









# __________________________________________________________________________

#   {
#     "name": "menuMaster",
#     "title": "Menu",
#     "isActive": true,
#     "subMenu": []
#   }

# @master.route('/update-master-details', methods=['POST'])
# def update_master_details():
#     try:
#         # Get the user ID from the headers
#         user_id_from_header = request.headers.get('id')

#         if not user_id_from_header:
#             response = {"Body": None, "status": "error", "statusCode": 400, "message": 'User ID is required in the header'}
#             return jsonify(response), 400

#         # Convert user ID to ObjectId
#         user_id_object = ObjectId(user_id_from_header)

#         # Get the user from the database
#         user = User.objects(id=user_id_object).first()

#         if not user:
#             response = {"Body": None, "status": "error", "statusCode": 404, "message": 'User not found'}
#             return jsonify(response), 404

#         # Get the new isActive values from the request JSON
#         updated_category = request.json

#         # Extract category details
#         category_name = updated_category.get('name')
#         new_is_active_category = updated_category.get('isActive')

#         # Access the "Masters" category directly (index 1)
#         masters_category = user.restoBundle[0]['categories'][1]

#         # Use filter to find the specific master category based on category name
#         master_category = next((subcategory for subcategory in masters_category.get("subcategories", []) if subcategory.get("name") == category_name), None)

#         if not master_category:
#             response = {"Body": None, "status": "error", "statusCode": 404, "message": f'{category_name} not found in Masters category'}
#             return jsonify(response), 404

#         # Update isActive for the master category
#         master_category['isActive'] = new_is_active_category

#         # Handle subcategories if any
#         subcategories = updated_category.get("subMenu", [])
#         for subcategory in subcategories:
#             subcategory_name = subcategory.get("name")
#             new_is_active_subcategory = subcategory.get("isActive")

#             # Find the specific subcategory based on subcategory name
#             target_subcategory = next((sub for sub in master_category.get("subcategories", []) if sub.get("name") == subcategory_name), None)

#             if not target_subcategory:
#                 response = {"Body": None, "status": "error", "statusCode": 404, "message": f'{subcategory_name} not found in {category_name}'}
#                 return jsonify(response), 404

#             # Update isActive for the subcategory
#             target_subcategory['isActive'] = new_is_active_subcategory

#         # Save the updated user to the database
#         user.save()

#         response = {"Body": None, "status": "success", "statusCode": 200, "message": 'Master details updated successfully'}
#         return jsonify(response), 200

#     except Exception as e:
#         response = {"Body": None, "status": "error", "statusCode": 500, "message": str(e)}
#         return jsonify(response), 500


# ____________________________________________________________________
# json data 
# [
#   {
#     "name": "menuMaster",
#     "title": "Menu",
#     "isActive": false,
#     "subMenu": []
#   }
# ]

# @master.route('/update-master-details', methods=['POST'])
# def update_master_details():
#     try:
#         # Get the user ID from the headers
#         user_id_from_header = request.headers.get('id')

#         if not user_id_from_header:
#             response = {"Body": None, "status": "error", "statusCode": 400, "message": 'User ID is required in the header'}
#             return jsonify(response), 400

#         # Convert user ID to ObjectId
#         user_id_object = ObjectId(user_id_from_header)

#         # Get the user from the database
#         user = User.objects(id=user_id_object).first()

#         if not user:
#             response = {"Body": None, "status": "error", "statusCode": 404, "message": 'User not found'}
#             return jsonify(response), 404

#         # Get the new isActive values from the request JSON
#         updated_categories = request.json

#         # Iterate through the updated categories
#         for updated_category in updated_categories:
#             category_name = updated_category.get('name')
#             new_is_active_category = updated_category.get('isActive')

#             # Access the "Masters" category directly (index 1)
#             masters_category = user.restoBundle[0]['categories'][1]

#             # Use filter to find the specific master category based on category name
#             master_category = next((subcategory for subcategory in masters_category.get("subcategories", []) if subcategory.get("name") == category_name), None)

#             if not master_category:
#                 response = {"Body": None, "status": "error", "statusCode": 404, "message": f'{category_name} not found in Masters category'}
#                 return jsonify(response), 404

#             # Update isActive for the master category
#             master_category['isActive'] = new_is_active_category

#             # Handle subcategories if any
#             subcategories = updated_category.get("subMenu", [])
#             for subcategory in subcategories:
#                 subcategory_name = subcategory.get("name")
#                 new_is_active_subcategory = subcategory.get("isActive")

#                 # Find the specific subcategory based on subcategory name
#                 target_subcategory = next((sub for sub in master_category.get("subcategories", []) if sub.get("name") == subcategory_name), None)

#                 if not target_subcategory:
#                     response = {"Body": None, "status": "error", "statusCode": 404, "message": f'{subcategory_name} not found in {category_name}'}
#                     return jsonify(response), 404

#                 # Update isActive for the subcategory
#                 target_subcategory['isActive'] = new_is_active_subcategory

#         # Save the updated user to the database
#         user.save()

#         response = {"Body": None, "status": "success", "statusCode": 200, "message": 'Master details updated successfully'}
#         return jsonify(response), 200

#     except Exception as e:
#         response = {"Body": None, "status": "error", "statusCode": 500, "message": str(e)}
#         return jsonify(response), 500




# ________________________________________________
# {
#   "masterType": "itemMaster",
# //   "isActive": true,
# //   "isActiveName": true,
#      "isActiveDescription": true
# //   "isActiveMeasureUnit": true,
# //   "isActivePrice": true,
# //   "isActiveCategory": true,
# //   "isActiveSubCategory": true,
# //   "isActiveNutrition": true
# }

# @master.route('/update-master-details', methods=['POST'])
# def update_master_details():
#     try:
#         # Get the user ID from the headers
#         user_id_from_header = request.headers.get('id')

#         if not user_id_from_header:
#             response = {"Body": None, "status": "error", "statusCode": 400, "message": 'User ID is required in the header'}
#             return jsonify(response), 400

#         # Convert user ID to ObjectId
#         user_id_object = ObjectId(user_id_from_header)

#         # Get the user from the database
#         user = User.objects(id=user_id_object).first()

#         if not user:
#             response = {"Body": None, "status": "error", "statusCode": 404, "message": 'User not found'}
#             return jsonify(response), 404

#         # Get the new isActive value from the request JSON
#         data = request.json
#         master_type = data.get('masterType')
#         new_is_active = data.get('isActive')

#         # Access the "Masters" category directly (index 1)
#         masters_category = user.restoBundle[0]['categories'][1]

#         # Use filter to find the specific master category based on master type
#         master_category = next((subcategory for subcategory in masters_category.get("subcategories", []) if subcategory.get("name") == master_type), None)

#         if not master_category:
#             response = {"Body": None, "status": "error", "statusCode": 404, "message": f'{master_type} not found in Masters category'}
#             return jsonify(response), 404

#         # Update isActive for the master category
#         master_category['isActive'] = new_is_active

#         # Handle submenus if any
#         submenus = master_category.get("subMenu", [])
#         for submenu in submenus:
#             submenu_name = submenu.get("name")
#             new_submenu_is_active = data.get(f'isActive{submenu_name.capitalize()}')
#             submenu['isActive'] = new_submenu_is_active

#         # Save the updated user to the database
#         user.save()

#         response = {"Body": None, "status": "success", "statusCode": 200, "message": f'{master_type} details updated successfully'}
#         return jsonify(response), 200

#     except Exception as e:
#         response = {"Body": None, "status": "error", "statusCode": 500, "message": str(e)}
#         return jsonify(response), 500



# ______________________________________________________________________________________
# # from flask import request, jsonify
# @master.route('/update-menu-master-details', methods=['POST'])
# def update_menu_master_details():
#     try:
#         # Get the user ID from the headers
#         user_id_from_header = request.headers.get('id')

#         if not user_id_from_header:
#             response = {"Body": None, "status": "error", "statusCode": 400, "message": 'User ID is required in the header'}
#             return jsonify(response), 400

#         # Convert user ID to ObjectId
#         user_id_object = ObjectId(user_id_from_header)

#         # Get the user from the database
#         user = User.objects(id=user_id_object).first()

#         if not user:
#             response = {"Body": None, "status": "error", "statusCode": 404, "message": 'User not found'}
#             return jsonify(response), 404

#         # Get the new isActive value from the request JSON
#         data = request.json
#         new_is_active = data.get('isActive')

#         # Access the "Masters" category directly (index 1)
#         masters_category = user.restoBundle[0]['categories'][1]

#         # Access the "menuMaster" subcategory directly (index 0)
#         menu_master_category = masters_category.get("subcategories", [])[0]

#         # Update isActive for "Masters" category
#         masters_category['isActive'] = new_is_active

#         # Update isActive for "menuMaster" subcategory
#         menu_master_category['isActive'] = new_is_active

#         # Save the updated user to the database
#         user.save()

#         response = {"Body": None, "status": "success", "statusCode": 200, "message": 'Menu Master details updated successfully'}
#         return jsonify(response), 200

#     except Exception as e:
#         response = {"Body": None, "status": "error", "statusCode": 500, "message": str(e)}
#         return jsonify(response), 500




# # from flask import request, jsonify
# @master.route('/update-item-master-details', methods=['POST'])
# def update_item_master_details():
#     try:
#         # Get the user ID from the headers
#         user_id_from_header = request.headers.get('id')

#         if not user_id_from_header:
#             response = {"Body": None, "status": "error", "statusCode": 400, "message": 'User ID is required in the header'}
#             return jsonify(response), 400

#         # Convert user ID to ObjectId
#         user_id_object = ObjectId(user_id_from_header)

#         # Get the user from the database
#         user = User.objects(id=user_id_object).first()

#         if not user:
#             response = {"Body": None, "status": "error", "statusCode": 404, "message": 'User not found'}
#             return jsonify(response), 404

#         # Get the new isActive value from the request JSON
#         data = request.json
#         new_is_active_item_master = data.get('isActiveItemMaster')

#         # Access the "Masters" category directly (index 1)
#         masters_category = user.restoBundle[0]['categories'][1]

#         # Access the "itemMaster" subcategory directly (index 1)
#         item_master_category = masters_category.get("subcategories", [])[1]

#         # Update isActive for "Masters" category
#         masters_category['isActive'] = new_is_active_item_master

#         # Update isActive for "itemMaster" subcategory
#         item_master_category['isActive'] = new_is_active_item_master

#         # Handle separate configurations for each submenu within "itemMaster"
#         submenus = item_master_category.get("subMenu", [])
#         for submenu in submenus:
#             submenu_name = submenu.get("name")
#             new_submenu_is_active = data.get(f'isActive{submenu_name.capitalize()}')
#             submenu['isActive'] = new_submenu_is_active

#         # Save the updated user to the database
#         user.save()

#         response = {"Body": None, "status": "success", "statusCode": 200, "message": 'Item Master details updated successfully'}
#         return jsonify(response), 200

#     except Exception as e:
#         response = {"Body": None, "status": "error"}



# # from flask import request, jsonify
# @master.route('/update-tax-master-details', methods=['POST'])
# def update_tax_master_details():
#     try:
#         # Get the user ID from the headers
#         user_id_from_header = request.headers.get('id')

#         if not user_id_from_header:
#             response = {"Body": None, "status": "error", "statusCode": 400, "message": 'User ID is required in the header'}
#             return jsonify(response), 400

#         # Convert user ID to ObjectId
#         user_id_object = ObjectId(user_id_from_header)

#         # Get the user from the database
#         user = User.objects(id=user_id_object).first()

#         if not user:
#             response = {"Body": None, "status": "error", "statusCode": 404, "message": 'User not found'}
#             return jsonify(response), 404

#         # Get the new isActive value from the request JSON
#         data = request.json
#         new_is_active_tax_master = data.get('isActiveTaxMaster')

#         # Access the "Masters" category directly (index 1)
#         masters_category = user.restoBundle[0]['categories'][1]

#         # Access the "taxMaster" subcategory directly (index 2)
#         tax_master_category = masters_category.get("subcategories", [])[2]

#         # Update isActive for "Masters" category
#         masters_category['isActive'] = new_is_active_tax_master

#         # Update isActive for "taxMaster" subcategory
#         tax_master_category['isActive'] = new_is_active_tax_master

#         # Handle submenu "taxName"
#         tax_name_submenu = tax_master_category.get("subMenu", [])[0]
#         new_is_active_tax_name = data.get('isActiveTaxName')

#         # Update isActive for "taxName" submenu
#         tax_name_submenu['isActive'] = new_is_active_tax_name

#         # Save the updated user to the database
#         user.save()

#         response = {"Body": None, "status": "success", "statusCode": 200, "message": 'Tax Master details updated successfully'}
#         return jsonify(response), 200

#     except Exception as e:
#         response = {"Body": None, "status": "error", "statusCode": 500, "message": str(e)}
#         return jsonify(response), 500




# # from flask import request, jsonify
# @master.route('/update-customer-master-details', methods=['POST'])
# def update_customer_master_details():
#     try:
#         # Get the user ID from the headers
#         user_id_from_header = request.headers.get('id')

#         if not user_id_from_header:
#             response = {"Body": None, "status": "error", "statusCode": 400, "message": 'User ID is required in the header'}
#             return jsonify(response), 400

#         # Convert user ID to ObjectId
#         user_id_object = ObjectId(user_id_from_header)

#         # Get the user from the database
#         user = User.objects(id=user_id_object).first()

#         if not user:
#             response = {"Body": None, "status": "error", "statusCode": 404, "message": 'User not found'}
#             return jsonify(response), 404

#         # Get the new isActive value from the request JSON
#         data = request.json
#         new_is_active_customer_master = data.get('isActiveCustomerMaster')

#         # Access the "Masters" category directly (index 1)
#         masters_category = user.restoBundle[0]['categories'][1]

#         # Access the "customerMaster" subcategory directly (index 3)
#         customer_master_category = masters_category.get("subcategories", [])[3]

#         # Update isActive for "Masters" category
#         masters_category['isActive'] = new_is_active_customer_master

#         # Update isActive for "customerMaster" subcategory
#         customer_master_category['isActive'] = new_is_active_customer_master

#         # Handle submenu "customerName"
#         customer_name_submenu = customer_master_category.get("subMenu", [])[0]
#         new_is_active_customer_name = data.get('isActiveCustomerName')

#         # Update isActive for "customerName" submenu
#         customer_name_submenu['isActive'] = new_is_active_customer_name

#         # Handle submenu "customerMobile"
#         customer_mobile_submenu = customer_master_category.get("subMenu", [])[1]
#         new_is_active_customer_mobile = data.get('isActiveCustomerMobile')

#         # Update isActive for "customerMobile" submenu
#         customer_mobile_submenu['isActive'] = new_is_active_customer_mobile

#         # Handle submenu "customerEmail"
#         customer_email_submenu = customer_master_category.get("subMenu", [])[2]
#         new_is_active_customer_email = data.get('isActiveCustomerEmail')

#         # Update isActive for "customerEmail" submenu
#         customer_email_submenu['isActive'] = new_is_active_customer_email

#         # Handle submenu "customerLastVisit"
#         customer_last_visit_submenu = customer_master_category.get("subMenu", [])[3]
#         new_is_active_customer_last_visit = data.get('isActiveCustomerLastVisit')

#         # Update isActive for "customerLastVisit" submenu
#         customer_last_visit_submenu['isActive'] = new_is_active_customer_last_visit

#         # Handle submenu "customerAddr"
#         customer_addr_submenu = customer_master_category.get("subMenu", [])[4]
#         new_is_active_customer_addr = data.get('isActiveCustomerAddr')

#         # Update isActive for "customerAddr" submenu
#         customer_addr_submenu['isActive'] = new_is_active_customer_addr

#         # Handle submenu "customerHistory"
#         customer_history_submenu = customer_master_category.get("subMenu", [])[5]
#         new_is_active_customer_history = data.get('isActiveCustomerHistory')

#         # Update isActive for "customerHistory" submenu
#         customer_history_submenu['isActive'] = new_is_active_customer_history

#         # Save the updated user to the database
#         user.save()

#         response = {"Body": None, "status": "success", "statusCode": 200, "message": 'Customer Master details updated successfully'}
#         return jsonify(response), 200

#     except Exception as e:
#         response = {"Body": None, "status": "error", "statusCode": 500, "message": str(e)}
#         return jsonify(response), 500





# # from flask import request, jsonify
# @master.route('/update-employee-master-details', methods=['POST'])
# def update_employee_master_details():
#     try:
#         # Get the user ID from the headers
#         user_id_from_header = request.headers.get('id')

#         if not user_id_from_header:
#             response = {"Body": None, "status": "error", "statusCode": 400, "message": 'User ID is required in the header'}
#             return jsonify(response), 400

#         # Convert user ID to ObjectId
#         user_id_object = ObjectId(user_id_from_header)

#         # Get the user from the database
#         user = User.objects(id=user_id_object).first()

#         if not user:
#             response = {"Body": None, "status": "error", "statusCode": 404, "message": 'User not found'}
#             return jsonify(response), 404

#         # Get the new isActive value from the request JSON
#         data = request.json
#         new_is_active_employee_master = data.get('isActiveEmployeeMaster')

#         # Access the "Masters" category directly (index 1)
#         masters_category = user.restoBundle[0]['categories'][1]

#         # Access the "employeeMaster" subcategory directly (index 4)
#         employee_master_category = masters_category.get("subcategories", [])[4]

#         # Update isActive for "Masters" category
#         masters_category['isActive'] = new_is_active_employee_master

#         # Update isActive for "employeeMaster" subcategory
#         employee_master_category['isActive'] = new_is_active_employee_master

#         # Handle submenu "employeeName"
#         employee_name_submenu = employee_master_category.get("subMenu", [])[0]
#         new_is_active_employee_name = data.get('isActiveEmployeeName')

#         # Update isActive for "employeeName" submenu
#         employee_name_submenu['isActive'] = new_is_active_employee_name

#         # Handle submenu "employeeMobile"
#         employee_mobile_submenu = employee_master_category.get("subMenu", [])[1]
#         new_is_active_employee_mobile = data.get('isActiveEmployeeMobile')

#         # Update isActive for "employeeMobile" submenu
#         employee_mobile_submenu['isActive'] = new_is_active_employee_mobile

#         # Handle submenu "employeeEmail"
#         employee_email_submenu = employee_master_category.get("subMenu", [])[2]
#         new_is_active_employee_email = data.get('isActiveEmployeeEmail')

#         # Update isActive for "employeeEmail" submenu
#         employee_email_submenu['isActive'] = new_is_active_employee_email

#         # Handle submenu "employeeAddr"
#         employee_addr_submenu = employee_master_category.get("subMenu", [])[3]
#         new_is_active_employee_addr = data.get('isActiveEmployeeAddr')

#         # Update isActive for "employeeAddr" submenu
#         employee_addr_submenu['isActive'] = new_is_active_employee_addr

#         # Handle submenu "employeeHistory"
#         employee_history_submenu = employee_master_category.get("subMenu", [])[4]
#         new_is_active_employee_history = data.get('isActiveEmployeeHistory')

#         # Update isActive for "employeeHistory" submenu
#         employee_history_submenu['isActive'] = new_is_active_employee_history

#         # Handle submenu "employeeVerification"
#         employee_verification_submenu = employee_master_category.get("subMenu", [])[5]
#         new_is_active_employee_verification = data.get('isActiveEmployeeVerification')

#         # Update isActive for "employeeVerification" submenu
#         employee_verification_submenu['isActive'] = new_is_active_employee_verification

#         # Save the updated user to the database
#         user.save()

#         response = {"Body": None, "status": "success", "statusCode": 200, "message": 'Employee Master details updated successfully'}
#         return jsonify(response), 200

#     except Exception as e:
#         response = {"Body": None, "status": "error", "statusCode": 500, "message": str(e)}
#         return jsonify(response), 500
