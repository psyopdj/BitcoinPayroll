from bson import ObjectId
from bson.errors import InvalidId

from src.api.model.employee import Employee
from setup import mongo

employee_collection = mongo.db.employee

'''
Find all employees that exist. If no employees exist, return an empty list
'''


def find_all():
    employees_result = employee_collection.employee.find({'enabled': True}).sort("clock")
    employees = []
    for employee in employees_result:
        employees.append(Employee.from_json_dict(employee))
    return employees


'''
Find and return a employee by its ID.
Return None if the employee is not found.
'''


def find_by_id(emp_id):
    try:
        employee = employee_collection.find_one({'_id': ObjectId(emp_id)})
        if employee is None:
            return None
        return Employee.from_json_dict(employee)
    except InvalidId:
        return None


'''
Find and return a employee by its name.
Return None if the employee is not found.
'''


def find_by_address(address):
    try:
        regex = {"name": {"$regex": "^" + address + "$", "$options": "i"}}
        employee = employee_collection.find_one(regex)
        if employee is None:
            return None
        return Employee.from_json_dict(employee)
    except InvalidId:
        return None


'''
Insert a new employee and return it
'''


def insert(employee):
    employee._id = None
    employee_id = employee_collection.insert_one(employee.to_json()).inserted_id
    employee._id = employee_id


'''
Find and delete a employee by an ID.
Return the number of employees deleted (should be 1 or 0)
'''


def delete_by_id(employee_id):
    try:
        result = employee_collection.delete_one({'_id': ObjectId(employee_id)})
        return result.deleted_count
    except InvalidId:
        return None
