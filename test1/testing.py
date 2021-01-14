from unittest.mock import ANY
import unittest
from flask import url_for
from flask_testing import TestCase

from models import Show, User, Ticket
import json

from sqlalchemy.orm import close_all_sessions

#import urllib3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash

from app import app, engine, session
from models import Base

class BaseTestCase(TestCase):
    user_1 = {
        "name": "a",
        "password": "123",
        "phone": "22324345",
        "mail": "a@gmail.com",
        "admin": 0
    }
    user_2 = {

        "name": "b",
        "password": "1231",
        "phone": "22324366",
        "mail": "b@gmail.com",
        "admin": 1
    }
    user_1_credentials = {
        "mail": user_1["mail"],
        "password": user_1["password"]
    }
    user_2_credentials = {
        "mail": user_2["mail"],
        "password": user_2["password"]
    }
    update = {
        "name": "anton",
        "phone":"3992993"
    }

    ticket = {
        "clas": "VIP"
    }
    show = {
        "description": "very funny show",
        "name": "Varjaty Show",
        "place": "Dovjenka theatre",
        "show_id": 1,
        "show_type": "comedy",
        "time": "18-12-2020 18:00:00"
    }

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def setUp(self):
        session.commit()
        Base.metadata.create_all(engine)

    def tearDown(self):
        session.commit()
        Base.metadata.drop_all(bind=engine)

    def get_auth_headers(self,credentials):
        resp= self.client.post("/login", json =credentials)
        access_token = resp.json["access_token"]
        return {'Authorisation':f'Bearer {access_token}'}

    def test_creation(self):
        encoded_data = json.dumps(self.user_1).encode('utf-8')
        resp = self.client.post('/register',data=encoded_data,
            headers={'Content-Type': 'application/json', 'Accept': 'application/json'}
        )
        self.assertEqual(resp.status_code,200)
    def test_creation_admin(self):
        encoded_data = json.dumps(self.user_2).encode('utf-8')
        resp = self.client.post('/register',data=encoded_data,
            headers={'Content-Type': 'application/json', 'Accept': 'application/json'}
        )
        self.assertEqual(resp.status_code,200)
    def test_admin_auth(self):
        self.test_creation_admin()
        resp = self.client.post("/login", json=self.user_2_credentials)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json,{"access_token":ANY})

    def test_user_auth(self):
        self.test_creation()
        resp = self.client.post("/login", json=self.user_1_credentials)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {"access_token": ANY})

    def test_get_own(self):
        self.test_creation()
        resp1 = self.client.post("/login", json=self.user_1_credentials)
        token = resp1.json["access_token"]
        resp = self.client.get("/user",headers={

                                        'Authorization': f'Bearer {token}'})
        self.assertEqual(resp.status_code, 201)

    def test_get_id(self):
        self.test_creation_admin()
        resp1 = self.client.post("/login", json=self.user_2_credentials)
        token = resp1.json["access_token"]
        resp = self.client.get("/user/1", headers={
            'Authorization': f'Bearer {token}'})
        self.assertEqual(resp.status_code, 201)

    def test_update_user(self):
        self.test_creation()
        encoded_data = json.dumps(self.update).encode('utf-8')
        resp = self.client.post("/login", json=self.user_1_credentials)
        token = resp.json["access_token"]
        resp1 = self.client.put(
            '/user',
            data=encoded_data, headers={'Content-Type': 'application/json',
                                        'Accept': 'application/json',
                                        'Authorization': f'Bearer {token}'}
        )
        self.assertEqual(resp1.status_code, 200)

    def test_create_show(self):
        self.test_creation_admin()
        encoded_data = json.dumps(self.show).encode('utf-8')
        resp = self.client.post("/login", json=self.user_2_credentials)
        token = resp.json["access_token"]
        resp1 = self.client.post('/show', data=encoded_data,
                                headers={'Content-Type': 'application/json', 'Accept': 'application/json','Authorization': f'Bearer {token}'}
                                )
        self.assertEqual(resp1.status_code, 200)

    def test_add_ticket(self):
        self.test_create_show()
        encoded_data = json.dumps(self.ticket).encode('utf-8')
        resp = self.client.post("/login", json=self.user_2_credentials)
        token = resp.json["access_token"]
        resp1 = self.client.post('/ticket/1', data=encoded_data,
                                headers={'Content-Type': 'application/json', 'Accept': 'application/json','Authorization': f'Bearer {token}'}
                                )
        self.assertEqual(resp1.status_code, 200)

    def test_buy_ticket(self):
        self.test_add_ticket()
        #encoded_data = json.dumps(self.update).encode('utf-8')
        resp = self.client.post("/login", json=self.user_2_credentials)
        token = resp.json["access_token"]
        resp1 = self.client.put(
            '/ticket/buy/1', headers={'Content-Type': 'application/json',
                                        'Accept': 'application/json',
                                        'Authorization': f'Bearer {token}'}
        )
        self.assertEqual(resp1.status_code, 200)

    def test_reserv(self):
        self.test_add_ticket()
        # encoded_data = json.dumps(self.update).encode('utf-8')
        resp = self.client.post("/login", json=self.user_2_credentials)
        token = resp.json["access_token"]
        resp1 = self.client.put(
            '/ticket/reserve/1', headers={'Content-Type': 'application/json',
                                      'Accept': 'application/json',
                                      'Authorization': f'Bearer {token}'}
        )
        self.assertEqual(resp1.status_code, 200)

    def test_get_alltic(self):
        self.test_add_ticket()
        resp1 = self.client.post("/login", json=self.user_2_credentials)
        token = resp1.json["access_token"]
        resp = self.client.get("/tickets",headers={

                                        'Authorization': f'Bearer {token}'})
        self.assertEqual(resp.status_code, 201)
