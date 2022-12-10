from http import HTTPStatus

from flask import Blueprint, request, make_response, jsonify

from src.api.model.employee import Employee
from src.api.model.error import ErrorResponse
from src.api.service import employee as employee_service

employee_api = Blueprint('employees-api', __name__)
employee_api.url_prefix = '/api/employees'


@employee_api.route('/', methods=['GET'])
def find_all():
    """
    Retrieve all employees
    Return the employees with a 200 response.
    """
    employees = employee_service.find_all()
    return make_response(jsonify(employees), HTTPStatus.OK)


@employee_api.route('/<id>', methods=['GET'])
def find_by_id(id):
    """
    Retrieve an employee by its ID
    If the employee does not exist, return 404 response.
    If the employee does exist, return a 200 response with the employee.
    """
    employee = employee_service.find_by_id(id)
    if employee is None:
        response = ErrorResponse(HTTPStatus.NOT_FOUND, "employee not found by ObjectId: '{}'".format(id))
        return make_response(response.to_json_response(), response.code)
    return make_response(jsonify(employee), HTTPStatus.OK)


@employee_api.route('/rfid/<rfid>', methods=['GET'])
def find_by_rfid(rfid):
    """
    Retrieve an employee by its RFID
    If the employee does not exist, return 404 response.
    If the employee does exist, return a 200 response with the employee.
    """
    employee = employee_service.find_by_rfid(rfid)
    if employee is None:
        response = ErrorResponse(HTTPStatus.NOT_FOUND, "employee not found by RFID: '{}'".format(id))
        return make_response(response.to_json_response(), response.code)
    return make_response(jsonify(employee), HTTPStatus.OK)


@employee_api.route('/walletaddress/<wallet_address>', methods=['GET'])
def find_by_wallet_address(wallet_address):
    """
    Retrieve an employee by its wallet address
    If the employee does not exist, return 404 response.
    If the employee does exist, return a 200 response with the employee.
    """
    employee = employee_service.find_by_wallet_address(wallet_address)
    if employee is None:
        response = ErrorResponse(HTTPStatus.NOT_FOUND,
                                 "employee not found by wallet address: '{}'".format(wallet_address))
        return make_response(response.to_json_response(), response.code)
    return make_response(jsonify(employee), HTTPStatus.OK)


@employee_api.route('/', methods=['POST'])
def create_employee():
    """
    Create a new Employee.

    If a required field is missing in the request body, return a 400 response.
    If the employee is successfully created, return the report with a 201 response.
    """
    try:
        employee = Employee.from_json_dict(request.json)
        existing_employee = employee_service.find_by_rfid(employee.rfid)
        if existing_employee is not None:
            response = ErrorResponse(HTTPStatus.BAD_REQUEST,
                                     "RFID already is assigned for an employee. Please use a different RFID")
            return make_response(response.to_json_response(), response.code)
        employee_service.insert(employee)
        return make_response(jsonify(employee), HTTPStatus.CREATED)
    except KeyError as e:
        response = ErrorResponse(HTTPStatus.BAD_REQUEST, "Missing field in request body: {}".format(e))
        return make_response(response.to_json_response(), response.code)


@employee_api.route('/<id>', methods=['DELETE'])
def delete_employee_by_id(id):
    """
    Delete an employee by its ID

    If the employee does not exist, return a 404 response
    If the employee is deleted, return a 204 response.
    """
    result = employee_service.delete_by_id(id)
    if result != 1:
        response = ErrorResponse(HTTPStatus.NOT_FOUND, "Employee not found to delete by ID: {}".format(id))
        return make_response(response.to_json_response(), response.code)
    return make_response('', HTTPStatus.NO_CONTENT)
