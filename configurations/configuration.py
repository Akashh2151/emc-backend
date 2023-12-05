

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
