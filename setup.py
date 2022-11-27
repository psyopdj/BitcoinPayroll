import json

from bson import ObjectId
from flask import Flask
from flask.json import JSONEncoder
from flask_pymongo import PyMongo
from flask_session import Session
from pymongo import MongoClient

from src.api.model.employee import Employee

app = Flask(__name__)
mongo_uri = "mongodb+srv://super:super@maincluster.tt6dyyu.mongodb.net/?retryWrites=true&w=majority"
app.config["MONGO_URI"] = mongo_uri


class CustomJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        elif isinstance(o, Employee):
            return o.to_json()
        return json.JSONEncoder.default(self, o)


app.json_encoder = CustomJSONEncoder

mongo = PyMongo(app)

SESSION_TYPE = 'mongodb'
SESSION_MONGODB = MongoClient(mongo_uri)
SESSION_MONGODB_DB = 'BitcoinPayroll'
SESSION_MONGODB_COLLECT = 'sessions'
PERMANENT_SESSION_LIFETIME = 1800   # 30 minutes
SESSION_USE_SIGNER = True
app.config.from_object(__name__)
Session(app)
