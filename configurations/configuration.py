

shop_data =  [
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

#  New resto data to be added
resto_data = {
      "type": "resto",
      "name": "HR Resorts",
      "defaultMenu": [
        { "name": "top10", "title": "Top 10" },
        { "name": "onGoing", "title": "On Going" },
        { "name": "goToMenu", "title": "Go To Menu" },
        { "name": "help", "title": "Help" }
      ],
      "categories": [
        {
          "name": "Orders",
          "icon": "Orders",
          "path": "/orders",
          "title": "Orders",
          "isActive": "true",
          "default": "true",
          "subcategories": [
            {
              "name": "Orders",
              "title": "Orders",
              "isActive": "true",
              "subMenu": [
                {
                  "name": "vendorCode",
                  "title": "Vendor Code",
                  "isActive": "true",
                  "type": "text",
                  "placeholder": "Enter Vendor Code"
                },
                {
                  "name": "vendorName",
                  "title": "Vendor Name",
                  "isActive": "true",
                  "type": "text",
                  "placeholder": "Enter Vendor Name"
                },
                {
                  "name": "vendorEmail",
                  "title": "Vendor Email",
                  "isActive": "true",
                  "type": "text",
                  "values": [],
                  "placeholder": "Enter Vendor Email"
                },
                {
                  "name": "vendorMobile",
                  "title": "Vendor Mobile",
                  "isActive": "true",
                  "type": "text",
                  "values": ["Lawn", "Terrace"],
                  "placeholder": "Choose Vendor Location"
                },

                {
                  "name": "vendorAddr",
                  "title": "Vendor Address",
                  "isActive": "true",
                  "type": "text",
                  "placeholder": "Enter Address"
                }
              ]
            }
          ]
        },
        {
          "name": "Masters",
          "icon": "Masters",
          "path": "/masters",
          "title": "Masters",
          "isActive": "true",
          "default": "true",
          "subcategories": [
            {
              "name": "menuMaster",
              "title": "Menu",
              "isActive": "true",
              "subMenu": []
            },
            {
              "name": "itemMaster",
              "title": "Items",
              "isActive": "true",
              "subMenu": [
                {
                  "name": "name",
                  "title": "Food Name",
                  "values": "",
                  "type": "Input",
                  "isActive": "true",
                  "status": "default"
                },
                {
                  "name": "description",
                  "title": "Food Description",
                  "values": "",
                  "type": "Input",
                  "isActive": "true",
                  "status": "custom"
                },
                {
                  "name": "measureUnit",
                  "title": "Units",
                  "type": "DropDown",
                  "values": ["Kg", "PC", "Unit"],
                  "isActive": "true",
                  "status": "default"
                },
                {
                  "name": "price",
                  "title": "Price",
                  "type": "Input",
                  "values": "INR",
                  "default": ["INR", "Dollar"],
                  "isActive": "true",
                  "status": "default"
                },
                {
                  "name": "category",
                  "title": "Category",
                  "type": "Input",
                  "values": "",
                  "default": ["Veg", "Non Veg"],
                  "isActive": "true",
                  "status": "custom"
                },
                {
                  "name": "subCategory",
                  "title": "Sub Category",
                  "type": "Input",
                  "values": "",
                  "status": "custom",
                  "default": [
                    {
                      "name": "Starters",
                      "category": "Veg",
                      "values": ["Chinese", "Starters", "Main Course"]
                    },
                    {
                      "name": "Starters",
                      "category": "Non Veg",
                      "values": ["Chinese", "Starters", "Main Course"]
                    }
                  ],
                  "isActive": "true"
                },
                {
                  "name": "nutrition",
                  "title": "Nutritional Information",
                  "type": "Radio",
                  "values": "",
                  "status": "custom",
                  "isActive": "false"
                }
              ]
            },
            {
              "name": "taxMaster",
              "title": "Tax",
              "isActive": "true",
              "subMenu": [
                {
                  "name": "taxName",
                  "title": "Tax Name",
                  "type": "Input",
                  "values": "",
                  "isActive": "true"
                }
              ]
            },
            {
              "name": "customerMaster",
              "title": "Customers Master",
              "isActive": "true",
              "subMenu": [
                {
                  "name": "customerName",
                  "type": "Input",
                  "title": "Customer Name",
                  "values": "",
                  "isActive": "true"
                },
                {
                  "name": "customerMobile",
                  "title": "Customer Mobile",
                  "type": "Input",
                  "values": "",
                  "isActive": "true"
                },
                {
                  "name": "customerEmail",
                  "title": "Customer Email",
                  "type": "Input",
                  "values": "",
                  "isActive": "true"
                },
                {
                  "name": "customerLastVisit",
                  "title": "Customer Last Visit",
                  "type": "Input",
                  "values": "Date",
                  "isActive": "true"
                },
                {
                  "name": "customerAddr",
                  "title": "Customer Address",
                  "type": "Input",
                  "values": "Address String",
                  "isActive": "true"
                },
                {
                  "name": "customerHistory",
                  "title": "Customer History",
                  "values": [
                    {
                      "visitOn": "date",
                      "type": "Input",
                      "orderedItems": ["asas", "asdas", "asdasd"],
                      "lastAmount": "200"
                    }
                  ],
                  "isActive": "true"
                }
              ]
            },
            {
              "name": "employeeMaster",
              "title": "Employee Master",
              "isActive": "true",
              "subMenu": [
                {
                  "name": "employeeName",
                  "title": "Employee Name",
                  "type": "Input",
                  "values": "",
                  "isActive": "true"
                },
                {
                  "name": "employeeMobile",
                  "title": "Employee Mobile",
                  "type": "Input",
                  "values": "",
                  "isActive": "true"
                },
                {
                  "name": "employeeEmail",
                  "title": "Employee Email",
                  "type": "Input",
                  "values": "",
                  "isActive": "true"
                },
                {
                  "name": "employeeAddr",
                  "title": "Employee Address",
                  "type": "Input",
                  "values": "Address String",
                  "isActive": "true"
                },
                {
                  "name": "employeeHistory",
                  "title": "Employee History",
                  "values": [
                    {
                      "joining": "date",
                      "type": "Input",
                      "salaryDate": "Date",
                      "salary": 200
                    }
                  ],
                  "isActive": "true"
                },
                {
                  "name": "employeeVerification",
                  "title": "Employee Verification",
                  "values": [
                    {
                      "type": "Upload",
                      "proofType": "Adhar",
                      "proofDoc": "photo path"
                    }
                  ],
                  "isActive": "true"
                }
              ]
            }
          ]
        },
        {
          "name": "Items",
          "icon": "Items",
          "path": "/items",
          "title": "Foods",
          "isActive": "true",
          "default": "true",
          "subcategories": [
            {
              "name": "items",
              "title": "Items",
              "isActive": "true",
              "subMenu": [
                {
                  "name": "itemCode",
                  "title": "Food Code",
                  "isActive": "true",
                  "type": "text",
                  "placeholder": "Enter Food Code"
                },
                {
                  "name": "itemName",
                  "title": "Food Name",
                  "isActive": "true",
                  "type": "text",
                  "placeholder": "Enter Food Name"
                },
                {
                  "name": "itemCategory",
                  "title": "Food Category",
                  "isActive": "true",
                  "type": "DropDown",
                  "values": ["Naved", "Naik"],
                  "placeholder": "Choose Food Category"
                },
                {
                  "name": "itemSubCategory",
                  "title": "Food Sub Category",
                  "isActive": "true",
                  "type": "DropDown",
                  "values": ["Naved", "Naik"],
                  "placeholder": "Choose Food Sub Category"
                },
                {
                  "name": "itemPrice",
                  "title": "Food Price",
                  "isActive": "true",
                  "type": "text",
                  "placeholder": "Enter Food Price"
                },
                {
                  "name": "ingredients",
                  "title": "Ingredients",
                  "isActive": "true",
                  "type": "DropDown",
                  "values": ["category one", "category 2"],
                  "placeholder": "Enter Food Ingredients"
                },
                {
                  "name": "recipe",
                  "title": "Food Recipe",
                  "isActive": "true",
                  "type": "DropDown",
                  "values": ["category one", "category 2"],
                  "placeholder": "Enter Food Recipe"
                },
                {
                  "name": "allergen",
                  "title": "Allergen Information",
                  "isActive": "true",
                  "type": "text",
                  "placeholder": "Something allergic to this food"
                },
                {
                  "name": "portionSize",
                  "title": "Portion Size",
                  "isActive": "true",
                  "type": "text",
                  "placeholder": "How Many It Can Serve"
                },
                {
                  "name": "status",
                  "title": "Status",
                  "isActive": "true",
                  "type": "text",
                  "placeholder": "Is It Available"
                },
                {
                  "name": "tax",
                  "title": "Taxable",
                  "isActive": "true",
                  "type": "text",
                  "placeholder": "Enter Tax"
                },
                {
                  "name": "discount",
                  "title": "Discount",
                  "isActive": "true",
                  "type": "text",
                  "placeholder": "Enter Discount"
                },
                {
                  "name": "images",
                  "title": "Images",
                  "isActive": "true",
                  "value": [{}],
                  "type": "upload",
                  "placeholder": "Upload Pics"
                },
                {
                  "name": "currentStock",
                  "title": "Current Stock",
                  "isActive": "true",
                  "type": "text",
                  "placeholder": "Items in stock"
                },
                {
                  "name": "barcode",
                  "title": "Bar Code",
                  "isActive": "true",
                  "type": "text",
                  "placeholder": "Enter Barcode"
                },
                {
                  "name": "salesHistory",
                  "title": "Sales History",
                  "isActive": "true",
                  "value": [{}]
                },
                {
                  "name": "customNotes",
                  "title": "Notes",
                  "isActive": "true",
                  "type": "text",
                  "placeholder": "Enter more details"
                }
              ]
            }
          ]
        },
        {
          "name": "Tables",
          "icon": "Tables",
          "path": "/tables",
          "title": "Tables",
          "isActive": "true",
          "default": "true",
          "subcategories": [
            {
              "name": "tables",
              "title": "Tables",
              "isActive": "true",
              "subMenu": [
                {
                  "name": "tableCode",
                  "title": "Table Code",
                  "isActive": "true",
                  "type": "text",
                  "placeholder": "Enter Table Code"
                },
                {
                  "name": "tableName",
                  "title": "Table Name",
                  "isActive": "true",
                  "type": "text",
                  "placeholder": "Enter Table Name"
                },
                {
                  "name": "tableStatus",
                  "title": "Table Status",
                  "isActive": "true",
                  "type": "DropDown",
                  "values": ["Open", "Vaccant", "Closed", "Dirty"],
                  "placeholder": "Choose Table Status"
                },
                {
                  "name": "tablePlacement",
                  "title": "Table Placement",
                  "isActive": "true",
                  "type": "DropDown",
                  "values": ["Lawn", "Terrace"],
                  "placeholder": "Choose Table Location"
                },

                {
                  "name": "tableQR",
                  "title": "Table QR",
                  "isActive": "true",
                  "type": "text",
                  "placeholder": "Enter Table QR Code"
                }
              ]
            }
          ]
        },
        {
          "name": "Employees",
          "icon": "Employees",
          "path": "/employees",
          "title": "Employees",
          "isActive": "true",
          "default": "true",
          "subcategories": [
            {
              "name": "employeea",
              "title": "Employees",
              "isActive": "true",
              "subMenu": [
                {
                  "name": "employeeCode",
                  "title": "Employee Code",
                  "isActive": "true",
                  "type": "text",
                  "placeholder": "Enter Employee Code"
                },
                {
                  "name": "employeeName",
                  "title": "Employee Name",
                  "isActive": "true",
                  "type": "text",
                  "placeholder": "Enter Employee Name"
                },
                {
                  "name": "employeeEmail",
                  "title": "Employee Email",
                  "isActive": "true",
                  "type": "text",
                  "values": [],
                  "placeholder": "Enter Employeee Email"
                },
                {
                  "name": "employeeMobile",
                  "title": "Employee Mobile",
                  "isActive": "true",
                  "type": "text",
                  "values": ["Lawn", "Terrace"],
                  "placeholder": "Choose Table Location"
                },

                {
                  "name": "employeeAddr",
                  "title": "Employee Address",
                  "isActive": "true",
                  "type": "text",
                  "placeholder": "Enter Address"
                },
                {
                  "name": "employeeVerify",
                  "title": "Employee Verification",
                  "isActive": "true",
                  "type": "upload",
                  "placeholder": "Choose ID Proofs"
                }
              ]
            }
          ]
        },
        {
          "name": "Vendors",
          "icon": "Vendors",
          "path": "/vendors",
          "title": "Vendors",
          "isActive": "true",
          "default": "true",
          "subcategories": [
            {
              "name": "vendors",
              "title": "Vendors",
              "isActive": "true",
              "subMenu": [
                {
                  "name": "vendorCode",
                  "title": "Vendor Code",
                  "isActive": "true",
                  "type": "text",
                  "placeholder": "Enter Vendor Code"
                },
                {
                  "name": "vendorName",
                  "title": "Vendor Name",
                  "isActive": "true",
                  "type": "text",
                  "placeholder": "Enter Vendor Name"
                },
                {
                  "name": "vendorEmail",
                  "title": "Vendor Email",
                  "isActive": "true",
                  "type": "text",
                  "values": [],
                  "placeholder": "Enter Vendor Email"
                },
                {
                  "name": "vendorMobile",
                  "title": "Vendor Mobile",
                  "isActive": "true",
                  "type": "text",
                  "values": ["Lawn", "Terrace"],
                  "placeholder": "Choose Vendor Location"
                },

                {
                  "name": "vendorAddr",
                  "title": "Vendor Address",
                  "isActive": "true",
                  "type": "text",
                  "placeholder": "Enter Address"
                }
              ]
            }
          ]
        }
      ]
    }
    



