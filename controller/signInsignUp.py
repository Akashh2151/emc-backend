import re
import hashlib
import datetime
import uuid
from flask import Blueprint, current_app, request, jsonify, session
from flask_jwt_extended import get_jwt_identity, jwt_required
import jwt
from model.signInsignup_model import  User
# from model.signInsignup_model import Resto, Shop, UserData


email_regex = r'^\S+@\S+\.\S+$' 
password_regex = r'^.{8,}$'

shop_data = {
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
                                    "showName": "Item Master",
                                    "connectedTo": "itemMaster",
                                    "path": "/masters/items"
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
                            "showName": "Items",
                            "path": "/items",
                            "connectedTo": "itemMaster",
                            "subMenu": [
                                {
                                    "showName": "Manage Items",
                                    "path": "/items/manage"
                                },
                                {
                                    "showName": "Create",
                                    "path": "/items/create"
                                }
                            ]
                        },
                        {
                            "showName": "My Shop",
                            "path": "/boards",
                            "connectedTo": "generalMaster",
                            "subMenu": [
                                {
                                    "showName": "Sales",
                                    "path": "/boards/sales"
                                },
                                {
                                    "showName": "Service",
                                    "path": "/boards/service"
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
                                "startString": "ABC",
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
                            "shopAddress": "shops address which will be used while selling goods"
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
                                    "businessURL": "/business-name"
                                },
                                {
                                    "businessName": "cusomers Business Name"
                                },
                                {
                                    "businessAddress": "cusomers Business Name"
                                },
                                {
                                    "businessMobile": ["9890980947", "9890980948"]
                                },
                                {
                                    "businessEmail": "cusomers Email Id"
                                },
                                {
                                    "businessDescription": "Long Text Added by customer about their business"
                                }
                            ]
                        },
                        {
                            "orderTypes": {
                                "showName": "How You Deliver Your Orders",
                                "properties": ["online", "offline", "walkin"]
                            }
                        }
                    ],
                    "itemMaster": [
                        {
                            "category": [
                                {
                                    "showName": "Category",
                                    "title": "category 1",
                                    "accessTo": ["SUB CATEGORY 1", "SUB CATEGORY 2"]
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






#  signinblueprint
signUp_bp = Blueprint('signUp', __name__)
# @signUp_bp.route('/register', methods=['POST'])
# def register():
#     try:
#         data = request.json
#         username = data.get('username')
#         email = data.get('email')
#         password = data.get('password')
#         role = data.get('role')  # Get the role from the request
#         session['username']=username
#         session['email']=email
#         session['password']=password
#         session['role']=role        
#         print("email:",email)
#         print("password:",password)
#         print("username:",username)
#         # Check if the email is already registered
#         existing_user = User.objects(email=email).first()
#         if existing_user:
#             response = { "Body": None,"status": "error","statusCode": 400,"message": 'Email already registered'}
#             return jsonify(response), 400

#         if not username or not email or not password:
#             response = {"Body": None,"status": "error","statusCode": 400,"message": 'Name, email, and password are required'}
#             return jsonify(response), 400

#         if not re.match(email_regex, email):
#             response = {"Body": None, "status": "error", "statusCode": 400, "message": 'Invalid email format'}
#             return jsonify(response), 400

#         if not re.match(password_regex, password):
#             response = {"Body": None,"status": "error","statusCode": 400,"message": 'Password must have at least 8 characters'}
#             return jsonify(response), 400

#         password_hash = hashlib.sha256(password.encode()).hexdigest()

#         user = User(username=username, email=email, password=password_hash,role=role)
#         user.save()

#         response = {"Body": None,"status": "success","statusCode": 200,"message": 'Registration successful'}
#         return jsonify(response), 200

#     except Exception as e:
#         response = { "Body": None,"status": "error","statusCode": 500,"message": str(e)}
#         return jsonify(response), 500
    
    
    
# @signUp_bp.route('/getregister',methods=['POST'])
# def cloneregister():
#     try:
#         data=request.json
#         name=data.get('name')
#         mobilenumber=data.get('mobilenumber')
#         businessname=data.get('businessname')
#         businesstype=data.get('businesstype')
        
#         if not name or not mobilenumber or not businessname or not businesstype:
#             return jsonify({"error":"name mobilenumber businessname businesstype is requred"})
        
#         if "username" and "email" and "password" and "role" in session and request.method=="POST":
#             user=User(name=name,mobilenumber=mobilenumber,businessname=businessname,businesstype=businesstype)
#             user.save()
#             response={"Body":None,"Status":"Success","StatusCode":200,"message": 'Registration successful'}
            
            
#             # username=session['username']
#             # email=session['email']
#             # password=session['password']
#             # role=session['role']
#             # return jsonify({"session name ":username,"email":email,"password":password,"role":role})
            
#     #    data=request.json
#     #    name=data.get('name')
#     #    mobilenumber=data.get('mobilenumber')
#     #    if request.method == 'POST':
           
          
       
       
#     except Exception as e:
#         response = {'Body':None,"status":"error","statuscode":500,"message":str(e)}
#         return jsonify(response)



# Step 1: Register user with basic information
@signUp_bp.route('/register/step1', methods=['POST'])
def register_step1():
    try:
        data = request.json
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role')

        # Store the data in the session
        session['username'] = username
        session['email'] = email
        session['password'] = password
        session['role'] = role
        session['shop_data'] = shop_data
        session['resto_data']=resto_data

        response = {"Body": None, "status": "success", "statusCode": 200, "message": 'Step 1 successful'}
        return jsonify(response), 200

    except Exception as e:
        response = {"Body": None, "status": "error", "statusCode": 500, "message": str(e)}
        return jsonify(response), 500




# Step 2: Register user with additional information 
@signUp_bp.route('/register/step2', methods=['POST'])
def register_step2():
    try:
        data = request.json
        name = data.get('name')
        mobilenumber = data.get('mobilenumber')
        businessname = data.get('businessname')
        businesstype = data.get('businesstype')

        # Retrieve data from the session
        username = session.get('username')
        email = session.get('email')
        password = session.get('password')
        role = session.get('role')
        # Assuming session['resto_data'] contains the required dictionary
        resto_data = session.get('resto_data')

        if not name or not mobilenumber or not businessname or not businesstype:
            response = {"Body": None, "status": "error", "statusCode": 400, "message": 'Name, mobile number, business name, and business type are required'}
            return jsonify(response), 400



        # Perform additional validation if needed
        if businesstype == "resto" or businesstype == "shop":
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
        if businesstype == "shop":
            user = User(username=username, email=email, password=password_hash, role=role,
                        name=name, mobilenumber=mobilenumber, businessname=businessname, businesstype=businesstype,
                        shopbundale=session.get('shop_data'))
        elif businesstype == "resto":
            user = User(username=username, email=email, password=password_hash, role=role,
                        name=name, mobilenumber=mobilenumber, businessname=businessname, businesstype=businesstype,
                        restobundale=resto_data)
        
        user.save()

        # Clear the session data after successful registration
        session.pop('username', None)
        session.pop('email', None)
        session.pop('password', None)
        session.pop('role', None)

        response = {"Body": None, "status": "success", "statusCode": 200, "message": 'Registration successful'}
        return jsonify(response), 200

    except Exception as e:
        response = {"Body": None, "status": "error", "statusCode": 500, "message": str(e)}
        return jsonify(response), 500
    
    

    
    
    
    
    
    
# __________________________________________________________________________________________________________________________
# sending json  bundale ragister api

# @signUp_bp.route('/register', methods=['POST'])
# def register():
#     try:
#         data = request.json
#         name = data.get('name')
#         email = data.get('email')
#         password = data.get('password')
#         role = data.get('role')
#         json_data = data.get('json_data')

#         # Check if the email is already registered
#         existing_user = User.objects(email=email).first()
#         if existing_user:
#             response = {"Body": None, "status": "error", "statusCode": 400, "message": 'Email already registered'}
#             return jsonify(response), 400

#         if not name or not email or not password:
#             response = {"Body": None, "status": "error", "statusCode": 400, "message": 'Name, email, and password are required'}
#             return jsonify(response), 400

#         if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
#             response = {"Body": None, "status": "error", "statusCode": 400, "message": 'Invalid email format'}
#             return jsonify(response), 400

#         if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$", password):
#             response = {"Body": None, "status": "error", "statusCode": 400, "message": 'Password must have at least 8 characters, one uppercase letter, and one digit'}
#             return jsonify(response), 400

#         password_hash = hashlib.sha256(password.encode()).hexdigest()

#         user = User(name=name, email=email, password=password_hash, role=role)
#         user.save()

#         # Store additional JSON data in UserData collection
#         user_data = User(user=user, data=json_data)
#         user_data.save()

#         response = {"Body": None, "status": "success", "statusCode": 200, "message": 'Registration successful'}
#         return jsonify(response), 200

#     except Exception as e:
#         response = {"Body": None, "status": "error", "statusCode": 500, "message": str(e)}
#         return jsonify(response), 500
    
    
# @signUp_bp.route('/user/<user_id>', methods=['GET'])
# def get_user_json_data(user_id):
#     try:
#         # Find the user by user_id
#         user = User.objects.get(id=user_id)

#         # Find associated JSON data in UserData collection
#         user_data = User.objects(user=user).first()

#         if user_data:
#             # Include only JSON data in the response
#             response = user_data.data
#             return jsonify(response), 200
#         else:
#             response = {"Body": None, "status": "error", "statusCode": 404, "message": 'User data not found'}
#             return jsonify(response), 404

#     except Exception as e:
#         response = {"Body": None, "status": "error", "statusCode": 500, "message": str(e)}
#         return jsonify(response), 500

# __________________________________________________________________________________________________________________________


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
                        return jsonify({'Body': resto_data,
                                        'message': 'Login successful', 'access_token': token, 'status_code': 200})
                    elif user.businesstype == 'shop':
                        return jsonify({'Body': shop_data,
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