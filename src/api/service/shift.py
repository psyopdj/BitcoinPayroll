import datetime
import time

import pymongo
from bson import ObjectId
from bson.errors import InvalidId
from pymongo import ReturnDocument

from src.api.model.shift import Shift
from setup import mongo

shift_collection = mongo.db.shifts


def find_all():
    """
    Find all shifts that exist. If no shifts exist, return an empty list
    """
    shifts_result = shift_collection.find().sort('in_timestamp', pymongo.DESCENDING)
    shifts = []
    for shift in shifts_result:
        shifts.append(Shift.from_json_dict(shift))
    return shifts


def find_by_id(shift_id):
    """
    Find and return a shift by its ID.
    Return None if the shift is not found.
    """
    try:
        shift = shift_collection.find_one({'_id': ObjectId(shift_id)})
        if shift is None:
            return None
        return Shift.from_json_dict(shift)
    except InvalidId:
        return None


def find_all_by_employee(employee_id):
    """
    Find and return all shifts for an employee
    Return an empty list if the employee is not found or no shifts exist for that employee
    """
    shifts_result = shift_collection.find({'employee_id': ObjectId(employee_id)}) \
        .sort('in_timestamp', pymongo.DESCENDING)
    shifts = []
    for shift in shifts_result:
        shifts.append(Shift.from_json_dict(shift))
    return shifts


def clock_in(employee_id):
    """
    Insert a new shift and return it
    """
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    shift = Shift(None, employee_id, date, time.time(), None)
    shift_id = shift_collection.insert_one(shift.to_json()).inserted_id
    shift._id = shift_id
    return shift


def clock_out(employee_id):
    """
    Update the latest employee's shift that doesn't have an out_timestamp
    """
    query = {
        "$and": [
            {"employee_id": employee_id},
            {"out_timestamp": None}
        ]
    }
    new_values = {"$set": {"out_timestamp": time.time()}}
    result = shift_collection.find_one_and_update(query, new_values, return_document=ReturnDocument.AFTER)
    return result


def delete_by_id(shift_id):
    """
    Find and delete a shift by an ID.
    Return the number of shifts deleted (should be 1 or 0)
    """
    try:
        result = shift_collection.delete_one({'_id': ObjectId(shift_id)})
        return result.deleted_count
    except InvalidId:
        return None
