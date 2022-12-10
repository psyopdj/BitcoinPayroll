# Importing Libraries
import json
import serial
import time
import requests
arduino = serial.Serial(port='COM3', baudrate=9600, timeout=.1)
BASE = 'https://2b95-128-62-38-151.ngrok.io/'
#BASE = 'https://95ca-2600-1700-210-d420-99db-5759-3237-bcae.ngrok.io'

employee_url = BASE + '/api/employees/'
shift_url = BASE + '/api/shifts/'
while True:
    try:
        data = arduino.readline().decode().rstrip()
        if data:


            shift1 = {
                'rfid': data
            }

            x = requests.post(shift_url, json=shift1)

            string = data
            time.sleep(0.05)
            json_object = json.loads(x.text)
            json_formatted_str = json.dumps(json_object, indent=2)
            print(json_formatted_str) # printing the value
    except Exception as e:
        print(e)
