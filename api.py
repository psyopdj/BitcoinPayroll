from pymongo_get_database import get_database
import flask
from flask import request, jsonify
from src.endpoints import *

dbname = get_database()
employees = dbname["employees"]     #collection for employees
shifts = dbname["shifts"]           #collection for shifts

app = flask.Flask(__name__)
app.config["DEBUG"] = True

#root page landing
@app.route('/')
def root():
    return "<h1>Bitcoin Paycheck Service</h1> \
            <p>This site is a prototype API for a payroll system that pays employees using bitcoin.</p>"


#this page is hit whenever a new employee needs to be added to the system
@app.route('/add_employee/', methods=['GET'])
def add_employee():
    address = ""
    if 'address' in request.args:
        address = request.args['address']

        #find the next available clock number
        clock = 0
        for doc in employees.find():
            if (int(doc['clock']) > clock):
                clock = int(doc['clock'])

        #insert the new employee into the database
        employees.insert_one({
            "clock" : str(clock + 1),
            "address" : address
        })

        return "<h1>Employee Added</h1> \
                <p>A new employee has been added and given the next available employee number.</p>"
    else:
        return "<h1>Error</h1> \
                <p>Please provide a bitcoin address for the new employee added.</p>"


#this page is hit whenever an employee needs to be removed from the system
@app.route('/delete_employee/', methods=['GET'])
def del_employee():
    if 'clock' in request.args:
        employees.delete_one({'clock' : request.args['clock']})

        shifts.delete_many({'clock' : request.args['clock']})

        return "<h1>Employee Deleted</h1> \
                <p>The employee has been removed from the database.</p>"
    else:
        return "<h1>Error</h1> \
                <p>Please provide a valid clock number for the employee you want to remove.</p>"


#this page is hit whenever a new shift need to be added to the system
@app.route('/add_shift/', methods=['GET'])
def add_shift():
    if ('clock' in request.args and 'st' in request.args and 'end' in request.args and 'date' in request.args):

        #calculate hours worked
        start_hr = float(request.args['st'][:2])
        end_hr = float(request.args['end'][:2])
        start_min = float(request.args['st'][-2:])
        end_min = float(request.args['end'][-2:])

        hours_worked = end_hr - start_hr
        if (start_min < end_min):
            hours_worked += (end_min - start_min)/60
        elif (start_min > end_min):
            hours_worked -= (start_min - end_min)/60
        hours_worked = "{:2.2f}".format(hours_worked)

        #add shift to the database with all the necessary information
        shifts.insert_one({
            "clock" : request.args['clock'],
            "date" : request.args['date'],
            "time in" : request.args['st'],
            "time out" : request.args['end'],
            "hours worked" : hours_worked
        })

        return "<h1>Shift Added</h1> \
                <p>A new shift has been added.</p>"

    else:
        return "<h1>Error</h1> \
                <p>Please be sure to include clock #, start time, end time, and the date.</p>"

app.run()
