from unittest import result
from pymongo import MongoClient 
from bson import ObjectId 
import os
from datetime import datetime
import redis
from flask import Flask,jsonify,request,Response,render_template,redirect,session,flash,url_for
import json
from werkzeug.utils import secure_filename
import bcrypt




UPLOAD_FOLDER = r'C:\Users\hp\Desktop\a\upload'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__)
app.secret_key = "abc"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


client = MongoClient("localhost", 27017)
db = client.test

# class attachments (db.document):

    


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)



def get_list_user():
    data_select = list(db.user.find())
    results =[]
    for data in data_select:
            print(data)
            data["_id"] = str(data["_id"])
            if data.get("create_time"):
                data["create_time"] = data["create_time"].timestamp()
            print("data : ", data)
            results.append(data)
    print("result", results)
    return results
def get_user_by_id(id):
    data_select = db.user.find({"_id":ObjectId(id)})
    results = []
    for data in data_select:
        data["_id"] = str(data["_id"])
        if data.get("create_time"):
            data["create_time"] = data["create_time"].timestamp()
        print("data : ", data)
        results.append(data)
    return results



def get_attachments_id(id):
    data_select = db.attachments.find({"user_id":id},{"user_id":0})
    results = []
    for data in data_select:
        data["_id"] = str(data["_id"])
        if data.get("create_time"):
            data["create_time"] = data["create_time"].timestamp()
        if data.get("update_time"):
            data["update_time"] = data["update_time"].timestamp()
        print("data : ", data)
        results.append(data)
    return results

    
def del_acc_by_id(id):
        db.account.delete_one({"_id" :ObjectId(id)})


def get_list_account():
        data_select = list(db.account.find({}, {"password": 0}))
        results =[]
        for data in data_select:
                data["_id"] = str(data["_id"])
                if data.get("created_time"):
                    data["created_time"] = data["created_time"].timestamp()
                print("data : ", data)
                results.append(data)
        return results

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
r = redis.Redis(host='127.0.0.1', port=6379)
# update 
# delete
# create