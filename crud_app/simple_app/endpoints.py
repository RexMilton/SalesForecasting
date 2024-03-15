import logging

from flask_pymongo import pymongo
from flask import jsonify, request
import pandas as pd
import json
from simple_app.ml import process

l=[{"test":"res-fine"}]


con_string = "mongodb+srv://RexMiltonS:Rexmilton5*@cluster0.3ekp5xp.mongodb.net/?retryWrites=true&w=majority"

client = pymongo.MongoClient(con_string)

db = client.get_database('login_creds')

user_collection = pymongo.collection.Collection(db, 'login_creds')
print("MongoDB connected Successfully")


def project_api_routes(endpoints):

    @endpoints.route('/register-user', methods=['POST'])
    def register_user():
        resp = {}
        try:
            req_body = request.json
            # req_body = req_body.to_dict()
            user_collection.insert_one(req_body)
            print("User Data Stored Successfully in the Database.")
            status = {
                "statusCode": "200",
                "statusMessage": "User Data Stored Successfully in the Database."
            }
        except Exception as e:
            print(e)
            status = {
                "statusCode": "400",
                "statusMessage": str(e)
            }
        resp["status"] = status
        return resp

    @endpoints.route('/read-users', methods=['GET'])
    def read_users():
        resp = {}
        try:
            users = user_collection.find({})
            print(users)
            users = list(users)
            status = {
                "statusCode": "200",
                "statusMessage": "User Data Retrieved Successfully from the Database."
            }
            output = [{'email':user['email'],'password': user['password']} for user in users]  # list comprehension
            resp['data'] = output
        except Exception as e:
            print(e)
            status = {
                "statusCode": "400",
                "statusMessage": str(e)
            }
        # resp["status"] = status
        return resp

    @endpoints.route('/file_upload',methods=['POST'])
    def file_upload():
        resp = {}
        try:
            req = request.form
            file = request.files.get('file')
            df = pd.read_csv(file)
            print(df.head)
            print(df.columns)
            global l
            l=process(df)
            # print(l)
            status = {
                "statusCode":"200",
                "statusMessage":"File uploaded Successfully.",
                "res": "hello"
            }
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
        resp["status"] = status
        return resp

    @endpoints.route('/get_data',methods=['GET'])
    def get_data():
        x={
            "date":l[0],
            "sales":l[1], 
            "forecast":l[2],
            'comments':l[3]
        }
        return x
    
    return endpoints
