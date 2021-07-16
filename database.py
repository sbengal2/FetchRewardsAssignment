from collections import deque

from flask import jsonify

from transaction_entity import TransactionEntity


class Database:
    points_database = {}
    transactions = deque()
    total_points = 0
    status_code = 200

    def __init__(self, arg1=None, arg2=None):
        self.arg1 = arg1
        self.arg2 = arg2

    def get_payer_list(self, user_id):
        if user_id in self.points_database:
            return self.points_database.get(user_id)
        payer_list = []
        self.points_database[user_id] = payer_list
        return payer_list

    def add_transaction(self, user_Id, payer, points, timestamp):
        if type(payer) != str:
            self.status_code = 400
            return "Invalid input format for \'payer\' must be a string", int(self.status_code)

        if type(points) != int:
            self.status_code = 400
            return "Invalid input format for \'points\' must be a number", int(self.status_code)

        user_transactions = self.get_payer_list(user_Id)
        new_transaction = TransactionEntity(payer, points, timestamp)
        user_transactions.append(new_transaction)
        return "Points Added Successfully!", int(self.status_code)

    def reduce_helper(self, user_transactions):
        acc = {}
        for transaction in user_transactions:
            curr_sum = acc.get(transaction.payer, 0)
            acc[transaction.payer] = curr_sum + transaction.points
        return acc

    def get_balances(self, user_id):
        user_transactions = self.points_database.get(user_id)
        if not user_transactions:
            self.status_code = 400
            return "Cannot find user with such User ID", int(self.status_code)
        return jsonify(self.reduce_helper(user_transactions))

    def create_spending_plan(self, user_id, points):
        user_transactions = self.get_payer_list(user_id)
        copied_user_transactions = user_transactions.copy()
        copied_user_transactions.sort(key=lambda x: x.timestamp)

        positive_points = []
        for transaction in copied_user_transactions:
            if transaction.points > 0:
                positive_points.append(transaction)
            elif transaction.points < 0:
                points_left_to_neutralize = -transaction.points
                payer_points = list(filter(lambda x: x.payer == transaction.payer != 0, positive_points))
                i = 0
                while i < len(payer_points) and points_left_to_neutralize > 0:
                    points_to_neutralize_now = min(points_left_to_neutralize, payer_points[i].points)
                    points_left_to_neutralize -= points_to_neutralize_now
                    payer_points[i].points -= points_to_neutralize_now
                    i += 1

        points_left_to_spend = points
        payer_map = {}
        j = 0
        while j < len(positive_points) and points_left_to_spend > 0:
            transaction = positive_points[j]
            if transaction.payer not in payer_map:
                payer_map[transaction.payer] = 0
            points_to_spend_now = min(points_left_to_spend, transaction.points)
            points_left_to_spend -= points_to_spend_now
            payer_map[transaction.payer] = payer_map.get(transaction.payer) - points_to_spend_now
            j += 1

        return payer_map
