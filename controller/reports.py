import datetime
from mongoengine.queryset.visitor import Q
from flask import Blueprint, jsonify, request
from model.reports_model import Expense
from model.resto_model import Item


reports=Blueprint('reports',__name__)

import datetime
from mongoengine.queryset.visitor import Q
from flask import Blueprint, jsonify, request
from model.reports_model import Expense
from model.resto_model import Item

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


@reports.route('/akash')
def hello_world():
      return jsonify({'message': 'hi All team'}), 200