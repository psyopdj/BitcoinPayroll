import datetime
import time

import pymongo
from bson import ObjectId
from bson.errors import InvalidId
from pymongo import ReturnDocument

from src.api.model.shift import Shift
from setup import mongo
from setup import app
from src.bitcoin.encoder import encode_tx
from src.bitcoin.hash import hash256
from src.bitcoin.helper import decode_address
from src.bitcoin.rpc import RpcSocket
from src.bitcoin.sign import sign_tx

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


def clock_in(employee):
    """
    Insert a new shift and return it
    """
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    shift = Shift(None, employee._id, date, time.time(), None, None)
    shift_id = shift_collection.insert_one(shift.to_json()).inserted_id
    shift._id = shift_id
    return shift


def clock_out(employee):
    """
    Update the latest employee's shift that doesn't have an out_timestamp
    """
    query = {
        "$and": [
            {"employee_id": employee._id},
            {"out_timestamp": None}
        ]
    }
    # Update shift with new out_timestamp
    new_values = {"$set": {"out_timestamp": time.time()}}
    shift_dict = shift_collection.find_one_and_update(query, new_values, return_document=ReturnDocument.AFTER)
    return Shift.from_json_dict(shift_dict)


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


def pay_out(shift, employee, employee_recv_value, fee):
    """
    Pay out to an employee based on the shift worked
    """
    rpc = RpcSocket({'wallet': app.config["EMPLOYER_WALLET_NAME"]})
    assert rpc.check()

    # First, we will look up an existing utxo, and use that to fund our transaction
    employer_utxo = rpc.get_utxo(0)

    # Get a change address for the employer
    employer_change_txout = rpc.get_recv()
    _, employer_redeem_script = decode_address(employer_change_txout['address'])

    # Get a payment address for the employee
    _, employee_redeem_script = decode_address(employee.wallet_address)

    # Calculate our output amounts
    employer_change_value = employer_utxo['value'] - employee_recv_value - fee

    # The initial spending transaction. This tx spends a previous utxo,
    # and commits the funds to our P2WPKH transaction
    transaction = {
        'version': 1,
        'vin': [{
            # We are unlocking the utxo from the Employer.
            'txid': employer_utxo['txid'],
            'vout': employer_utxo['vout'],
            'script_sig': [],
            'sequence': 0xFFFFFFFF
        }],
        'vout': [
            {
                'value': employee_recv_value,
                'script_pubkey': [0, employee_redeem_script]
            },
            {
                'value': employer_change_value,
                'script_pubkey': [0, employer_redeem_script]
            }
        ],
        'locktime': 0
    }

    # Serialize the transaction and calculate the transaction ID
    transaction_hex = encode_tx(transaction)
    transaction_id = hash256(bytes.fromhex(transaction_hex))[::-1].hex()

    # The redeem-script is a basic Pay-to-Pubkey-Hash template
    redeem_script = f"76a914{employer_utxo['pubkey_hash']}88ac"

    # Sign the employer's UTXO using BIP143 standard
    employer_signature = sign_tx(
        transaction,  # The transaction
        0,  # The input being signed
        employer_utxo['value'],  # The value of the utxo being spent
        redeem_script,  # The redeem-script to unlock the utxo
        employer_utxo['priv_key']  # The private key to the utxo pubkey hash
    )

    # Include the arguments needed to unlock the redeem-script
    transaction['vin'][0]['witness'] = [employer_signature, employer_utxo['pub_key']]

    print(f'''
    ## Sending Transaction ##
    -- Transaction Id --
    {transaction_id}

    -- Employer UTXO --
         Txid : {employer_utxo['txid']}
         Vout : {employer_utxo['vout']}
        Value : {employer_utxo['value']}
         Hash : {employer_utxo['pubkey_hash']}

    -- Sending to Employee --
           ID : {employee._id}
         Name : {employee.name}
      Address : {employee.wallet_address}
        Coins : {employee_recv_value}

    -- Change --
      Address : {employer_change_txout['address']}
          Fee : {fee}
        Coins : {employer_change_value}

    -- Hex --
    {encode_tx(transaction)}
    ''')

    txid = rpc.send_transaction(transaction)
    print("Successfully sent transaction with ID: " + txid)

    # Update shift with transaction ID
    new_values = {"$set": {"transaction_id": transaction_id}}
    return shift_collection.find_one_and_update({'_id': ObjectId(shift._id)}, new_values,
                                                return_document=ReturnDocument.AFTER)
