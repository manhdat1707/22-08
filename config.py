from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
import redis
from flask import Flask,jsonify,request,Response,render_template,redirect,session,url_for
import json
from werkzeug.security import generate_password_hash, check_password_hash
import bcrypt





app = Flask(__name__)
app.secret_key = "abc"


client = MongoClient("localhost", 27017)
db = client.test





def get_list_user():
        data_select = list(db.user.find())
        return json.dumps(data_select, default=str)

def del_acc_by_id(id):
        db.account.delete_one({"_id" :ObjectId(id)})
def get_list_account():
        data_select = list(db.account.find())
        return json.dumps(data_select , default=str)



r = redis.Redis(host='127.0.0.1', port=6379)
