from datetime import datetime
from mongoengine.queryset.visitor import Q
from flask import Blueprint, jsonify, request
from model.reports_model import Expense
from model.resto_model import Item
# from dateutil import parser

reports=Blueprint('reports',__name__)

# import datetime
from mongoengine.queryset.visitor import Q
from flask import Blueprint, jsonify, request
from model.reports_model import Expense
from model.resto_model import Item


# itam report

reports = Blueprint('reports',__name__)
@reports.route('/v1/reports', methods=['GET'])
def generate_report():
    try:
        year = request.args.get('year', type=int)
        month = request.args.get('month', type=int)

        if year is None or month is None:
            return jsonify({'body': None, 'status': 'error', 'message': 'Year and month are required query parameters.', 'statusCode': 400}), 400

        report = {
            'year': year,
            'month': datetime.date(1900, month, 1).strftime('%B'),
            'purchases': {'purchase': 0, 'purchasecancel': 0, 'total': 0},
            'sales': {'sale': 0, 'salecancel': 0, 'total': 0},
            'totalExpense': 0.0
        }

        items = Item.objects.all()

        for item in items:
            for history in item.salesHistory:
                if history.date.year == year and history.date.month == month:
                    if history.action == 'purchase':
                        report['purchases']['purchase'] += 1
                    elif history.action == 'sale':
                        report['sales']['sale'] += 1
                    elif history.action == 'purchasecancel':
                        report['purchases']['purchasecancel'] += 1
                    elif history.action == 'salecancel':
                        report['sales']['salecancel'] += 1

        # Adding the total of purchase and purchasecancel
        report['purchases']['total'] = report['purchases']['purchase'] + report['purchases']['purchasecancel']
        # Adding the total of sale and salecancel
        report['sales']['total'] = report['sales']['sale'] + report['sales']['salecancel']

        start_date = datetime.datetime(year, month, 1)
        end_date = datetime.datetime(year, month + 1, 1) if month < 12 else datetime.datetime(year + 1, 1, 1)

        expenses = Expense.objects(Q(date__gte=start_date) & Q(date__lt=end_date))
        report['totalExpense'] = sum(expense.amount for expense in expenses)
        
          # Adding the sums of purchases and sales to the total expense
        report['totalExpense'] += report['purchases']['total'] + report['sales']['total']

        response = {
            "report": report,
            "status": "success",
            "statusCode": 200,
            "message": "Report entries retrieved successfully"
        }
        return jsonify(response), 200
    
        # return jsonify(response), 200
        
        

    except Exception as e:
        return jsonify({'body': None, 'error': str(e), 'statusCode': 500}), 500


# @reports.route('/v1/reports/most-sold', methods=['GET'])
# def most_sold_items():
#     try:
#         year = request.args.get('year', type=int)
#         month = request.args.get('month', type=int)

#         if year is None or month is None:
#             return jsonify({'body': None, 'status': 'error', 'message': 'Year and month are required query parameters.', 'statusCode': 400}), 400

#         items_sold = {}
#         items = Item.objects.all()
#         for item in items:
#             count = 0
#             for history in item.salesHistory:
#                 if history.date.year == year and history.date.month == month and history.action == 'sale':
#                     count += 1
#             if count > 0:
#                 items_sold[str(item.id)] = count  # Convert ObjectId to string

#         # Sort items by sold count in descending order
#         most_sold = sorted(items_sold.items(), key=lambda x: x[1], reverse=True)

#         return jsonify({'most_sold': most_sold, 'status': 'success', 'message': 'Most sold items retrieved successfully', 'statusCode': 200}), 200
#     except Exception as e:
#         return jsonify({'body': None, 'error': str(e), 'statusCode': 500}), 500
 


# @reports.route('/v1/reports/least-sold', methods=['GET'])
# def least_sold_items():
#     try:
#         year = request.args.get('year', type=int)
#         month = request.args.get('month', type=int)

#         if year is None or month is None:
#             return jsonify({'body': None, 'status': 'error', 'message': 'Year and month are required query parameters.', 'statusCode': 400}), 400

#         items_sold = {}
#         items = Item.objects.all()
#         for item in items:
#             count = 0
#             for history in item.salesHistory:
#                 if history.date.year == year and history.date.month == month and history.action == 'sale':
#                     count += 1
#             if count > 0:
#                 items_sold[str(item.id)] = count  # Convert ObjectId to string

#         # Sort items by sold count in ascending order
#         least_sold = sorted(items_sold.items(), key=lambda x: x[1])

#         return jsonify({'least_sold': least_sold, 'status': 'success', 'message': 'Least sold items retrieved successfully', 'statusCode': 200}), 200
#     except Exception as e:
#         return jsonify({'body': None, 'error': str(e), 'statusCode': 500}), 500

# @reports.route('/v1/reports/quantity-remaining', methods=['GET'])
# def quantity_remaining():
#     try:
#         order = request.args.get('order', default='asc', type=str)
#         if order not in ['asc', 'desc']:
#             return jsonify({'body': None, 'status': 'error', 'message': 'Order must be either "asc" or "desc".', 'statusCode': 400}), 400

#         items = Item.objects.all()
#         items_with_stock = {str(item.id): item.currentStock for item in items if item.currentStock is not None}

#         # Sort items by current stock
#         sorted_items = sorted(items_with_stock.items(), key=lambda x: x[1], reverse=(order == 'desc'))
        
#         return jsonify({'sorted_items': sorted_items, 'status': 'success', 'message': 'Items sorted by current stock successfully', 'statusCode': 200}), 200
#     except Exception as e:
#         return jsonify({'body': None, 'error': str(e), 'statusCode': 500}), 500

# @reports.route('/akash')
# def hello_world():
#       return jsonify({'message': 'hi All team'}), 200


@reports.route('/v1/reports/overview', methods=['GET'])
def reports_overview():
    try:
        # Extract query parameters
        date_str = request.args.get('date', type=str)  # Expected format: 'YYYY-MM'
        column = request.args.get('column', type=str)
        sort_order = request.args.get('sort', default='asc', type=str)

        # Validate and parse the date
        if date_str is None:
            return jsonify({'message': 'Date is a required query parameter.', 'status': 'error', 'statusCode': 400}), 400
        try:
            year, month = map(int, date_str.split('-'))
        except ValueError:
            return jsonify({'message': 'Date format should be YYYY-MM.', 'status': 'error', 'statusCode': 400}), 400

        # Validate sort_order
        if sort_order not in ['asc', 'desc']:
            return jsonify({'message': 'Sort must be either "asc" or "desc".', 'status': 'error', 'statusCode': 400}), 400

        # Query items from the database
        items = Item.objects.all()
        items_report = []

        for item in items:
            report = {
                'itemName': item.itemName,
                'mostSold': 0,  # Placeholder, assuming you'll calculate this
                'leastSold': 0,  # Placeholder, assuming you'll calculate this
                'quantityRemaining': item.currentStock  # Assuming this is an attribute of your item model
            }
            sales_count = 0
            cancellations_count = 0
            
            for history in item.salesHistory:
                history_date = history.date.date()  # Assuming history.date is already a datetime object
                
                if history_date.year == year and history_date.month == month:
                    if history.action == 'sale':
                        sales_count += 1
                    elif history.action == 'salecancel':
                        cancellations_count += 1
            
            net_sales = sales_count - cancellations_count
            report['mostSold'] = net_sales  # Assuming mostSold is equivalent to net sales here
            # Adjust `leastSold` and other fields as necessary based on your logic
            report['leastSold'] = net_sales 
            items_report.append(report)

        # You may need to adjust the sorting logic based on your actual requirements
        items_report = sorted(items_report, key=lambda x: x.get(column, 0), reverse=(sort_order == 'desc'))

        # Construct the final response
        final_response = {
            'items': items_report,
            'status': 'success',
            'message': 'Report retrieved successfully',
            'statusCode': 200
        }

        return jsonify(final_response), 200
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error', 'statusCode': 500}), 500    