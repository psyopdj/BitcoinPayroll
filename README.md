# BitcoinPayroll

Project for Blockchains &amp; Smart Contracts taught at the University of Texas at Austin

Bitcoin Payroll is a system where employees are paid in satoshis immediately upon finishing their shift of work.

## Contributors

Tyler Carlson (tc26763) \
Jason Castillo (jzc248) \
Saehej Kang (ssk2353) \
Tyler Stubbs (tjs986)


* [Introduction](#introduction)
* [Design](#design)
  * [MongoDB](#mongodb)
    * [Employees](#employees)
    * [Shifts](#shifts)
  * [API Architecture](#api-architecture)
* [Setup](#setup)
  * [Bitcoin Node](#bitcoin-node)
  * [Employer Wallet](#employer-wallet)
  * [Run the API](#run-the-api)
  * [Optional Hardware Setup](#optional-hardware-setup)
    * [Setting up ngrok](#setting-up-ngrok)
  * [Create Employee](#create-employee)
* [Using the App](#using-the-app)
  * [With RFID Scanner](#with-rfid-scanner)
  * [Without RFID Scanner](#without-rfid-scanner)

## Introduction

Bitcoin Payroll is a system where employees are paid in Satoshis immediately upon finishing their shift of work.
Each employee has an RFID badge that they use to badge in/out of work. Both RFID transactions are logged to a database.
The hours worked is calculated upon clocking out.

The Satoshis paid are then sent to the address on file for the employee. If the payout amount is less than the 1000
Satoshi fee, then the shift will be canceled and no transaction will take place.

To recap:
- Each employee has an RFID badge that they use to badge in/out of work. Both RFID transactions are logged to a database. 
- The hours worked is calculated upon clocking out. 
- The satoshis paid are then sent to the address on file for the employee.

## Design

### MongoDB

#### Employees

An **Employee** is a collection of information about an employee. This includes information such as the ID of the
employee (which gets
assigned during creation of that employee), the employee name, their pay_rate (in Satoshis), the rfid value which should
be associated
with an employees badge, and the wallet address that they want to pay out to (Make sure this aligns with which bitcoin
network you are on).
All payments are done on-chain.

The following is an example Employee.

```json
{
  "_id": "0123456789",
  "name": "Mr Satoshi",
  "pay_rate": 500000,
  "rfid": "9876543210",
  "wallet_address": "1234abcd"
}
```

#### Shifts

A **Shift** is a collection of information about a work shift for an employee. This includes information such as the ID
of the shift (which gets assigned during creation of that shift on clock-in), the date that the shift was for, the
employee_id
that is associated with that shift, the in_timestamp (which is assigned when clocking in), the out_timestamp (which is
assigned when
clocking out), and the transaction_id (which is the ID of the on-chain transaction ID after submitting to the selected
network).

The following is an example Shift.

```json
{
  "_id": "6393b9532893abf57fff18ff",
  "date": "2022-12-09",
  "employee_id": "638ae6ebe0ebdcdbfea24a2e",
  "in_timestamp": 1670625619.878994,
  "out_timestamp": 1670625624.008638,
  "transaction_id": "820ee969c5cfb3a8e6b35a163edc6403569c0a81aeb66fe2de4bb74e1b0bdd67"
}
```

### API Architecture

The Web API is a collection of HTTP endpoints that interact with the database and return Json responses. The UI
interacts with these endpoints in order to retrieve data to process and display. The following endpoints are available.

**Employee API**

```
GET /api/employees                        Find all employees
GET /api/employees/<id>                   Find an employee by their ID
GET /api/employees/rfid/<rfid>            Find an employee by their rfid value
POST /api/employees                       Create a new employee (employee json in request body)
DELETE /api/employees/<id>                Delete an employee by its ID
```

**Shift API**

```
GET /api/shifts                        Find all shifts
GET /api/shifts/<id>                   Find a shift by its ID
GET /api/shifts/employee/<employee_id> Find all shifts for an employee ID
POST /api/shifts                       Clock In/Out (request body is json object with 1 entry *rfid*. Ff no previous shift for employee - clock in, otherwise clock out and then pay out)
DELETE /api/shifts/<id>                Delete a shift by its ID
```

You can find a Postman collection of all endpoints in the root `/postman` directory.

## Setup

### Bitcoin Node

Before running the API, you need a local instance of bitcoin core running on your machine. The API talks to bitcoin core
on port **18443**, so make sure that it is running on that port.

### Employer Wallet

The API also needs to have a wallet to pay its employees from. To set the name of the wallet in the API, navigate to
the`setup.py` file in the top level directory. You will see a line like the following. You just need to change the wallet name
to the name of your wallet on your bitcoin core node (and with which network you are using).

```python
app.config["EMPLOYER_WALLET_NAME"] = "regtest"
```

In this example, we are using a wallet called _regtest_. Change this to whatever you have locally.

### Run the API

Make sure that you have a virtual python environment setup with the required packages installed.

Use your IDE or follow the steps below.

```bash
# create virtual env and install dependencies
$ python3 -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt

# run the app
$ python main.py
```

The API runs locally on your machine with this URL.

`` http://127.0.0.1:5000/``


### Optional Hardware Setup

We used the hardware below:

- Arduino: MEGA2560 R3
- RFID-RC522 Sensor 
- RFID card and RFID tag

1. Connect RFID sensor onto the arduino with the schematic in the top right corner 
1. The arduino is connected to a laptop using USB cable. 

```Note: The MEGA2560 doesn’t have WIFI capabilities and needed to be hooked up via a USB to connect to the server```


#### Setting up ngrok

If using hardware, you need to expose the local url running on your machine so the Arudino can hit it.

Run the following command to create the proxy:

~~~
ngrok http 127.0.0.1:5000  
~~~

### Create Employee

In order to get paid, you must create an employee with a wallet address and unique RFID value. Make a `POST /api/employees` 
request like the following with the data you want for you (being the new employee).

```json
{
    "name": "Your Name",
    "pay_rate": 200000,
    "rfid": "<unique rfid value>",
    "wallet_address": "<your wallet address on your bitcoin core instance>"
}
```

## Using the App

### With RFID Scanner

If you have a rfid scanner (we used an arduino with a scanner), you just need to point the
arduino (or whatever you are using) to hit the `POST /api/shifts` endpoint of the API any time
the rfid scanner is scanned, with a payload as follows.

```json
{
  "rfid": "123456789"
}
```

The API does all the heavy lifting, by determining if you are already clocked in and must clock out, or if you need to
clock in. After submitting the request for the first time, you will get a response with a new shift object, but the out_timestamp
and transaction_id will be _null_. After clocking out again, those fields should populate, and you should see the Sats in your wallet!

### Without RFID Scanner

If you do NOT have a scanner, you can just send the same `POST /api/shifts` request to the API to mimic the RFID
scanner.
