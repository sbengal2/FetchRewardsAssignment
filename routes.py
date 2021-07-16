import json
from datetime import datetime
from flask import request, Flask
from database import Database

db = Database()
app = Flask("web_server")


@app.route("/", methods=['GET'])
def get_response():
    return "FETCH REWARDS ASSIGNMENT"


@app.route("/points/user/<user_id>/transaction", methods=['POST'])
def add_transaction(user_id):
    data = request.get_json(force=True)
    payer = str(data['payer'])
    points = int(data['points'])
    timestamp = str(data['timestamp'])
    return db.add_transaction(user_id, payer, points, timestamp)


@app.route('/points/user/<user_id>/balances', methods=['GET'])
def get_balance_points(user_id):
    result = db.get_balances(user_id)
    return result

@app.route('/points/user/<user_id>/spend', methods=['POST'])
def spend(user_id):
    data = request.get_json(force=True)
    points = int(data['points'])
    spending_plans = db.create_spending_plan(user_id, points)

    points_spent = 0
    for i in spending_plans.values():
        points_spent += i
    if -points_spent < points:
        return "Not Enough points", int(400)

    spending_track = []
    my_date = datetime.now()
    timestamp = my_date.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
    for key, value in spending_plans.items():
        payer_information = {'payer': key, 'point': value}
        db.add_transaction(user_id, key, value, timestamp)
        spending_track.append(payer_information)

    return json.dumps(spending_track), 200


if __name__ == "__main__":
    app.run(debug=True)
