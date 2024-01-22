from flask import Blueprint, jsonify, request
from model.reports_model import Expense
from model.resto_model import Item


reports=Blueprint('reports',__name__)


# Report API
@reports.route('/v1/reports', methods=['GET'])
def generate_report():
    try:
        # Get query parameters for year and month
        year = request.args.get('year')
        month = request.args.get('month')

        # Validate year and month
        if not year or not month:
            return jsonify({'body': None, 'status': 'error', 'message': 'Year and month are required query parameters.', 'statusCode': 400}), 200

        # Get items with sales history for the specified year and month
        items = Item.objects(salesHistory__date__year=year, salesHistory__date__month=month)

        # Initialize report data
        report = {
            'year': year,
            'month': month,
            'total_purchase': 0.0,
            'total_sales': 0.0,
            'total_expense': 0.0
        }

        # Calculate totals based on sales history actions
        for item in items:
            for purchase_entry in item.purchasesHistory:
                if purchase_entry.date.year == int(year) and purchase_entry.date.month == int(month):
                    report['total_purchase'] += item.itemPrice

            for sale_entry in item.salesHistory:
                if sale_entry.date.year == int(year) and sale_entry.date.month == int(month):
                    report['total_sales'] += item.itemPrice

        # Calculate total expenses
        expenses = Expense.objects(expenses__date__year=year, expenses__date__month=month)
        report['total_expense'] = sum(expense.amount for expense in expenses)

        return jsonify({'body': report, 'status': 'success', 'statusCode': 200, 'message': 'Report generated successfully.'}), 200

    except Exception as e:
        return jsonify({'body': None, 'error': str(e), 'statusCode': 500}), 200




@reports.route('/akash')
def hello_world():
      return jsonify({'message': 'hi All team'}), 200