from flask import Flask, jsonify, request
import datetime as dt
from dateutil.relativedelta import *

app = Flask(__name__)


def calculate_deposit(date, periods, amount, rate):
    if periods < 1 or periods > 60:
        return {"error": "periods are not valid"}, 400
    if amount < 10000 or amount > 3000000:
        return {"error": "amount is not valid"}, 400
    if rate < 1 or rate > 8:
        return {"error": "rate is not valid"}, 400

    result = {}
    for i in range(periods):
        interest = amount * rate / 12 / 100
        amount += interest
        result[(date + relativedelta(months=+i)).strftime('%d.%m.%Y')] = int(amount) if amount.is_integer() else round(amount, 2)

    return result, 200


@app.route("/", methods=['POST'])
def deposit():
    try:
        data = request.json
        date = dt.datetime.strptime(data['date'], "%d.%m.%Y").date()
        periods = data['periods']
        amount = data['amount']
        rate = data['rate']
        result, status_code = calculate_deposit(date, periods, amount, rate)
        return jsonify(result), status_code
    except (TypeError, ValueError):
        return jsonify({"error": "data is not valid"}), 400
