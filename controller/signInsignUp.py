import re
import hashlib
import datetime
import uuid
from bson import ObjectId
from flask import Blueprint, current_app, request, jsonify, session
from flask_jwt_extended import get_jwt_identity, jwt_required
import jwt
from model.signInsignup_model import  User
# from model.signInsignup_model import Resto, Shop, UserData


email_regex = r'^\S+@\S+\.\S+$' 
password_regex = r'^.{8,}$'

shop_data =  [
    {
        "shop": [
            {
                "masters": [
                    {
                        "menuMaster": [
                            {
                                "showName": "Masters",
                                "path": "/masters",
                                "subMenu": [
                                    {
                                        "showName": "General Master",
                                        "connectedTo": "generalMaster",
                                        "path": "/masters/general"
                                    },
                                    {
                                        "showName": "Food Master",
                                        "connectedTo": "itemMaster",
                                        "path": "/masters/foods"
                                    },
                                    {
                                        "showName": "Payments Master",
                                        "connectedTo": "paymentMaster",
                                        "path": "/masters/payments"
                                    },
                                    {
                                        "showName": "Menu Master",
                                        "connectedTo": "menuMaster",
                                        "path": "/masters/menu"
                                    }
                                ]
                            },
                            {
                                "showName": "Foods",
                                "path": "/foods",
                                "subMenu": [
                                    {
                                        "showName": "Manage Foods",
                                        "path": "/foods/manage"
                                    },
                                    {
                                        "showName": "Create",
                                        "path": "/foods/create"
                                    }
                                ]
                            },
                            {
                                "showName": "My Restaurant",
                                "path": "/boards",
                                "subMenu": [
                                    {
                                        "showName": "Sales",
                                        "path": "/boards/sales"
                                    },
                                    {
                                        "showName": "KOT",
                                        "path": "/boards/kot"
                                    }
                                ]
                            }
                        ],
                        "sellMaster": [
                            {
                                "showName": "Sells Master",
                                "status": "Active/Inactive",
                                "sellUnits": ["kg", "gm", "/pc"],
                                "printers": ["Printer 1", "Printer 2"],
                                "sellType": ["EndCustomer", "Retailer", "Wholesaler"]
                            },
                            {
                                "showName": "Service Master",
                                "status": "Active/Inactive",
                                "sellUnits": ["/pc"],
                                "printers": ["Printer 1", "Printer 2"],
                                "sellType": ["EndCustomer", "Retailer", "Wholesaler"]
                            }
                        ],
                        "generalMaster": [
                            {
                                "billId": {
                                    "startString": "RESTO",
                                    "endString": 1000
                                }
                            },
                            {
                                "language": "En"
                            },
                            {
                                "theme": "dark/light/any color"
                            },
                            {
                                "shopName": "Customer Defined Name"
                            },
                            {
                                "sources": ["source 1 ", "source 2"]
                            },
                            {
                                "shopAddress": "resto address which will be used while serving foods"
                            },
                            {
                                "role": {
                                    "title": "owner",
                                    "accessTo": ["shop1", "shop2", "list of shops"]
                                }
                            },
                            {
                                "name": "Customers Full Name"
                            },
                            {
                                "userPic": "path to user picture"
                            },
                            {
                                "businessSummaryStatus": "active"
                            },
                            {
                                "businessSummary": [
                                    {
                                        "businessURL": "/resto-name"
                                    },
                                    {
                                        "businessName": "cusomers Resto Name"
                                    },
                                    {
                                        "businessAddress": "cusomers Resto Name"
                                    },
                                    {
                                        "businessMobile": ["9890980947", "9890980948"]
                                    },
                                    {
                                        "businessEmail": "cusomers Email Id"
                                    },
                                    {
                                        "businessDescription": "Long Text Added by customer about their resto"
                                    }
                                ]
                            },
                            {
                                "orderTypes": {
                                    "showName": "How You Serve Your Foods",
                                    "properties": ["online", "parcel", "walkin", "dine"]
                                }
                            }
                        ],
                        "itemMaster": [
                            {
                                "category": [
                                    {
                                        "showName": "Food Category",
                                        "accessTo": ["SUB CATEGORY 1", "SUB CATEGORY 2"]
                                    }
                                ]
                            },
                            {
                                "subCategory": [
                                    {
                                        "showName": "Food Sub Category",
                                        "properties": ["sub category 1 ", "sub category 2"]
                                    }
                                ]
                            },
                            {
                                "taxIndividual": {
                                    "showName": "Apply tax to indiviual food",
                                    "properties": {
                                        "status": "active",
                                        "value": "false"
                                    }
                                }
                            },
                            {
                                "barcode": {
                                    "showName": "Add Barcode to foods",
                                    "properties": {
                                        "status": "active",
                                        "value": "false"
                                    }
                                }
                            },
                            {
                                "rackManagement": {
                                    "showName": "Add rack management",
                                    "properties": {
                                        "status": "active",
                                        "value": "false"
                                    }
                                }
                            },
                            {
                                "deadStock": {
                                    "showName": "Manage my dead stocks",
                                    "properties": {
                                        "status": "active",
                                        "value": "false"
                                    }
                                }
                            }
                        ],
                        "paymentMaster": [
                            {
                                "taxSlab": [
                                    {
                                        "showName": "Tax Slabs",
                                        "properties": [
                                            {
                                                "slabName": "tax 18",
                                                "slabValue": 18
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "banks": [
                                    {
                                        "showName": "Your Banks",
                                        "properties": [
                                            {
                                                "name": "tax 18",
                                                "branch": "SBI Karad",
                                                "ifscCode": "esasdasd",
                                                "accNumber": "asdasdasdads",
                                                "startingBalance": 2000,
                                                "currentBalance": 3000
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "paymentModes": [
                                    {
                                        "showName": "Your Payment Modes",
                                        "properties": [
                                            {
                                                "name": "PhonePe ",
                                                "bankAttahed": "SBI Karad"
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "subCategory": [
                                    {
                                        "showName": "Sub Category",
                                        "properties": ["sub category 1 ", "sub category 2"]
                                    }
                                ]
                            },
                            {
                                "taxIndividual": {
                                    "showName": "Apply tax to indiviual item",
                                    "properties": {
                                        "status": "active",
                                        "value": "false"
                                    }
                                }
                            },
                            {
                                "barcode": {
                                    "showName": "Add Barcode to items",
                                    "properties": {
                                        "status": "active",
                                        "value": "false"
                                    }
                                }
                            },
                            {
                                "rackManagement": {
                                    "showName": "Add rack management",
                                    "properties": {
                                        "status": "active",
                                        "value": "false"
                                    }
                                }
                            },
                            {
                                "deadStock": {
                                    "showName": "Manage my dead stocks",
                                    "properties": {
                                        "status": "active",
                                        "value": "false"
                                    }
                                }
                            }
                        ]
                    }
                ],
                "invoices": [
                    {
                        "billId": "Number",
                        "customer": "mongo ID",
                        "billDate": "Date",
                        "itemList": [
                            {
                                "itemName": "String",
                                "itemMrp": "Number",
                                "itemDisc": "Number",
                                "itemDiscP": "Number",
                                "itemPrice": "Number",
                                "itemQty": "Number",
                                "subTotal": "Number",
                                "endUserRate": "Number",
                                "retailerRate": "Number",
                                "wholesalerRate": "Number"
                            }
                        ],
                        "savings": "Number",
                        "status": "String",
                        "count": "Number",
                        "orderType": "String",
                        "taxedAmount": "Number",
                        "taxedP": "Number",
                        "discountedAmount": "Number",
                        "discountedP": "Number",
                        "grandTotal": "Number",
                        "Credit": "Number",
                        "paidAmount": "Number",
                        "returnedAmount": "Number",
                        "paidIn": "Number",
                        "paymentMode": "String",
                        "remarks": "String"
                    }
                ]
            }
        ]
    }
]
#  New resto data to be added
resto_data = [
    {
        "masters": [
            {
                "menuMaster": [
                    {
                        "showName": "Masters",
                        "path": "/masters",
                        "subMenu": [
                            {
                                "showName": "General Master",
                                "connectedTo": "generalMaster",
                                "path": "/masters/general"
                            },
                            {
                                "showName": "Food Master",
                                "connectedTo": "itemMaster",
                                "path": "/masters/foods"
                            },
                            {
                                "showName": "Payments Master",
                                "connectedTo": "paymentMaster",
                                "path": "/masters/payments"
                            },
                            {
                                "showName": "Menu Master",
                                "connectedTo": "menuMaster",
                                "path": "/masters/menu"
                            }
                        ]
                    },
                    {
                        "showName": "Foods",
                        "path": "/foods",
                        "subMenu": [
                            {
                                "showName": "Manage Foods",
                                "path": "/foods/manage"
                            },
                            {
                                "showName": "Create",
                                "path": "/foods/create"
                            }
                        ]
                    },
                    {
                        "showName": "My Restaurant",
                        "path": "/boards",
                        "subMenu": [
                            {
                                "showName": "Sales",
                                "path": "/boards/sales"
                            },
                            {
                                "showName": "KOT",
                                "path": "/boards/kot"
                            }
                        ]
                    }
                ],
                "sellMaster": [
                    {
                        "showName": "Sells Master",
                        "status": "Active/Inactive",
                        "sellUnits": ["kg", "gm", "/pc"],
                        "printers": ["Printer 1", "Printer 2"],
                        "sellType": ["EndCustomer", "Retailer", "Wholesaler"]
                    },
                    {
                        "showName": "Service Master",
                        "status": "Active/Inactive",
                        "sellUnits": ["/pc"],
                        "printers": ["Printer 1", "Printer 2"],
                        "sellType": ["EndCustomer", "Retailer", "Wholesaler"]
                    }
                ],
                "generalMaster": [
                    {
                        "billId": {
                            "startString": "RESTO",
                            "endString": 1000
                        }
                    },
                    {
                        "language": "En"
                    },
                    {
                        "theme": "dark/light/any color"
                    },
                    {
                        "shopName": "Customer Defined Name"
                    },
                    {
                        "sources": ["source 1 ", "source 2"]
                    },
                    {
                        "shopAddress": "resto address which will be used while serving foods"
                    },
                    {
                        "role": {
                            "title": "owner",
                            "accessTo": ["shop1", "shop2", "list of shops"]
                        }
                    },
                    {
                        "name": "Customers Full Name"
                    },
                    {
                        "userPic": "path to user picture"
                    },
                    {
                        "businessSummaryStatus": "active"
                    },
                    {
                        "businessSummary": [
                            {
                                "businessURL": "/resto-name"
                            },
                            {
                                "businessName": "cusomers Resto Name"
                            },
                            {
                                "businessAddress": "cusomers Resto Name"
                            },
                            {
                                "businessMobile": ["9890980947", "9890980948"]
                            },
                            {
                                "businessEmail": "cusomers Email Id"
                            },
                            {
                                "businessDescription": "Long Text Added by customer about their resto"
                            }
                        ]
                    },
                    {
                        "orderTypes": {
                            "showName": "How You Serve Your Foods",
                            "properties": ["online", "parcel", "walkin", "dine"]
                        }
                    }
                ],
                "itemMaster": [
                    {
                        "category": [
                            {
                                "showName": "Food Category",
                                "accessTo": ["SUB CATEGORY 1", "SUB CATEGORY 2"]
                            }
                        ]
                    },
                    {
                        "subCategory": [
                            {
                                "showName": "Food Sub Category",
                                "properties": ["sub category 1 ", "sub category 2"]
                            }
                        ]
                    },
                    {
                        "taxIndividual": {
                            "showName": "Apply tax to indiviual food",
                            "properties": {
                                "status": "active",
                                "value": "false"
                            }
                        }
                    },
                    {
                        "barcode": {
                            "showName": "Add Barcode to foods",
                            "properties": {
                                "status": "active",
                                "value": "false"
                            }
                        }
                    },
                    {
                        "rackManagement": {
                            "showName": "Add rack management",
                            "properties": {
                                "status": "active",
                                "value": "false"
                            }
                        }
                    },
                    {
                        "deadStock": {
                            "showName": "Manage my dead stocks",
                            "properties": {
                                "status": "active",
                                "value": "false"
                            }
                        }
                    }
                ],
                "paymentMaster": [
                    {
                        "taxSlab": [
                            {
                                "showName": "Tax Slabs",
                                "properties": [
                                    {
                                        "slabName": "tax 18",
                                        "slabValue": 18
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "banks": [
                            {
                                "showName": "Your Banks",
                                "properties": [
                                    {
                                        "name": "tax 18",
                                        "branch": "SBI Karad",
                                        "ifscCode": "esasdasd",
                                        "accNumber": "asdasdasdads",
                                        "startingBalance": 2000,
                                        "currentBalance": 3000
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "paymentModes": [
                            {
                                "showName": "Your Payment Modes",
                                "properties": [
                                    {
                                        "name": "PhonePe ",
                                        "bankAttahed": "SBI Karad"
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "subCategory": [
                            {
                                "showName": "Sub Category",
                                "properties": ["sub category 1 ", "sub category 2"]
                            }
                        ]
                    },
                    {
                        "taxIndividual": {
                            "showName": "Apply tax to indiviual item",
                            "properties": {
                                "status": "active",
                                "value": "false"
                            }
                        }
                    },
                    {
                        "barcode": {
                            "showName": "Add Barcode to items",
                            "properties": {
                                "status": "active",
                                "value": "false"
                            }
                        }
                    },
                    {
                        "rackManagement": {
                            "showName": "Add rack management",
                            "properties": {
                                "status": "active",
                                "value": "false"
                            }
                        }
                    },
                    {
                        "deadStock": {
                            "showName": "Manage my dead stocks",
                            "properties": {
                                "status": "active",
                                "value": "false"
                            }
                        }
                    }
                ]
            }
        ],
        "invoices": [
            {
                "billId": "Number",
                "customer": "mongo ID",
                "billDate": "Date",
                "itemList": [
                    {
                        "itemName": "String",
                        "itemMrp": "Number",
                        "itemDisc": "Number",
                        "itemDiscP": "Number",
                        "itemPrice": "Number",
                        "itemQty": "Number",
                        "subTotal": "Number",
                        "endUserRate": "Number",
                        "retailerRate": "Number",
                        "wholesalerRate": "Number"
                    }
                ],
                "savings": "Number",
                "status": "String",
                "count": "Number",
                "orderType": "String",
                "taxedAmount": "Number",
                "taxedP": "Number",
                "discountedAmount": "Number",
                "discountedP": "Number",
                "grandTotal": "Number",
                "Credit": "Number",
                "paidAmount": "Number",
                "returnedAmount": "Number",
                "paidIn": "Number",
                "paymentMode": "String",
                "remarks": "String"
            }
        ]
    }
]

# session['resto_data']=resto_data
# session['shop_data']=shop_data
# 
signUp_bp = Blueprint('signUp', __name__)
# Step 1: Register user with basic information
# Step 1: Register user with basic information
@signUp_bp.route('/register/step1', methods=['POST'])
def register_step1():
    try:
        data = request.json
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role')

        # Check if the email is already registered
        if User.objects(email=email).first():
            response = {"Body": None, "status": "error", "statusCode": 400, "message": 'Email is already registered'}
            return jsonify(response), 400


        if not username or not email or not password or not role:
            response = {"Body": None, "status": "error", "statusCode": 400, "message": 'username, email, password, and role are required'}
            return jsonify(response), 400
        # Create User instance with basic information
        
        user = User(
            username=username,
            email=email,
            password=password,
            role=role,
        )

        # Save the user to the database
        user.save()

        # Retrieve the user ID after saving to the database and convert to string
        user_id = str(user.id)

        # Include user ID in the response
        response = {"Body": {"user_id": user_id}, "status": "success", "statusCode": 200, "message": 'Step 1 successful'}
        return jsonify(response), 200

    except Exception as e:
        response = {"Body": None, "status": "error", "statusCode": 500, "message": str(e)}
        return jsonify(response), 500



@signUp_bp.route('/register/step2', methods=['POST'])
def register_step2():
    try:
        data = request.json
        name = data.get('name')
        mobilenumber = data.get('mobilenumber')
        businessname = data.get('businessname')
        businesstype = data.get('businesstype')

        if not name or not mobilenumber or not businessname or not businesstype:
            response = {"Body": None, "status": "error", "statusCode": 400, "message": 'Username, name, mobile number, business name, and business type are required'}
            return jsonify(response), 400

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

        # Update the user with additional information
        user.name = name
        user.mobilenumber = mobilenumber
        user.businessname = businessname
        user.businesstype = businesstype

        # Perform additional validation if needed
        if businesstype == "resto" or businesstype == "shop":
            # Assuming session['resto_data'] contains the required dictionary
            resto_data = session.get('resto_data')
            # Assuming session['shop_data'] contains the required dictionary
            shop_data = session.get('shop_data')

            # Remove existing bundles if present
            user.shopbundale = None
            user.restobundale = None

            # password_hash = hashlib.sha256(password.encode()).hexdigest()

            if businesstype == "shop":
                user.shopbundale = shop_data
                response=jwt.encode({'bundale':shop_data},current_app.config['SECRET_KEY'],algorithm='HS256')
            elif businesstype == "resto":
                response=jwt.encode({'bundale':resto_data},current_app.config['SECRET_KEY'],algorithm='HS256')
                user.restobundale = resto_data

        # Save the updated user to the database
        user.save()
        
        response = {"Body": response, "status": "success", "statusCode": 200, "message": 'Step 2 successful'}
        return jsonify(response), 200

    except Exception as e:
        response = {"Body": None, "status": "error", "statusCode": 500, "message": str(e)}
        return jsonify(response), 500



# #  signinblueprint
# # Step 1: Register user with basic information
# @signUp_bp.route('/register/step1', methods=['POST'])
# def register_step1():
#     try:
#         data = request.json
#         username = data.get('username')
#         email = data.get('email')
#         password = data.get('password')
#         role = data.get('role')
        
    
#         if not username or not email or not password or not role:
#             response = {"Body": None, "status": "error", "statusCode": 400, "message": 'username, email, password , and role are required'}
#             return jsonify(response), 400
    

#         response = {"Body": None, "status": "success", "statusCode": 200, "message": 'Step 1 successful'}
#         return jsonify(response), 200

#     except Exception as e:
#         response = {"Body": None, "status": "error", "statusCode": 500, "message": str(e)}
#         return jsonify(response), 500




# # # Step 2: Register user with additional information 
# @signUp_bp.route('/register/step2', methods=['POST'])
# def register_step2():
#     try:
#         data = request.json
#         name = data.get('name')
#         mobilenumber = data.get('mobilenumber')
#         businessname = data.get('businessname')
#         businesstype = data.get('businesstype')

#         # Retrieve data from the session
#         username = session.get('username')
#         email = session.get('email')
#         password = session.get('password')
#         role = session.get('role')
#         # Assuming session['resto_data'] contains the required dictionary
#         resto_data = session.get('resto_data')

#         if not name or not mobilenumber or not businessname or not businesstype:
#             response = {"Body": None, "status": "error", "statusCode": 400, "message": 'Name, mobile number, business name, and business type are required'}
#             return jsonify(response), 400



#         # Perform additional validation if needed
#         if businesstype == "resto" or businesstype == "shop":
#             password_hash = hashlib.sha256(password.encode()).hexdigest()
            
#         if businesstype == "shop":
#             user = User(username=username, email=email, password=password_hash, role=role,
#                         name=name, mobilenumber=mobilenumber, businessname=businessname, businesstype=businesstype,
#                         shopbundale=session.get('shop_data'))
#         elif businesstype == "resto":
#             user = User(username=username, email=email, password=password_hash, role=role,
#                         name=name, mobilenumber=mobilenumber, businessname=businessname, businesstype=businesstype,
#                         restobundale=resto_data)
        
#         user.save()

#         # Clear the session data after successful registration
#         session.pop('username', None)
#         session.pop('email', None)
#         session.pop('password', None)
#         session.pop('role', None)

#         response = {"Body": None, "status": "success", "statusCode": 200, "message": 'Registration successful'}
#         return jsonify(response), 200

#     except Exception as e:
#         response = {"Body": None, "status": "error", "statusCode": 500, "message": str(e)}
#         return jsonify(response), 500
    

    

































login_bp = Blueprint('login', __name__)
@login_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        businesstype = data.get('businesstype')

        # Validate the presence of 'email', 'password', and 'businesstype'
        if email is None or password is None or businesstype is None:
            return jsonify({'error': 'Email, password, and businesstype are required', 'status_code': 400}), 400

        # Find the user by email
        user = User.objects(email=email).first()

        if user:
            # Check if the provided businesstype matches the user's businesstype
            if user.businesstype == businesstype:
                provided_password_hash = hashlib.sha256(password.encode()).hexdigest()

                if provided_password_hash == user.password:
                    payload = {
                        'user_id': str(user.id),
                        'sub': '1',
                        'jti': str(uuid.uuid4()),
                        'identity': user.email,
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=50),
                        'role': user.role,
                        'type': 'access',
                        'fresh': True
                    }
                    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256') 

                    # Include user businesstype in the response body based on its value
                    if user.businesstype == 'resto':
                        encoded_resto_data = jwt.encode({'bundle':resto_data}, current_app.config['SECRET_KEY'], algorithm='HS256')
                        return jsonify({'Body': encoded_resto_data,
                                        'message': 'Login successful', 'access_token': token, 'status_code': 200})
                    elif user.businesstype == 'shop':
                        encoded_shop_data = jwt.encode({'bundle': shop_data}, current_app.config['SECRET_KEY'], algorithm='HS256')
                        return jsonify({'Body': encoded_shop_data,
                                        'message': 'Login successful', 'access_token': token, 'status_code': 200})
                else:
                    return jsonify({'error': 'Invalid password'}), 401
            else:
                return jsonify({'error': 'Invalid businesstype'}), 401

        return jsonify({'error': 'Invalid email or password'}), 401

    except Exception as e:
        return jsonify({'error': str(e)}), 500
  

  


 
 
 



    
@login_bp.route('/protected', methods=['GET'])
@jwt_required
def role_login():
    try:
        token = request.headers.get('Authorization').split()[1]
        decoded_token = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])

        user_role = decoded_token.get('role')

        if user_role == 'admin':
            return jsonify({'status_code': 200, 'message': 'success', 'role': 'admin'}), 200
        elif user_role == 'user':
            return jsonify({'status_code': 200, 'message': 'success', 'role': 'user'}), 200
        else:
            return jsonify({'status_code': 403, 'message': 'Permission denied'}), 403
    except UnicodeDecodeError as e:
        # Handle the specific error when the token payload cannot be decoded
        return jsonify({'status_code': 400, 'error': 'Invalid token payload'}), 400
    except Exception as e:
        return jsonify({'status_code': 500, 'error': str(e)}), 500






# @login_bp.route('/login', methods=['POST'])
# @jwt_required(optional=True)  # Use optional=True to allow both authenticated and unauthenticated requests
# def login():
#     try:
#         if request.method == 'POST':
#             data = request.json
#             email = data.get('email')
#             password = data.get('password')
            
#             # Validate the presence of 'name', 'email', and 'password'
#             if email is None:
#                 return jsonify({'error': 'Email is required', 'status_code': 400}), 400

#             if password is None:
#                 return jsonify({'error': 'Password is required', 'status_code': 400}), 400

#             user = User.objects(email=email).first()

#             if user:
#                 provided_password_hash = hashlib.sha256(password.encode()).hexdigest()

#                 if provided_password_hash == user.password:
#                     payload = {
#                         'user_id': str(user.id),
#                         'sub': '1', 
#                         'jti': str(uuid.uuid4()),  # Generate a unique identifier
#                         'identity': user.email, 
#                         'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=50),
#                         'role': user.role,  # Include the 'role' claim here
#                         'type': 'access',
#                         'fresh': True
#                     }
#                     token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

#                     return jsonify({'message': 'Login successful', 'access_token': token}), 200

#             return jsonify({'error': 'Invalid email or password'}), 401

#         elif request.method == 'GET':
#             # Handle the logic for the role based on the authenticated user
#             current_user = get_jwt_identity()
#             current_user_role = get_jwt_claims().get('role')

#             if current_user_role == 'admin':
#                 return jsonify({'status_code': 200, 'message': 'success', 'role': 'admin'}), 200
#             elif current_user_role == 'user':
#                 return jsonify({'status_code': 200, 'message': 'success', 'role': 'user'}), 200
#             else:
#                 return jsonify({'status_code': 403, 'message': 'Permission denied'}), 403

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500