from flask import Flask
import json
import requests
from routes import app
import uuid


class Tester:
    id = uuid.uuid4()

    def test_base_route(self):
        client = app.test_client()
        url = '/'
        response = client.get(url)
        assert response.get_data() == b'FETCH REWARDS ASSIGNMENT'
        assert response.status_code == 200
        print("SERVER ACTIVE")

    def test_post_route__success(self):
        client = app.test_client()
        url = "http://127.0.0.1:5000/points/user/{}/transaction".format(id)
        response = client.post(url, json={"payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z"})
        data = response.data.decode('utf-8')
        assert data == "Points Added Successfully!"
        assert response.status_code == 200

        response = client.post(url, json={"payer": "UNILEVER", "points": 200, "timestamp": "2020-10-31T11:00:00Z"})
        data = response.data.decode('utf-8')
        assert data == "Points Added Successfully!"
        assert response.status_code == 200

        response = client.post(url, json={"payer": "DANNON", "points": -200, "timestamp": "2020-10-31T15:00:00Z"})
        data = response.data.decode('utf-8')
        assert data == "Points Added Successfully!"
        assert response.status_code == 200

        response = client.post(url,
                               json={"payer": "MILLER COORS", "points": 10000, "timestamp": "2020-11-01T14:00:00Z"})
        data = response.data.decode('utf-8')
        assert data == "Points Added Successfully!"
        assert response.status_code == 200

        response = client.post(url, json={"payer": "DANNON", "points": 300, "timestamp": "2020-10-31T10:00:00Z"})
        data = response.data.decode('utf-8')
        assert data == "Points Added Successfully!"
        assert response.status_code == 200
        print("ALL PAYER POINTS ADDED SUCCESSFULLY")
        self.test_balance()

    def test_balance(self):
        client = app.test_client()
        url = "http://127.0.0.1:5000/points/user/{}/balances".format(id)
        response = client.get(url)
        assert response.status_code == 200
        print(response.json)

    def test_spending(self):
        client = app.test_client()
        url = "http://127.0.0.1:5000/points/user/{}/spend".format(id)
        response = client.post(url, json={"points": 5000})
        data = response.data.decode('utf-8')
        print(data)
        assert response.status_code == 200



if __name__ == "__main__":
    tester = Tester()
    tester.test_base_route()
    tester.test_post_route__success()
    tester.test_spending()
