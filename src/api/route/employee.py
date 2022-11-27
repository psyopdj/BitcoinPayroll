from http import HTTPStatus

from flask import Blueprint, make_response, jsonify, request
from src.api.model.error import ErrorResponse
from src.api.service import employee as employee_service

employee_api = Blueprint('employees-api', __name__)
employee_api.url_prefix = '/api/employee'

'''
Retrieve all enabled employees
Return the employees with a 200 response.
'''


@employee_api.route('/', methods=['GET'])
def find_all():
    print("test")
    employees = employee_service.find_all()
    return make_response(jsonify(employees), HTTPStatus.OK)


'''
Retrieve a employee by its ID
If the employee does not exist, return 404 response.
If the employee does exist, return a 200 response with the employee.
'''


@employee_api.route('/<id>', methods=['GET'])
def find_by_id(id):
    employee = employee_service.find_by_id(id)
    if employee is None:
        response = ErrorResponse(HTTPStatus.NOT_FOUND, "employee not found by ObjectId: '{}'".format(id))
        return make_response(response.to_json_response(), response.code)
    return make_response(jsonify(employee), HTTPStatus.OK)


'''
Retrieve a employee by its name
If the employee does not exist, return 404 response.
If the employee does exist, return a 200 response with the employee.
'''


@employee_api.route('/address/<address>', methods=['GET'])
def find_by_address(address):
    employee = employee_service.find_by_address(address)
    if employee is None:
        response = ErrorResponse(HTTPStatus.NOT_FOUND, "employee not found by name: '{}'".format(address))
        return make_response(response.to_json_response(), response.code)
    return make_response(jsonify(employee), HTTPStatus.OK)
