from collections import deque
from datetime import datetime

from entity import Entity
from flask import jsonify
from functools import reduce
import json


class Database:
    accounts_map = {}
    transactions = deque()
    total_points = 0
    status_code = 200

    def __init__(self, arg1=None, arg2=None):
        self.arg1 = arg1
        self.arg2 = arg2

    def get_or_create(self, user_id):
        if user_id in self.accounts_map:
            return self.accounts_map.get(user_id)
        new_list = []
        self.accounts_map[user_id] = new_list
        return new_list

    def add_transaction(self, user_Id, payer, points, timestamp):
        print(type(payer),type(points))
        if type(payer) != str:
            self.status_code = 400
            return "Invalid input format for \'payer\' must be a string",int(self.status_code)
        if type(points) != int:
            self.status_code = 400
            return "Invalid input format for \'points\' must be a number",int(self.status_code)

        user_points = self.get_or_create(user_Id)
        new_entity = Entity(payer, points, timestamp)
        new_entity.spent = 0
        user_points.append(new_entity)
        return "Points Added Successfully!", int(self.status_code)

    def reduce_helper(self, user_points):
        acc = {}
        for i in user_points:
            curr_sum = acc.get(i.payer, 0)
            acc[i.payer] = curr_sum + i.points
        return acc

    def get_balances(self, user_id):
        user_points = self.accounts_map.get(user_id)
        return self.reduce_helper(user_points)

    def create_plan(self, user_id, points):
        user_points = self.get_or_create(user_id)
        copied_points = user_points.copy()
        copied_points.sort(key=lambda x: x.timestamp)
        positive_points = []
        for i in copied_points:
            if i.points > 0:
                positive_points.append(i)
            elif i.points < 0:
                points_left_to_neutralize = -i.points
                payer_points = list(filter(lambda x: x.payer == i.payer != 0, positive_points))
                j = 0
                while j < len(payer_points) and points_left_to_neutralize > 0:
                    points_to_neutralize_now = min(points_left_to_neutralize, payer_points[j].points)
                    points_left_to_neutralize -= points_to_neutralize_now
                    payer_points[j].points -= points_to_neutralize_now
                    j += 1

        points_left_to_spend = points
        payer_map = {}
        k = 0
        while k < len(positive_points) and points_left_to_spend > 0:
            transaction = positive_points[k]
            if transaction.payer not in payer_map:
                payer_map[transaction.payer] = 0
            points_to_spend_now = min(points_left_to_spend, transaction.points)
            points_left_to_spend -= points_to_spend_now
            payer_map[transaction.payer] = payer_map.get(transaction.payer) - points_to_spend_now
            k += 1

        return payer_map

    #
    # def serialize(self, e):
    #     return {
    #         'payer': e.payer,
    #         'points': e.points,
    #     }
