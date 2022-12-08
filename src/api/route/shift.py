import math
from http import HTTPStatus

from flask import Blueprint, request, make_response, jsonify

from src.api.model.error import ErrorResponse
from src.api.service import shift as shift_service
from src.api.service import employee as employee_service

shift_api = Blueprint('shifts-api', __name__)
shift_api.url_prefix = '/api/shifts'


@shift_api.route('/', methods=['GET'])
def find_all():
    """
    Retrieve all shifts
    Return the shifts with a 200 response.
    """
    shifts = shift_service.find_all()
    return make_response(jsonify(shifts), HTTPStatus.OK)


@shift_api.route('/<id>', methods=['GET'])
def find_by_id(id):
    """
    Retrieve a shift by its ID
    If the shift does not exist, return 404 response.
    If the shift does exist, return a 200 response with the shift.
    """
    shift = shift_service.find_by_id(id)
    if shift is None:
        response = ErrorResponse(HTTPStatus.NOT_FOUND, "shift not found by ObjectId: '{}'".format(id))
        return make_response(response.to_json_response(), response.code)
    return make_response(jsonify(shift), HTTPStatus.OK)


@shift_api.route('/employee/<employee_id>', methods=['GET'])
def find_by_employee_id(employee_id):
    """
    Retrieve all shifts for an employee given their ID
    Return the shifts with a 200 response.
    """
    shifts = shift_service.find_all_by_employee(employee_id)
    return make_response(jsonify(shifts), HTTPStatus.OK)


@shift_api.route('/', methods=['POST'])
def clock_in_or_out():
    """
    Either clock in or clock out depending on what exists in the db for specified employee given its RFID

    If a required field is missing in the request body, return a 400 response.
    If the shift is successfully created, return the report with a 201 response.
    """
    if "rfid" not in request.json:
        response = ErrorResponse(HTTPStatus.BAD_REQUEST, "Missing rfid field in request body")
        return make_response(response.to_json_response(), response.code)

    rfid = request.json['rfid']
    employee = employee_service.find_by_rfid(rfid)
    if employee is None:
        response = ErrorResponse(HTTPStatus.NOT_FOUND, "No Employee found with RFID: '{}'".format(rfid))
        return make_response(response.to_json_response(), response.code)

    current_shifts = shift_service.find_all_by_employee(employee._id)
    # if there are no current shifts for this employee OR if the most recent shift has an
    # out_timestamp, then we need to clock in. Otherwise, we clock out
    if (len(current_shifts) == 0) or (current_shifts[0].out_timestamp is not None):
        print("Clocking in for employee: '{}'".format(employee._id))
        shift = shift_service.clock_in(employee)
        return make_response(jsonify(shift), HTTPStatus.CREATED)
    else:
        print("Clocking out for employee: '{}'".format(employee._id))
        shift = shift_service.clock_out(employee)
        fee = 1000
        amount = math.ceil(employee.pay_rate * ((shift.out_timestamp - shift.in_timestamp) / 3600))
        if amount < fee:
            response = ErrorResponse(HTTPStatus.BAD_REQUEST,
                                     "Transaction not sent. Payout amount was less than the fee... Maybe try actually "
                                     "working?")
            return make_response(response.to_json_response(), response.code)
        shift = shift_service.pay_out(shift, employee, amount, fee)
        return make_response(jsonify(shift), HTTPStatus.OK)


@shift_api.route('/<id>', methods=['DELETE'])
def delete_shift_by_id(id):
    """
    Delete an employee by its ID

    If the employee does not exist, return a 404 response
    If the employee is deleted, return a 204 response.
    """
    result = shift_service.delete_by_id(id)
    if result != 1:
        response = ErrorResponse(HTTPStatus.NOT_FOUND, "Shift not found to delete by ID: {}".format(id))
        return make_response(response.to_json_response(), response.code)
    return make_response('', HTTPStatus.NO_CONTENT)
