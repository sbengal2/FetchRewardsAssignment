import json

from flask import request, Flask
from database import Database
from datetime import datetime

db = Database()
app = Flask("web_server")


# Adds a transaction given Payer's name, points, and timestamp
@app.route("/", methods=['GET'])
def get_response():
    return ("Hello world")


@app.route("/points/user/<user_id>/transaction", methods=['POST'])
def add_transaction(user_id):
    data = request.get_json(force=True)
    payer = str(data['payer'])
    points = int(data['points'])
    timestamp = str(data['timestamp'])
    return db.add_transaction(user_id, payer, points, timestamp)


@app.route('/points/user/<user_id>/balances', methods=['GET'])
def get_balance(user_id):
    print(db.accounts_map)
    data = request.get_json(force=True)
    return db.get_balances(user_id),200


@app.route('/points/user/<user_id>/spend', methods=['POST'])
def spend(user_id):
    data = request.get_json(force=True)
    points = int(data['points'])
    plans = db.create_plan(user_id, points)
    points_spent = 0
    print(plans)
    for i in plans.values():
        points_spent += i
    if -points_spent < points:
        return "Not Enough points", int(400)
    summary = []
    my_date = datetime.now()
    timestamp = my_date.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
    for key, value in plans.items():
        temp = {'payer': key, 'point': value}
        db.add_transaction(user_id,key,value,timestamp)
        summary.append(temp)

    return json.dumps(summary),200


if __name__ == "__main__":
    app.run(debug=True)
