from bson import ObjectId
from bson.errors import InvalidId

from src.api.model.employee import Employee
from setup import mongo

employee_collection = mongo.db.employees


def find_all():
    """
    Find all employees that exist. If no employees exist, return an empty list
    """
    employees_result = employee_collection.find().sort("name")
    employees = []
    for employee in employees_result:
        employees.append(Employee.from_json_dict(employee))
    return employees


def find_by_id(employee_id):
    """
    Find and return an employee by its ID.
    Return None if the employee is not found.
    """
    try:
        employee = employee_collection.find_one({'_id': ObjectId(employee_id)})
        if employee is None:
            return None
        return Employee.from_json_dict(employee)
    except InvalidId:
        return None


def find_by_rfid(rfid):
    """
    Find and return an employee by its RFID.
    Return None if the employee is not found.
    """
    employee = employee_collection.find_one({'rfid': rfid})
    if employee is None:
        return None
    return Employee.from_json_dict(employee)


def find_by_wallet_address(wallet_address):
    """
    Find and return an employee by its wallet address.
    Return None if the employee is not found.
    """
    try:
        employee = employee_collection.find_one({'wallet_address': wallet_address})
        if employee is None:
            return None
        return Employee.from_json_dict(employee)
    except InvalidId:
        return None


def insert(employee):
    """
    Insert a new employee and return it
    """
    employee._id = None
    employee_id = employee_collection.insert_one(employee.to_json()).inserted_id
    employee._id = employee_id


def delete_by_id(employee_id):
    """
    Find and delete an employee by an ID.
    Return the number of employees deleted (should be 1 or 0)
    """
    try:
        result = employee_collection.delete_one({'_id': ObjectId(employee_id)})
        return result.deleted_count
    except InvalidId:
        return None
