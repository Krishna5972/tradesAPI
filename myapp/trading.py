from flask import Blueprint,request,jsonify
from binance.client import Client
from .services import *


trading = Blueprint('trading', __name__)


cache = {}

@trading.route('/test', methods = ['POST','GET'])
def trade():
    return "Trade endpoint response"

@trading.route('/getIncome', methods = ['POST','GET'])
def get_trades():

    if request.method == 'POST':
        if not request.is_json:
            return jsonify({"error": "Missing JSON in request"}), 400

        api_key = request.json.get('api_key')
        secret_key = request.json.get('secret_key')

        if not api_key or not secret_key:
            return jsonify({"error": "API key and Secret key are required"}), 400
        
    df_income = fetch_income_history(api_key, secret_key)
    cache['income_history'] = df_income

    data = df_income.to_dict('records')
    return jsonify(data)


@trading.route('/getFunding', methods=['GET','POST'])
def get_funding():

    if request.method == 'POST':
        if not request.is_json:
            return jsonify({"error": "Missing JSON in request"}), 400

        api_key = request.json.get('api_key')
        secret_key = request.json.get('secret_key')

        if not api_key or not secret_key:
            return jsonify({"error": "API key and Secret key are required"}), 400

    df_income = cache.get('income_history')
    if df_income is None:
        df_income = fetch_income_history(api_key, secret_key)
        cache['income_history'] = df_income

    df_funding = df_income[df_income['incomeType'] == 'FUNDING_FEE']

    funding_data = df_funding.to_dict('records')
    return jsonify(funding_data)


@trading.route('/getCommission', methods=['GET','POST'])
def get_commission():

    if request.method == 'POST':
        if not request.is_json:
            return jsonify({"error": "Missing JSON in request"}), 400

        api_key = request.json.get('api_key')
        secret_key = request.json.get('secret_key')

        if not api_key or not secret_key:
            return jsonify({"error": "API key and Secret key are required"}), 400

    df_income = cache.get('income_history')
    if df_income is None:
        df_income = fetch_income_history(api_key, secret_key)
        cache['income_history'] = df_income

    df_funding = df_income[df_income['incomeType'] == 'COMMISSION']

    funding_data = df_funding.to_dict('records')
    return jsonify(funding_data)



@trading.route('/getAccountHistory', methods=['GET','POST'])
def get_account_history():

    if request.method == 'POST':
        if not request.is_json:
            return jsonify({"error": "Missing JSON in request"}), 400

        api_key = request.json.get('api_key')
        secret_key = request.json.get('secret_key')

        if not api_key or not secret_key:
            return jsonify({"error": "API key and Secret key are required"}), 400
        
    account_history = fetch_account_history(api_key, secret_key)
    cache['account_history'] = account_history

    data = account_history.to_dict('records')
    return jsonify(data)


@trading.route('/getPositionHistory', methods=['GET','POST'])
def get_position_history():

    if request.method == 'POST':
        if not request.is_json:
            return jsonify({"error": "Missing JSON in request"}), 400

        api_key = request.json.get('api_key')
        secret_key = request.json.get('secret_key')

        if not api_key or not secret_key:
            return jsonify({"error": "API key and Secret key are required"}), 400


    account_history = cache.get('account_history')
    if account_history is None:
        account_history = fetch_account_history(api_key, secret_key)
        cache['account_history'] = account_history

    PNL = get_position_from_account(account_history)

    cache['PNL'] = PNL

    data = PNL.to_dict('records')
    return jsonify(data)



@trading.route('/getBalance', methods=['GET','POST'])
def get_balance():
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({"error": "Missing JSON in request"}), 400

        api_key = request.json.get('api_key')
        secret_key = request.json.get('secret_key')

        if not api_key or not secret_key:
            return jsonify({"error": "API key and Secret key are required"}), 400

    balance = fetch_balance(api_key,secret_key)

    data = {
        'balance' : balance
    }

    return jsonify(data)




@trading.route('/getOpenOrders', methods=['GET','POST'])
def get_open_orders():
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({"error": "Missing JSON in request"}), 400

        api_key = request.json.get('api_key')
        secret_key = request.json.get('secret_key')

        if not api_key or not secret_key:
            return jsonify({"error": "API key and Secret key are required"}), 400

    open_orders_df = fetch_open_orders(api_key,secret_key)
    if open_orders_df.empty:
        return jsonify({"message": "No open orders found", "data": []})

    data = open_orders_df.to_dict('records')
    
    return jsonify({"message": "Retrieved open orders successfully", "data": data})


@trading.route('/getOpenPositions', methods=['GET','POST'])
def get_open_positions():
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({"error": "Missing JSON in request"}), 400

        api_key = request.json.get('api_key')
        secret_key = request.json.get('secret_key')

        if not api_key or not secret_key:
            return jsonify({"error": "API key and Secret key are required"}), 400

    open_orders_df = fetch_open_positions(api_key,secret_key)
    if open_orders_df.empty:
        return jsonify({"message": "No open positions found", "data": []})

    data = open_orders_df.to_dict('records')
    
    return jsonify({"message": "Retrieved open positions successfully", "data": data})