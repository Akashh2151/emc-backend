


import json


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
          "isActive": True,
          "default": True,
          "subcategories": [
            {
              "name": "Orders",
              "title": "Orders",
              "isActive": True,
              "subMenu": [
                {
                  "name": "vendorCode",
                  "title": "Vendor Code",
                  "isActive": True,
                  "type": "text",
                  "placeholder": "Enter Vendor Code"
                },
                {
                  "name": "vendorName",
                  "title": "Vendor Name",
                  "isActive": True,
                  "type": "text",
                  "placeholder": "Enter Vendor Name"
                },
                {
                  "name": "vendorEmail",
                  "title": "Vendor Email",
                  "isActive": True,
                  "type": "text",
                  "values": [],
                  "placeholder": "Enter Vendor Email"
                },
                {
                  "name": "vendorMobile",
                  "title": "Vendor Mobile",
                  "isActive": True,
                  "type": "text",
                  "values": ["Lawn", "Terrace"],
                  "placeholder": "Choose Vendor Location"
                },

                {
                  "name": "vendorAddr",
                  "title": "Vendor Address",
                  "isActive": True,
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
          "isActive": True,
          "default": True,
          "subcategories": [
            {
              "name": "menuMaster",
              "title": "Menu",
              "isActive": True,
              "subMenu": []
            },
            {
              "name": "itemMaster",
              "title": "Items",
              "isActive": True,
              "subMenu": [
                {
                  "name": "name",
                  "title": "Food Name",
                  "values": "",
                  "type": "Input",
                  "isActive": True,
                  "status": "default"
                },
                {
                  "name": "description",
                  "title": "Food Description",
                  "values": "",
                  "type": "Input",
                  "isActive": True,
                  "status": "custom"
                },
                {
                  "name": "measureUnit",
                  "title": "Units",
                  "type": "DropDown",
                  "values": ["Kg", "PC", "Unit"],
                  "isActive": True,
                  "status": "default"
                },
                {
                  "name": "price",
                  "title": "Price",
                  "type": "Input",
                  "values": "INR",
                  "default": ["INR", "Dollar"],
                  "isActive": True,
                  "status": "default"
                },
                {
                  "name": "category",
                  "title": "Category",
                  "type": "Input",
                  "values": "",
                  "default": ["Veg", "Non Veg"],
                  "isActive": True,
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
                  "isActive": True
                },
                {
                  "name": "nutrition",
                  "title": "Nutritional Information",
                  "type": "Radio",
                  "values": "",
                  "status": "custom",
                  "isActive": False
                }
              ]
            },
            {
              "name": "taxMaster",
              "title": "Tax",
              "isActive": True,
              "subMenu": [
                {
                  "name": "taxName",
                  "title": "Tax Name",
                  "type": "Input",
                  "values": "",
                  "isActive": True
                }
              ]
            },
            {
              "name": "customerMaster",
              "title": "Customers Master",
              "isActive": True,
              "subMenu": [
                {
                  "name": "customerName",
                  "type": "Input",
                  "title": "Customer Name",
                  "values": "",
                  "isActive": True
                },
                {
                  "name": "customerMobile",
                  "title": "Customer Mobile",
                  "type": "Input",
                  "values": "",
                  "isActive": True
                },
                {
                  "name": "customerEmail",
                  "title": "Customer Email",
                  "type": "Input",
                  "values": "",
                  "isActive": True
                },
                {
                  "name": "customerLastVisit",
                  "title": "Customer Last Visit",
                  "type": "Input",
                  "values": "Date",
                  "isActive": True
                },
                {
                  "name": "customerAddr",
                  "title": "Customer Address",
                  "type": "Input",
                  "values": "Address String",
                  "isActive": True
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
                  "isActive": True
                }
              ]
            },
            {
              "name": "employeeMaster",
              "title": "Employee Master",
              "isActive": True,
              "subMenu": [
                {
                  "name": "employeeName",
                  "title": "Employee Name",
                  "type": "Input",
                  "values": "",
                  "isActive": True
                },
                {
                  "name": "employeeMobile",
                  "title": "Employee Mobile",
                  "type": "Input",
                  "values": "",
                  "isActive": True
                },
                {
                  "name": "employeeEmail",
                  "title": "Employee Email",
                  "type": "Input",
                  "values": "",
                  "isActive": True
                },
                {
                  "name": "employeeAddr",
                  "title": "Employee Address",
                  "type": "Input",
                  "values": "Address String",
                  "isActive": True
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
                  "isActive": True
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
                  "isActive": True
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
          "isActive": True,
          "default": True,
          "subcategories": [
            {
              "name": "items",
              "title": "Items",
              "isActive": True,
              "subMenu": [
                {
                  "name": "itemCode",
                  "title": "Food Code",
                  "isActive": True,
                  "type": "text",
                  "placeholder": "Enter Food Code"
                },
                {
                  "name": "itemName",
                  "title": "Food Name",
                  "isActive": True,
                  "type": "text",
                  "placeholder": "Enter Food Name"
                },
                {
                  "name": "itemCategory",
                  "title": "Food Category",
                  "isActive": True,
                  "type": "DropDown",
                  "values": ["Naved", "Naik"],
                  "placeholder": "Choose Food Category"
                },
                {
                  "name": "itemSubCategory",
                  "title": "Food Sub Category",
                  "isActive": True,
                  "type": "DropDown",
                  "values": ["Naved", "Naik"],
                  "placeholder": "Choose Food Sub Category"
                },
                {
                  "name": "itemPrice",
                  "title": "Food Price",
                  "isActive": True,
                  "type": "text",
                  "placeholder": "Enter Food Price"
                },
                {
                  "name": "ingredients",
                  "title": "Ingredients",
                  "isActive": True,
                  "type": "DropDown",
                  "values": ["category one", "category 2"],
                  "placeholder": "Enter Food Ingredients"
                },
                {
                  "name": "recipe",
                  "title": "Food Recipe",
                  "isActive": True,
                  "type": "DropDown",
                  "values": ["category one", "category 2"],
                  "placeholder": "Enter Food Recipe"
                },
                {
                  "name": "allergen",
                  "title": "Allergen Information",
                  "isActive": True,
                  "type": "text",
                  "placeholder": "Something allergic to this food"
                },
                {
                  "name": "portionSize",
                  "title": "Portion Size",
                  "isActive": True,
                  "type": "text",
                  "placeholder": "How Many It Can Serve"
                },
                {
                  "name": "status",
                  "title": "Status",
                  "isActive": True,
                  "type": "text",
                  "placeholder": "Is It Available"
                },
                {
                  "name": "tax",
                  "title": "Taxable",
                  "isActive": True,
                  "type": "text",
                  "placeholder": "Enter Tax"
                },
                {
                  "name": "discount",
                  "title": "Discount",
                  "isActive": True,
                  "type": "text",
                  "placeholder": "Enter Discount"
                },
                {
                  "name": "images",
                  "title": "Images",
                  "isActive": True,
                  "value": [{}],
                  "type": "upload",
                  "placeholder": "Upload Pics"
                },
                {
                  "name": "currentStock",
                  "title": "Current Stock",
                  "isActive": True,
                  "type": "text",
                  "placeholder": "Items in stock"
                },
                {
                  "name": "barcode",
                  "title": "Bar Code",
                  "isActive": True,
                  "type": "text",
                  "placeholder": "Enter Barcode"
                },
                {
                  "name": "salesHistory",
                  "title": "Sales History",
                  "isActive": True,
                  "value": [{}]
                },
                {
                  "name": "customNotes",
                  "title": "Notes",
                  "isActive": True,
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
          "isActive": True,
          "default": True,
          "subcategories": [
            {
              "name": "tables",
              "title": "Tables",
              "isActive": True,
              "subMenu": [
                {
                  "name": "tableCode",
                  "title": "Table Code",
                  "isActive": True,
                  "type": "text",
                  "placeholder": "Enter Table Code"
                },
                {
                  "name": "tableName",
                  "title": "Table Name",
                  "isActive": True,
                  "type": "text",
                  "placeholder": "Enter Table Name"
                },
                {
                  "name": "tableStatus",
                  "title": "Table Status",
                  "isActive": True,
                  "type": "DropDown",
                  "values": ["Open", "Vaccant", "Closed", "Dirty"],
                  "placeholder": "Choose Table Status"
                },
                {
                  "name": "tablePlacement",
                  "title": "Table Placement",
                  "isActive": True,
                  "type": "DropDown",
                  "values": ["Lawn", "Terrace"],
                  "placeholder": "Choose Table Location"
                },

                {
                  "name": "tableQR",
                  "title": "Table QR",
                  "isActive": True,
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
          "isActive": True,
          "default": True,
          "subcategories": [
            {
              "name": "employeea",
              "title": "Employees",
              "isActive": True,
              "subMenu": [
                {
                  "name": "employeeCode",
                  "title": "Employee Code",
                  "isActive": True,
                  "type": "text",
                  "placeholder": "Enter Employee Code"
                },
                {
                  "name": "employeeName",
                  "title": "Employee Name",
                  "isActive": True,
                  "type": "text",
                  "placeholder": "Enter Employee Name"
                },
                {
                  "name": "employeeEmail",
                  "title": "Employee Email",
                  "isActive": True,
                  "type": "text",
                  "values": [],
                  "placeholder": "Enter Employeee Email"
                },
                {
                  "name": "employeeMobile",
                  "title": "Employee Mobile",
                  "isActive": True,
                  "type": "text",
                  "values": ["Lawn", "Terrace"],
                  "placeholder": "Choose Table Location"
                },

                {
                  "name": "employeeAddr",
                  "title": "Employee Address",
                  "isActive": True,
                  "type": "text",
                  "placeholder": "Enter Address"
                },
                {
                  "name": "employeeVerify",
                  "title": "Employee Verification",
                  "isActive": True,
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
          "isActive": True,
          "default": True,
          "subcategories": [
            {
              "name": "vendors",
              "title": "Vendors",
              "isActive": True,
              "subMenu": [
                {
                  "name": "vendorCode",
                  "title": "Vendor Code",
                  "isActive": True,
                  "type": "text",
                  "placeholder": "Enter Vendor Code"
                },
                {
                  "name": "vendorName",
                  "title": "Vendor Name",
                  "isActive": True,
                  "type": "text",
                  "placeholder": "Enter Vendor Name"
                },
                {
                  "name": "vendorEmail",
                  "title": "Vendor Email",
                  "isActive": True,
                  "type": "text",
                  "values": [],
                  "placeholder": "Enter Vendor Email"
                },
                {
                  "name": "vendorMobile",
                  "title": "Vendor Mobile",
                  "isActive": True,
                  "type": "text",
                  "values": ["Lawn", "Terrace"],
                  "placeholder": "Choose Vendor Location"
                },

                {
                  "name": "vendorAddr",
                  "title": "Vendor Address",
                  "isActive": True,
                  "type": "text",
                  "placeholder": "Enter Address"
                }
              ]
            }
          ]
        }
      ]
    }
    

# Convert JSON to Python dictionary
# resto_dict = json.loads(json.dumps(resto_data))
