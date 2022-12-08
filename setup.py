import json

from bson import ObjectId
from flask import Flask
from flask.json import JSONEncoder
from flask_pymongo import PyMongo

from src.api.model.employee import Employee
from src.api.model.shift import Shift

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://super:super@maincluster.tt6dyyu.mongodb.net/BitcoinPayroll?retryWrites=true&w=majority"
app.config["EMPLOYER_WALLET_NAME"] = "regtest"

class CustomJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        elif isinstance(o, Employee):
            return o.to_json()
        elif isinstance(o, Shift):
            return o.to_json()
        return json.JSONEncoder.default(self, o)


app.json_encoder = CustomJSONEncoder

mongo = PyMongo(app)